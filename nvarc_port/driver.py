"""Packaging by default. Explicit competition rerun gate; no scientific-policy changes."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import signal
import sys
import time

ROOT = Path(__file__).resolve().parent

def verified_sources():
    hashes = json.loads((ROOT / 'SOURCE_HASHES.json').read_text())
    for name, digest in hashes.items():
        if hashlib.sha256((ROOT / 'vendor' / name).read_bytes()).hexdigest() != digest:
            raise ValueError('Vendor source hash mismatch: ' + name)
    return json.loads((ROOT / 'vendor/author-v10.ipynb').read_text())

def replace_once(source, old, new):
    if source.count(old) != 1:
        raise ValueError('Source port anchor changed: ' + old[:60])
    return source.replace(old, new, 1)

def prepare(destination):
    destination = Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=False)
    notebook = verified_sources()
    modules = {}
    for cell in notebook['cells']:
        text = ''.join(cell['source'])
        if text.startswith('%%writefile '):
            first, body = text.split('\n', 1)
            modules[first.split()[1]] = body
    for name in ('arc_solver.py', 'starter.py'):
        body = modules[name]
        begin = body.index('    if rerun_mode:\n')
        end = body.index('\n', body.index('        test_path = ', body.index('    else:\n', begin)))
        body = body[:begin] + '    test_path = os.environ["NVARC_CHALLENGES"]' + body[end:]
        if name == 'arc_solver.py':
            body = replace_once(body, 'model_name="/kaggle/input/qwen3_4b_grids15_sft139/transformers/bfloat16/1",', 'model_name=os.environ["NVARC_MODEL"],')
            body = replace_once(body, 'dir_outputs = "/kaggle/inference_outputs"', 'dir_outputs = os.environ["NVARC_OUTPUTS"]')
            marker = '        print(f"[Rank {rank}] finished {key} in {spend_time:.1f}s")'
            body = replace_once(body, marker, marker + '\n        with open(os.path.join(os.environ["NVARC_STATUS"], f"{rank}.jsonl"), "a") as status:\n            status.write(__import__("json").dumps({"task_id": key}) + "\\n")')
        else:
            subset = '        if not rerun_mode:\n            if key not in ["0934a4d8", "36a08778", "981571dc", "aa4ec2a5"]:\n                continue\n'
            body = replace_once(body, subset, '')
            body = body.replace('f"/kaggle/worker{rank-1}"', 'os.path.join(os.environ["NVARC_STATUS"], f"worker{rank-1}")')
            body = body.replace('f"/kaggle/worker{rank}"', 'os.path.join(os.environ["NVARC_STATUS"], f"worker{rank}")')
        modules[name] = body
    for name, body in modules.items():
        compile(body, name, 'exec')  # never import or execute during packaging
        (destination / name).write_text(body)
    return destination

def resolve_input(explicit, root, pattern):
    paths = [Path(explicit)] if explicit else sorted(Path(root).glob(pattern))
    paths = [p for p in paths if p.exists()]
    if len(paths) != 1:
        raise ValueError(f'Expected one explicit input for {pattern}, got {paths}')
    return paths[0].resolve()

def load_challenges(path):
    raw = json.loads(Path(path).read_text())
    if not isinstance(raw, dict) or not raw:
        raise ValueError('Empty/invalid challenges')
    for key, task in raw.items():
        if not isinstance(key, str) or not key or '_' in key or '.' in key or '/' in key:
            raise ValueError('Unsupported task id for author decoder')
        if not task.get('train') or not task.get('test'):
            raise ValueError('Missing demonstration/test pairs')
        if any('output' in example for example in task['test']):
            raise ValueError('Test targets prohibited in inference')
    return raw

def check_payload(payload, tasks):
    if set(payload) != set(tasks):
        raise ValueError('Submission task coverage mismatch')
    for key, task in tasks.items():
        if len(payload[key]) != len(task['test']):
            raise ValueError('Submission test coverage mismatch')
        for attempts in payload[key]:
            if set(attempts) != {'attempt_1', 'attempt_2'}:
                raise ValueError('Attempt keys mismatch')
            for grid in attempts.values():
                if not isinstance(grid, list) or not 1 <= len(grid) <= 30:
                    raise ValueError('Invalid grid')
                if not isinstance(grid[0], list) or not 1 <= len(grid[0]) <= 30:
                    raise ValueError('Invalid width')
                if any(not isinstance(r, list) or len(r) != len(grid[0]) or any(type(v) is not int or not 0 <= v <= 9 for v in r) for r in grid):
                    raise ValueError('Invalid grid cells')

def smoke_input(manifest_path=None):
    manifest_path = Path(manifest_path) if manifest_path else ROOT / 'smoke-manifest.json'
    manifest = json.loads(manifest_path.read_text())
    challenge = manifest_path.parent / manifest['challenges_file']
    if hashlib.sha256(challenge.read_bytes()).hexdigest() != manifest['sha256']:
        raise ValueError('Smoke challenge hash mismatch')
    tasks = load_challenges(challenge)
    if sorted(tasks) != manifest['task_ids'] or sum(len(t['test']) for t in tasks.values()) != manifest['test_outputs']:
        raise ValueError('Smoke cohort mismatch')
    return challenge.resolve(), tasks, manifest


def upstream_patch_blocks():
    verified_sources()
    notebook = json.loads((ROOT / 'vendor/dependency-v2.ipynb').read_text())
    patch = None
    for cell in notebook['cells']:
        source = ''.join(cell['source'])
        if source.startswith('patch = '):
            tree = ast.parse(source)
            patch = ast.literal_eval(tree.body[0].value).decode()
    if patch is None:
        raise ValueError('Exact dependency v2 patch not found')
    blocks, current = [], []
    for line in patch.splitlines():
        if line.startswith('+') and not line.startswith('+++'):
            current.append(line[1:].strip())
        elif current:
            blocks.append(current); current = []
    if current: blocks.append(current)
    return blocks, hashlib.sha256(patch.encode()).hexdigest()


def verify_dependency_patch(path):
    # Verify exact added-code blocks from the hash-preserved author's v2 patch.
    # This is a patch-content check, not a claim of hashing the entire dependency tree.
    blocks, patch_hash = upstream_patch_blocks()
    data = Path(path).read_bytes()
    lines = [line.strip() for line in data.decode().splitlines()]
    for block in blocks:
        if not any(lines[i:i+len(block)] == block for i in range(len(lines)-len(block)+1)):
            raise RuntimeError('Required author dependency-v2 Qwen3 patch block absent')
    return {'required_kernel_version':272622465, 'required_notebook_version':2,
            'upstream_patch_sha256':patch_hash, 'mounted_qwen3_sha256':hashlib.sha256(data).hexdigest()}


def attempt_coverage(selected, tasks):
    expected = {f'{key}_{i}' for key,t in tasks.items() for i in range(len(t['test']))}
    present = {k for k,v in selected.items() if len(v)}
    missing = {k: [f'attempt_{i+1}' for i in range(min(len(selected.get(k, [])),2),2)] for k in expected}
    return {'candidate_outputs':len(present), 'expected_outputs':len(expected),
            'fallback_outputs':sorted(expected-present),
            'missing_attempts':{k:v for k,v in sorted(missing.items()) if v},
            'missing_attempt_count':sum(map(len,missing.values()))}


def validate_mode(mode, rerun):
    if mode == 'competition' and not rerun:
        raise RuntimeError('Competition execution requires actual Kaggle rerun')
    if mode == 'smoke' and rerun:
        raise RuntimeError('Smoke mode forbidden during competition rerun')


def preflight(model, dependency):
    if sys.version_info[:2] != (3, 11):
        raise RuntimeError('Pinned source requires Python 3.11')
    if not (model / 'config.json').is_file() or not list(model.glob('*.safetensors')):
        raise RuntimeError('Missing attached model configuration/weights')
    if not (dependency / 'unsloth/models/qwen3.py').is_file():
        raise RuntimeError('Missing attached patched dependency output')
    provenance = verify_dependency_patch(dependency / 'unsloth/models/qwen3.py')
    sys.path.insert(0, str(dependency))
    import torch
    if torch.__version__.split('+')[0].split('.')[:2] != ['2', '8'] or torch.version.cuda != '12.8':
        raise RuntimeError('Require Torch 2.8 and CUDA 12.8 for bundled Flash Attention ABI')
    if torch.cuda.device_count() != 4 or any('L4' not in torch.cuda.get_device_name(i) for i in range(4)):
        raise RuntimeError('Require four NVIDIA L4 GPUs')
    import importlib.metadata
    for package, version in [('unsloth','2025.9.7'), ('unsloth_zoo','2025.9.9')]:
        if importlib.metadata.version(package) != version:
            raise RuntimeError('Pinned dependency mismatch: ' + package)
    import flash_attn
    if not flash_attn.__version__.startswith('2.8.2'):
        raise RuntimeError('Flash Attention version mismatch')
    return provenance

def execute(args):
    rerun = os.environ.get('KAGGLE_IS_COMPETITION_RERUN','').lower() in ('1','true')
    validate_mode(args.mode, rerun)
    if args.mode == 'smoke':
        if args.challenges:
            raise ValueError('Smoke uses only the fixed hash-checked challenge manifest')
        challenge, tasks, manifest = smoke_input()
        if not 1 <= args.smoke_seconds <= manifest['max_seconds']:
            raise ValueError('Smoke deadline outside declared bound')
        deadline = time.time() + args.smoke_seconds
        args.end_time = min(args.end_time, deadline) if args.end_time else deadline
        if Path(args.output).name == 'submission.json':
            raise ValueError('Smoke must not write submission.json')
    else:
        if args.end_time is None or args.end_time > time.time() + 12*3600-590:
            raise RuntimeError('First-cell deadline required')
        challenge = resolve_input(args.challenges, '/kaggle/input', '**/arc-prize-2026-arc-agi-2/arc-agi_test_challenges.json')
        if 'arc-prize-2026-arc-agi-2' not in challenge.parts or challenge.name != 'arc-agi_test_challenges.json':
            raise RuntimeError('Require current 2026 competition test challenges')
        tasks = load_challenges(challenge)
    if args.end_time <= time.time():
        raise RuntimeError('Budget exhausted before preflight')
    model = resolve_input(args.model, '/kaggle/input', '**/qwen3_4b_grids15_sft139/transformers/bfloat16/1')
    dep = resolve_input(args.dependencies, '/kaggle/usr/lib/notebooks', 'sorokin/pip_install_unsloth_flash_patch')
    dependency_provenance = preflight(model, dep)
    work = prepare(args.workdir)
    outputs, status = work/'outputs', work/'status'
    outputs.mkdir(); status.mkdir()
    env = os.environ.copy()
    env.update(NVARC_CHALLENGES=str(challenge), NVARC_MODEL=str(model), NVARC_OUTPUTS=str(outputs), NVARC_STATUS=str(status), UNSLOTH_DISABLE_STATISTICS='1', TRITON_PTXAS_PATH='/usr/local/cuda/bin/ptxas', OMP_NUM_THREADS='12', PYTHONPATH=str(dep)+os.pathsep+str(work)+os.pathsep+env.get('PYTHONPATH',''))
    remaining = args.end_time-time.time()
    if remaining <= 0:
        raise RuntimeError('Budget exhausted before workers')
    process = subprocess.Popen([sys.executable, 'starter.py', '--end-time', str(args.end_time)], cwd=work, env=env, start_new_session=True)
    try:
        returncode = process.wait(timeout=remaining)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait()
        (work/'diagnostics.json').write_text(json.dumps({'failure':'global_deadline','worker_returncode':process.returncode}))
        raise RuntimeError('Global deadline: terminated worker process group')
    completed = {json.loads(line)['task_id'] for p in status.glob('*.jsonl') for line in p.read_text().splitlines()}
    diagnostics = {'mode':args.mode, 'dependency_provenance':dependency_provenance, 'worker_returncode':returncode,'completed_tasks':len(completed),'expected_tasks':len(tasks),'missing_tasks':sorted(set(tasks)-completed)}
    (work/'diagnostics.json').write_text(json.dumps(diagnostics,indent=2))
    if returncode or completed != set(tasks):
        raise RuntimeError('Worker failure/incomplete processing; inspect diagnostics.json')
    sys.path.insert(0,str(work))
    from arc_loader import ArcDataset
    from arc_decoder import ArcDecoder
    data = ArcDataset.from_file(str(challenge))
    decoder = ArcDecoder(data.split_multi_replies(), n_guesses=2)
    decoder.load_decoded_results(str(outputs))
    selected = decoder.run_selection_algo()
    expected = {f'{key}_{i}' for key,t in tasks.items() for i in range(len(t['test']))}
    present = {k for k,v in selected.items() if len(v)}
    diagnostics.update(attempt_coverage(selected,tasks))
    (work/'diagnostics.json').write_text(json.dumps(diagnostics,indent=2))
    if not present or not present <= expected:
        raise RuntimeError('No generated candidates or unexpected decoded keys')
    payload = data.get_submission(selected)
    check_payload(payload,tasks)
    Path(args.output).write_text(json.dumps(payload))

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--mode',choices=('package','smoke','competition'),default='package')
    p.add_argument('--smoke-seconds',type=int,default=900)
    p.add_argument('--end-time',type=float)
    p.add_argument('--challenges');p.add_argument('--model');p.add_argument('--dependencies')
    p.add_argument('--workdir',default='/kaggle/working/nvarc2026-port')
    p.add_argument('--output')
    args=p.parse_args()
    args.output = args.output or ('/kaggle/working/smoke-predictions.json' if args.mode == 'smoke' else '/kaggle/working/submission.json')
    if args.mode != 'package': execute(args)
    else:
        prepare(args.workdir)
        print('Packaging only: no model, torch, Unsloth, GPU or submission invoked.')
if __name__=='__main__':main()
