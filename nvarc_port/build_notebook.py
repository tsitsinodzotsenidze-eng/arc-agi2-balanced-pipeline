"""Build self-contained candidate without importing or executing upstream code."""
import base64
import io
import json
from pathlib import Path
import zipfile
root=Path(__file__).resolve().parent
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED) as z:
    for name in ['driver.py','SOURCE_HASHES.json','NOTICE','LICENSE','vendor/author-v10.ipynb','vendor/dependency-v2.ipynb']:
        z.writestr(name,(root/name).read_bytes())
encoded=base64.b64encode(buf.getvalue()).decode()
first='import time\nPORT_DEADLINE = time.time() + 12 * 3600 - 600\n'
second=f'''# Attributed source packaging only unless Kaggle competition rerun is active.
import base64, io, os, pathlib, subprocess, sys, zipfile
bundle = {encoded!r}
port_root = pathlib.Path('/kaggle/working/nvarc2026-carrier')
port_root.mkdir(exist_ok=False)
with zipfile.ZipFile(io.BytesIO(base64.b64decode(bundle))) as archive:
    archive.extractall(port_root)
command = [sys.executable, str(port_root / 'driver.py'), '--workdir', '/kaggle/working/nvarc2026-runtime']
if os.environ.get('KAGGLE_IS_COMPETITION_RERUN', '').lower() in ('1', 'true'):
    command += ['--execute', '--end-time', str(PORT_DEADLINE)]
subprocess.run(command, check=True)
'''
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'kaggle':{'isInternetEnabled':False,'isGpuEnabled':False}},'cells':[{'cell_type':'code','execution_count':None,'metadata':{},'outputs':[],'source':s.splitlines(True)} for s in (first,second)]}
(root/'NVARC_2026_PORT_CANDIDATE.ipynb').write_text(json.dumps(nb,indent=1)+'\n')
