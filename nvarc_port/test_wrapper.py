"""CPU-only tests: upstream code is parsed/compiled, never imported/executed."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
spec=importlib.util.spec_from_file_location('port_driver',Path(__file__).with_name('driver.py'))
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
class WrapperTests(unittest.TestCase):
    def test_packaging(self):
        before=set(sys.modules)
        with tempfile.TemporaryDirectory() as t:
            out=d.prepare(Path(t)/'modules')
            self.assertEqual(len(list(out.glob('*.py'))),4)
            combined='\n'.join(p.read_text() for p in out.glob('*.py'))
            self.assertNotIn('/kaggle/input/arc-prize-2025',combined)
            starter=(out/'starter.py').read_text()
            self.assertNotIn('0934a4d8',starter)
            self.assertIn('queue.put(key)',starter)
            self.assertIn('score_kgmon',(out/'arc_decoder.py').read_text())
        self.assertFalse({'torch','unsloth','transformers'} & (set(sys.modules)-before))
    def test_labels_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'x.json';p.write_text(json.dumps({'a':{'train':[{}],'test':[{'input':[[1]],'output':[[2]]}]}}))
            with self.assertRaises(ValueError):d.load_challenges(p)
    def test_payload(self):
        task={'a':{'test':[{},{}]}}
        p={'a':[{'attempt_1':[[1]],'attempt_2':[[2]]}]*2}
        d.check_payload(p,task)
        p['a'][0]={'attempt_1':[[True]],'attempt_2':[[2]]}
        with self.assertRaises(ValueError):d.check_payload(p,task)
    def test_resolver_ambiguity(self):
        with tempfile.TemporaryDirectory() as t:
            for n in ('a','b'):Path(t,n).touch()
            with self.assertRaises(ValueError):d.resolve_input(None,t,'*')
    def test_anchor_guard(self):
        with self.assertRaises(ValueError):d.replace_once('x x','x','y')
    def test_mode_gates(self):
        d.validate_mode('smoke',False)
        d.validate_mode('competition',True)
        with self.assertRaises(RuntimeError):d.validate_mode('smoke',True)
        with self.assertRaises(RuntimeError):d.validate_mode('competition',False)
    def test_fixed_smoke_hash(self):
        path,tasks,m=d.smoke_input()
        self.assertEqual(list(tasks),['smoke01'])
        self.assertEqual(m['test_outputs'],2)
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            (root/'smoke-manifest.json').write_text(json.dumps(m))
            (root/m['challenges_file']).write_text('{}')
            with self.assertRaises(ValueError):d.smoke_input(root/'smoke-manifest.json')
    def test_dependency_patch(self):
        blocks,_=d.upstream_patch_blocks()
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'qwen3.py'
            p.write_text('\n'.join('\n'.join(b) for b in blocks))
            self.assertEqual(d.verify_dependency_patch(p)['required_kernel_version'],272622465)
            p.write_text(p.read_text().replace('flash_attn_func','unpatched_attention'))
            with self.assertRaises(RuntimeError):d.verify_dependency_patch(p)
    def test_missing_attempts(self):
        audit=d.attempt_coverage({'a_0':[[[1]]]}, {'a':{'test':[{},{}]}})
        self.assertEqual(audit['missing_attempt_count'],3)
        self.assertEqual(audit['missing_attempts']['a_0'],['attempt_2'])
        self.assertEqual(audit['fallback_outputs'],['a_1'])
if __name__=='__main__':unittest.main()
