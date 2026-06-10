# Troubleshooting Guide

Common issues and their solutions.

---

## Installation Issues

### `pip install` fails with "No module named setuptools"

**Solution:**
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### `streamlit` command not found after pip install

**Solution:**
Use the module invocation:
```bash
python -m streamlit run dashboard/app.py
```

Or ensure the Python environment is activated:
```bash
# Verify Python location
which python  # Linux/macOS
where python  # Windows

# Reinstall in correct environment
pip install streamlit
```

### Dependency conflict (e.g., "numpy incompatible")

**Solution:**
Create a fresh virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

---

## Trace Generation Issues

### `ModuleNotFoundError: No module named 'trace_exporter'`

**Solution:**
Ensure you're running from the project root:
```bash
cd /path/to/AIS2
python examples/minimal_system.py
```

Or add the parent directory to sys.path (already done in example files):
```python
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)
```

### Traces not saved to `traces/` directory

**Solution:**
Verify the `traces/` directory exists:
```bash
mkdir -p traces
python examples/minimal_system.py
```

Check write permissions:
```bash
ls -ld traces  # Linux/macOS
dir traces     # Windows
```

### Trace JSON is malformed or empty

**Solution:**
Check the trace export:
```bash
# Verify JSON is valid
python -m json.tool traces/minimal_trace.json

# Check file size
ls -lh traces/minimal_trace.json

# Regenerate
python examples/minimal_system.py
```

---

## Dashboard Issues

### `streamlit run` returns "No such file or directory"

**Solution:**
Run from project root:
```bash
cd /path/to/AIS2
python -m streamlit run dashboard/app.py
```

### Dashboard opens but shows blank/loading screen

**Solution:**
1. Check browser console for errors (F12 → Console)
2. Ensure trace JSON exists:
   ```bash
   ls traces/minimal_trace.json
   python examples/minimal_system.py  # Regenerate if missing
   ```
3. Restart Streamlit:
   - Press `C` in terminal to stop
   - Run again: `python -m streamlit run dashboard/app.py`

### `FileNotFoundError: traces/minimal_trace.json not found`

**Solution:**
Generate traces first:
```bash
python examples/minimal_system.py
python examples/failure_demo.py
python examples/omega_transition_demo.py
```

### Dashboard port already in use (address already in use)

**Solution:**
Use a different port:
```bash
python -m streamlit run dashboard/app.py --server.port 8502
```

Or find and kill the process using port 8501:
```bash
# Linux/macOS
lsof -i :8501 | grep LISTEN
kill -9 <PID>

# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

---

## Testing Issues

### `pytest` command not found

**Solution:**
Install dev dependencies:
```bash
pip install -e ".[dev]"
# or
pip install pytest black ruff mypy
```

### Tests fail with import errors

**Solution:**
Ensure you're in the project root and pytest can find modules:
```bash
cd /path/to/AIS2
pytest tests/ -v
```

If issues persist:
```bash
pip install -e .  # Install package in editable mode
pytest tests/ -v
```

### Determinism test fails (traces differ)

**Solution:**
This indicates non-determinism. Debug:
```bash
# Run twice and diff
python examples/minimal_system.py
cp traces/minimal_trace.json traces/minimal_trace_run1.json

python examples/minimal_system.py
cp traces/minimal_trace.json traces/minimal_trace_run2.json

# Compare
diff traces/minimal_trace_run1.json traces/minimal_trace_run2.json

# Or use jq for semantic diff
jq '.[] | {event_type, timestamp, payload}' traces/minimal_trace_run1.json > /tmp/run1.json
jq '.[] | {event_type, timestamp, payload}' traces/minimal_trace_run2.json > /tmp/run2.json
diff /tmp/run1.json /tmp/run2.json
```

Check for:
- Non-deterministic timestamp generation (use fixed clocks in tests)
- Dict iteration order (use OrderedDict or Python 3.7+ insertion order)
- Random number generation (set seed explicitly)

---

## Docker Issues

### `docker: command not found`

**Solution:**
Install Docker from https://www.docker.com/products/docker-desktop

Verify installation:
```bash
docker --version
docker run hello-world
```

### Docker build fails with "base image not found"

**Solution:**
Ensure internet connection and Docker daemon running:
```bash
docker pull python:3.11-slim
docker build -f docker/Dockerfile -t ais2 .
```

### Container build succeeds but run fails

**Solution:**
Check container logs:
```bash
docker run --rm ais2 python examples/minimal_system.py
# or with verbose output
docker run --rm -it ais2 bash
```

### Docker container too large

**Solution:**
The Python 3.11-slim base is ~150MB. To reduce size further, use Alpine or distroless, but note that compatibility may be affected:
```dockerfile
FROM python:3.11-alpine
```

---

## Code Quality Issues

### `black` or `ruff` fails on your code

**Solution:**
Auto-format with black:
```bash
black .
```

Fix common ruff issues:
```bash
ruff check . --fix
```

Review remaining issues:
```bash
ruff check .
```

### `mypy` type checking fails

**Solution:**
Check type errors:
```bash
mypy phase_c validator trace_exporter --show-error-codes
```

Fix common issues:
- Add type hints to function parameters/returns
- Use `Optional[T]` instead of `T | None` (if Python < 3.10)
- Suppress false positives with `# type: ignore`

---

## Git & GitHub Issues

### `git clone` fails

**Solution:**
1. Verify internet connection
2. Check SSH or HTTPS access:
   ```bash
   # HTTPS (no SSH key needed)
   git clone https://github.com/Dedoc-9/AIS2.git
   
   # SSH (requires SSH key)
   git clone git@github.com:Dedoc-9/AIS2.git
   ```
3. If using SSH, ensure key is added:
   ```bash
   ssh-add ~/.ssh/id_rsa
   ssh -T git@github.com  # Test connection
   ```

### `git commit` fails with GPG signature error

**Solution:**
Either sign commits (recommended) or disable signing:
```bash
# Disable signing for this repo
git config --local commit.gpgsign false

# Or configure signing properly
git config --global user.signingkey <GPG_KEY_ID>
```

### Pull request CI checks fail

**Solution:**
Run locally before pushing:
```bash
# Run all checks
pytest tests/ -v
black --check .
ruff check .
mypy phase_c validator trace_exporter --ignore-missing-imports

# Run determinism check
python examples/minimal_system.py
python examples/minimal_system.py
# (verify traces are identical)
```

---

## Performance Issues

### Trace generation is very slow

**Solution:**
Profile the code:
```bash
python -m cProfile -s cumtime examples/minimal_system.py
```

Common bottlenecks:
- Large payloads in events → reduce size
- Serialization overhead → optimize JSON serialization
- Type checking → consider lazy validation

### Dashboard is slow to load

**Solution:**
1. Check trace file size:
   ```bash
   ls -lh traces/minimal_trace.json
   ```
2. If trace is large (>10MB), consider compressing or filtering
3. Optimize Streamlit caching (already in place)

---

## System Integrity Issues

### Invariants I1–I5 fail verification

**Solution:**
This indicates a violation of system guarantees. Run the invariant test suite:
```bash
pytest tests/invariants/ -v
```

Check that:
- TraceEvent objects are frozen (I1)
- TraceLog is append-only (I2)
- UI has no reverse edges to system (I3)
- Ω-domain access is type-rejected (I4)
- State transitions are irreversible (I5)

If failures persist, open a bug report with full output.

### Type safety violation (Ω-domain leaks)

**Solution:**
Verify OmegaProjectionPolicy is used:
```python
from phase_c.projection import OmegaProjectionPolicy

policy = OmegaProjectionPolicy()
# Should raise TypeError on Observation input
```

Check for semantic leakage in:
- `phase_c/projection.py` — projection policy
- `examples/omega_transition_demo.py` — expected failures
- `validator/validator.py` — F_Ω validators

---

## Getting Help

If you encounter an issue not listed here:

1. **Check documentation**:
   - README.md
   - AIS2_USER_GUIDE.md
   - CONTRIBUTING.md

2. **Search GitHub Issues**: https://github.com/Dedoc-9/AIS2/issues

3. **Open a new issue** with:
   - Error message or symptoms
   - Steps to reproduce
   - Environment (Python version, OS, installation method)
   - Output of relevant commands

4. **Email** bigdilly95@gmail.com for urgent issues

---

**Last Updated**: 2026-06-09 | **Status**: Submission-Ready
