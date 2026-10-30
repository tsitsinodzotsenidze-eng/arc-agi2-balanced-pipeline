"""CPU restoration/source checks; real-model evidence is the archived PASS."""
import base64
import importlib.util
import io
import json
import math
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parent
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
b=load('study_builder',ROOT/'build_update_study.py')
s=load('probe_support',ROOT/'zero_update_probe_support.py')

class Tensor:
    def __init__(self,values=(1.,2.),dtype='bf16',shape=(2,)):
        self.values,self.dtype,self.shape=values,dtype,shape
    def numel(self):return len(self.values)

class StudyTests(unittest.TestCase):
    def test_exact_previously_reviewed_artifacts_and_repeats(self):
        z=b.build_zero();p,r=b.completed_probe(z)
        self.assertEqual(b.sha((json.dumps(z,indent=1)+'\n').encode()),b.ZERO_SHA)
        self.assertEqual(b.sha((json.dumps(p,indent=1)+'\n').encode()),b.PROBE_SHA)
        self.assertEqual((ROOT/'NVARC_2026_B1_REPEAT_SUBMISSION.ipynb').read_bytes(),(ROOT/b.B1_NAME).read_bytes())
        self.assertEqual((ROOT/'NVARC_2026_Z_REPEAT_SUBMISSION.ipynb').read_bytes(),(ROOT/'NVARC_2026_Z_ZERO_UPDATE_SUBMISSION.ipynb').read_bytes())
        self.assertEqual(r['receipt']['training']['global_step'],128)

    def test_generated_solver_has_only_one_lr_change(self):
        original=json.loads((ROOT/b.B1_NAME).read_text());zero=b.build_zero()
        self.assertEqual(original['cells'][0],zero['cells'][0])
        self.assertEqual(original['metadata']['kaggle'],zero['metadata']['kaggle'])
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);modules=[]
            for label,nb in [('b1',original),('z',zero)]:
                carrier=root/label
                with zipfile.ZipFile(io.BytesIO(base64.b64decode(b.source_bundle(''.join(nb['cells'][1]['source']))))) as a:a.extractall(carrier)
                d=load(label+'_driver',carrier/'driver.py');work=d.prepare(root/(label+'_work'))
                modules.append({f.name:f.read_text() for f in work.glob('*.py')})
            before,after=modules
            self.assertEqual(before['arc_solver.py'].count('learning_rate=5e-5,'),1)
            before['arc_solver.py']=before['arc_solver.py'].replace('learning_rate=5e-5,','learning_rate=0.0,',1)
            self.assertEqual(before,after)

    def test_changed_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'changed.ipynb';p.write_bytes((ROOT/b.B1_NAME).read_bytes()+b' ')
            with self.assertRaises(ValueError):b.build_zero(p)

    def test_adapter_guard_rejects_nonfinite_or_changed_state(self):
        def check(actual):
            return s.verify_state(actual,{'a':Tensor()},equal=lambda x,y:x.values==y.values,
                finite=lambda x:all(math.isfinite(v) for v in x.values),stage='test')
        self.assertTrue(check({'a':Tensor()})['all_exactly_equal'])
        for actual in [{},{'b':Tensor()},{'a':Tensor((1.,3.))},{'a':Tensor(dtype='fp32')},
                       {'a':Tensor(shape=(1,2))},{'a':Tensor((float('nan'),2.))}]:
            with self.subTest(actual=actual),self.assertRaises(RuntimeError):check(actual)

    def test_null_update_requires_real_complete_optimizer_work(self):
        a=dict(global_step=128,max_steps=128,learning_rate=0.,weight_decay=0.,group_lrs=[0.,0.],optimizer_steps=[128,128],train_loss=.75)
        self.assertTrue(s.validate_progress(**a)['training_executed'])
        for delta in [{'global_step':0},{'global_step':127},{'optimizer_steps':[]},
                      {'optimizer_steps':[0]},{'group_lrs':[5e-5]},{'train_loss':float('nan')},{'weight_decay':.01}]:
            with self.subTest(delta=delta),self.assertRaises(RuntimeError):s.validate_progress(**{**a,**delta})

if __name__=='__main__':unittest.main()
