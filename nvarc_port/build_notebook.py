"""Build self-contained candidate without importing or executing upstream code."""
import base64
import io
import json
from pathlib import Path
import zipfile
root=Path(__file__).resolve().parent
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED) as z:
    for name in ['driver.py','SOURCE_HASHES.json','NOTICE','LICENSE','smoke-challenges.json','smoke-manifest.json','vendor/author-v10.ipynb','vendor/dependency-v2.ipynb']:
        z.writestr(name,(root/name).read_bytes())
encoded=base64.b64encode(buf.getvalue()).decode()
first="import time\nPORT_STARTED = time.time()\nPORT_DEADLINE = PORT_STARTED + 12 * 3600 - 600\nPORT_MODE = 'package'  # Explicitly choose 'smoke' only for an authorized GPU check.\nSMOKE_SECONDS = 900\nEXPORT_SUBMISSION_PLACEHOLDER = False\n"
second=f'''# Attributed source packaging only unless Kaggle competition rerun is active.
import base64, io, os, pathlib, subprocess, sys, zipfile
bundle = {encoded!r}
port_root = pathlib.Path('/kaggle/working/nvarc2026-carrier')
port_root.mkdir(exist_ok=False)
with zipfile.ZipFile(io.BytesIO(base64.b64decode(bundle))) as archive:
    archive.extractall(port_root)
command = [sys.executable, str(port_root / 'driver.py'), '--workdir', '/kaggle/working/nvarc2026-runtime']
if os.environ.get('KAGGLE_IS_COMPETITION_RERUN', '').lower() in ('1', 'true'):
    if PORT_MODE == 'smoke': raise RuntimeError('Smoke choice prohibited in competition rerun')
    command += ['--mode', 'competition', '--end-time', str(PORT_DEADLINE)]
else:
    if PORT_MODE not in ('package','smoke'): raise ValueError('Choose package or smoke')
    command += ['--mode', PORT_MODE]
    if PORT_MODE == 'package': command += ['--inspect-inputs']
    if PORT_MODE == 'package' and EXPORT_SUBMISSION_PLACEHOLDER:
        command += ['--export-placeholder']
    if PORT_MODE == 'smoke':
        command += ['--end-time', str(min(PORT_DEADLINE, PORT_STARTED+SMOKE_SECONDS)), '--smoke-seconds', str(SMOKE_SECONDS)]
subprocess.run(command, check=True)
'''
kaggle_metadata = {
    'accelerator':'none', 'isInternetEnabled':False, 'isGpuEnabled':False,
    'language':'python', 'sourceType':'notebook', 'dockerImageVersionId':31090,
    'dataSources':[
        {'sourceType':'competition','sourceId':133469},
        {'sourceType':'kernelVersion','sourceId':272622465},
        {'sourceType':'modelInstanceVersion','sourceId':627758,
         'modelInstanceId':472720,'modelId':488596},
    ],
}
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'kaggle':kaggle_metadata},'cells':[{'cell_type':'code','execution_count':None,'metadata':{},'outputs':[],'source':s.splitlines(True)} for s in (first,second)]}
(root/'NVARC_2026_PORT_CANDIDATE.ipynb').write_text(json.dumps(nb,indent=1)+'\n')

# Separate engineering smoke artifact; never use as a competition submission.
smoke = json.loads(json.dumps(nb))
smoke['cells'][0]['source'] = first.replace("PORT_MODE = 'package'", "PORT_MODE = 'smoke'").splitlines(True)
smoke['metadata']['kaggle'].update(accelerator='nvidiaL4', isGpuEnabled=True)
(root/'NVARC_2026_SMOKE_CHECK.ipynb').write_text(json.dumps(smoke,indent=1)+'\n')

# The official carrier must save L4x4 settings and a selectable output file.
submission = json.loads(json.dumps(nb))
submission['cells'][0]['source'] = first.replace('EXPORT_SUBMISSION_PLACEHOLDER = False', 'EXPORT_SUBMISSION_PLACEHOLDER = True').splitlines(True)
submission['metadata']['kaggle'].update(accelerator='nvidiaL4', isGpuEnabled=True)
(root/'NVARC_2026_SUBMISSION_CANDIDATE.ipynb').write_text(json.dumps(submission,indent=1)+'\n')
