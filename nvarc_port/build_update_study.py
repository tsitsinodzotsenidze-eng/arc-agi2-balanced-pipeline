"""Rebuild guarded Z/repeats and the exact completed engineering check."""
from __future__ import annotations
import ast
import base64
import hashlib
import io
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT.parent / 'evidence/zero-update-check-20261030/rendered-source-and-receipt.json'
B1_NAME = 'NVARC_2026_B1_HASH42_SUBMISSION.ipynb'
B1_SHA = '926432d561121dea7914dab459374a693c08c29dc61d1105b72905625ab190e1'
DRIVER_SHA = '1eec5bb8db719e45d2e07af80b24db9b50d2214254b79445384d4852486f5fd4'
ZERO_SHA = '7b9a5c374d04cdbc959b925c4f4e21e3ba7fd6e9459e3958d8f6fd753ca0aec9'
PROBE_SHA = 'b2c90c21f8bdb979ed1a0668e3d1dd49404bd20d4e470db04643c2e0c3760aa1'
ANCHOR = "        if name == 'arc_solver.py':\n"
ZERO_PATCH = ANCHOR + "            body = replace_once(body, 'learning_rate=5e-5,', 'learning_rate=0.0,')\n"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def source_bundle(source):
    assignment = next(n for n in ast.parse(source).body if isinstance(n, ast.Assign)
                      and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'bundle')
    return ast.literal_eval(assignment.value)

def build_zero(base_path=ROOT / B1_NAME):
    raw = base_path.read_bytes()
    if sha(raw) != B1_SHA:
        raise ValueError('B1 reference changed; review before building Z')
    nb = json.loads(raw)
    source = ''.join(nb['cells'][1]['source'])
    encoded = source_bundle(source)
    output = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(base64.b64decode(encoded))) as original:
        driver = original.read('driver.py')
        if sha(driver) != DRIVER_SHA or driver.decode().count(ANCHOR) != 1:
            raise ValueError('Unexpected B1 driver or source-port anchor')
        zero_driver = driver.decode().replace(ANCHOR, ZERO_PATCH, 1).encode()
        with zipfile.ZipFile(output, 'w') as z:
            for info in original.infolist():
                z.writestr(info, zero_driver if info.filename == 'driver.py' else original.read(info.filename))
    old = 'bundle = ' + repr(encoded)
    if source.count(old) != 1:
        raise ValueError('Expected one literal bundle')
    nb['cells'][1]['source'] = source.replace(old, 'bundle = ' + repr(base64.b64encode(output.getvalue()).decode()), 1).splitlines(True)
    nb['metadata']['nvarc_study'].update(arm='Z', learning_rate=0.0,
        driver_sha256=sha(zero_driver), reference_notebook_sha256=B1_SHA,
        note='Guarded learning-rate literal change only; full nominal training work retained.')
    return nb

def completed_probe(zero):
    evidence = json.loads(EVIDENCE.read_text())
    receipt = evidence['receipt']
    if receipt['status'] != 'PASS' or receipt['training']['global_step'] != receipt['training']['max_steps'] or receipt['training']['global_step'] <= 0:
        raise ValueError('Completed real-model check has no valid PASS receipt')
    for stage in ['after_reset', 'after_training']:
        if not all(receipt[stage][k] for k in ['all_exactly_equal', 'all_finite', 'keys_shapes_dtypes_match']):
            raise ValueError('Adapter invariant not established')
    zsource = ''.join(zero['cells'][1]['source'])
    with zipfile.ZipFile(io.BytesIO(base64.b64decode(source_bundle(zsource)))) as z:
        official = {n:z.read(n) for n in z.namelist()}
    with zipfile.ZipFile(io.BytesIO(base64.b64decode(source_bundle(evidence['cells'][1])))) as z:
        for name, data in official.items():
            if z.read(name) != data:
                raise ValueError('Executed check and official Z source differ: ' + name)
        if sha(z.read('driver.py')) != receipt['driver_sha256'] or sha(z.read('zero_update_probe_support.py')) != receipt['probe_support_sha256']:
            raise ValueError('Executed check source/hash mismatch')
    nb = json.loads(json.dumps(zero))
    for cell, text in zip(nb['cells'], evidence['cells']):
        cell['source'] = text.splitlines(True)
    nb['metadata']['nvarc_study'].update(arm='Z_ENGINEERING_CHECK', budget_seconds=600)
    return nb, evidence

def write_nb(name, nb, expected):
    data = (json.dumps(nb, indent=1)+'\n').encode()
    if sha(data) != expected:
        raise ValueError('Previously reviewed carrier bytes changed: ' + name)
    (ROOT/name).write_bytes(data)
    return {'file':name, 'sha256':sha(data)}

def main():
    zero = build_zero()
    probe, evidence = completed_probe(zero)
    z1 = write_nb('NVARC_2026_Z_ZERO_UPDATE_SUBMISSION.ipynb', zero, ZERO_SHA)
    check = write_nb('NVARC_2026_ZERO_UPDATE_CHECK.ipynb', probe, PROBE_SHA)
    (ROOT/'Z_Cell2_CodeOnly.py').write_text(''.join(zero['cells'][1]['source']))
    for prefix, data in [('NVARC_2026_B1_REPEAT_SUBMISSION.ipynb',(ROOT/B1_NAME).read_bytes()),
                         ('NVARC_2026_Z_REPEAT_SUBMISSION.ipynb',(ROOT/z1['file']).read_bytes())]:
        (ROOT/prefix).write_bytes(data)
    manifest={'order':['Z1','B1_REPEAT','Z_REPEAT'],'hash_seed':42,'zero':z1,'probe':check,
        'b1_repeat_sha256':B1_SHA,'zero_repeat_sha256':ZERO_SHA,
        'zero_cell2_sha256':sha((ROOT/'Z_Cell2_CodeOnly.py').read_bytes()),
        'zero_driver_sha256':zero['metadata']['nvarc_study']['driver_sha256'],
        'real_model_check':'PASS','check_script_version_id':evidence['script_version_id'],
        'official_submissions_performed':False}
    (ROOT/'UPDATE_STUDY_BUILD_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,sort_keys=True))

if __name__ == '__main__':
    main()
