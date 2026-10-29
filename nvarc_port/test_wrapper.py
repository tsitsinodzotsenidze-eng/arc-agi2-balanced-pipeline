"""CPU-only tests: upstream code is parsed/compiled, never imported/executed."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace
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
    def test_input_inspection_metadata_only(self):
        before=set(sys.modules)
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            dep=root/'mounted'
            source=dep/'unsloth/models/qwen3.py';source.parent.mkdir(parents=True)
            blocks,_=d.upstream_patch_blocks()
            source.write_text('\n'.join('\n'.join(b) for b in blocks))
            metadata=dep/'torch-2.8.0.dist-info';metadata.mkdir()
            (metadata/'METADATA').write_text('Metadata-Version: 2.1\nName: torch\nVersion: 2.8.0\n')
            model=root/'models/qwen3_4b_grids15_sft139/transformers/bfloat16/1'
            model.mkdir(parents=True);(model/'config.json').write_text('{}')
            report=d.inspect_inputs([root])
            self.assertTrue(report['dependency_candidates'][0]['patch_verified'])
            self.assertEqual(report['dependency_candidates'][0]['package_versions'],[{'name':'torch','version':'2.8.0'}])
            self.assertEqual(report['model_config_parents'],[str(model.resolve())])
        self.assertFalse({'torch','unsloth','transformers'} & (set(sys.modules)-before))
    def test_placeholder_multitest_and_provenance(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);folder=root/'arc-prize-2026-arc-agi-2';folder.mkdir()
            challenge=folder/'arc-agi_test_challenges.json'
            tasks={'b':{'train':[{'input':[[1]],'output':[[1]]}], 'test':[{'input':[[2]]},{'input':[[3]]}]},
                   'a':{'train':[{'input':[[1]],'output':[[1]]}], 'test':[{'input':[[4]]}]}}
            challenge.write_text(json.dumps(tasks));output=root/'submission.json'
            with patch.dict(d.os.environ,{'KAGGLE_IS_COMPETITION_RERUN':''}):
                receipt=d.export_placeholder(challenge,output)
            payload=json.loads(output.read_text());d.check_payload(payload,tasks)
            self.assertEqual(len(payload['b']),2)
            self.assertTrue(receipt['packaging_placeholder'])
            self.assertEqual(receipt['test_outputs'],3)
            self.assertTrue(d.placeholder_receipt_path(output).is_file())
            with self.assertRaises(RuntimeError):d.export_placeholder(challenge,output,rerun=True)
            tasks['b']['test'][0]['output']=[[2]];challenge.write_text(json.dumps(tasks))
            with self.assertRaises(ValueError):d.export_placeholder(challenge,root/'other.json')
            self.assertFalse((root/'other.json').exists())
    def test_failed_competition_clears_stale_output_before_preflight(self):
        with tempfile.TemporaryDirectory() as t:
            output=Path(t)/'submission.json';output.write_text('{}')
            receipt=d.placeholder_receipt_path(output);receipt.write_text('{}')
            args=SimpleNamespace(mode='competition',output=str(output),end_time=d.time.time()+100,challenges=None)
            with patch.dict(d.os.environ,{'KAGGLE_IS_COMPETITION_RERUN':'true'}):
                with patch.object(d,'resolve_input',side_effect=ValueError('missing mount')):
                    with self.assertRaises(ValueError):d.execute(args)
            self.assertFalse(output.exists());self.assertFalse(receipt.exists())
    def test_atomic_json_replaces(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'result.json';p.write_text('old')
            d.atomic_json(p,{'ok':True})
            self.assertEqual(json.loads(p.read_text()),{'ok':True})
            self.assertEqual(list(Path(t).iterdir()),[p])
if __name__=='__main__':unittest.main()
