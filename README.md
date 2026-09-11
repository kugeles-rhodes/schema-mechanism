# Modified Drescher's Schema Mechanism (Python Version)

A Python implementation of Drescher's Schema Mechanism, a constructivist-AI learning architecture originally
described in *Made-up Minds* (Drescher, 1991). The system learns "schemas" (context/action/result triples) from an
agent's interaction with an environment, discovers reliable action-outcome predictions, and chains them together to
pursue goals.

This is not a literal reimplementation of the original algorithm — it deliberately deviates in a few areas, such as
using reinforcement-learning-style eligibility traces for delegated value (instead of Drescher's undiscounted
forward-chaining broadcast), pluggable statistical tests for item correlation, and epsilon-greedy exploration in
place of Drescher's habituation/hysteresis scheme.

## Getting Started

### Requirements

- **Python 3.9** is required (3.10 and later will not work).
- macOS, Linux, and Windows are all supported. There are no compiled components in this project, and every pinned
  dependency ships prebuilt wheels for Python 3.9 on all three platforms.

### Setting up a virtual environment

**macOS and Linux** — using `pyenv` to install the required Python version, then creating the virtual environment
in the project root:

```bash
pyenv install -s 3.9.23
~/.pyenv/versions/3.9.23/bin/python3.9 -m venv venv
```

**Windows** — install Python 3.9 from [python.org](https://www.python.org/downloads/release/python-3913/) (or with
`pyenv-win`), then use the `py` launcher to select it:

```powershell
py -3.9 -m venv venv
```

### Activating the virtual environment

From the project root, on macOS or Linux (`bash`/`zsh`):

```bash
source venv/bin/activate
```

On Windows, the activation script lives under `venv\Scripts` instead:

```bat
venv\Scripts\activate.bat
```

```powershell
venv\Scripts\Activate.ps1
```

If PowerShell refuses to run `Activate.ps1` because of its execution policy, either use the `activate.bat` form
above or allow local scripts for the current user with
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.

Once activated, `python` and `pip` resolve to the virtual environment's copies on every platform, and `deactivate`
restores the original shell environment.

**Every command in the rest of this README assumes an activated virtual environment.** To run one without
activating, prefix it with `venv/bin/` on macOS and Linux, or `venv\Scripts\` on Windows. For example,
`python -m unittest discover -s tests -v` becomes `venv/bin/python -m unittest discover -s tests -v` or
`venv\Scripts\python -m unittest discover -s tests -v`.

### Installing dependencies

Dependencies are pinned in `requirements.txt`. Activate the virtual environment created above, then install:

```bash
pip install -r requirements.txt
pip install -e .
```

The `pip install -e .` step performs an editable install of this project (configured via `setup.py`), which puts the
`schema_mechanism` package on the Python path without needing to set `PYTHONPATH` manually.

### Running tests

Tests use Python's built-in `unittest` framework and live under `tests/`:

```bash
python -m unittest discover -s tests -v
```

A single test module or test case can be run directly, e.g.:

```bash
python -m unittest tests.test_schema -v
```

## Running the Multi-Armed Bandit example

`src/examples/multi_arm_bandits.py` runs the schema mechanism against a multi-armed bandit environment. There are
two ways to run it.

### Single run

Run the example from the project root on any platform (it loads `config/logging.conf` via a relative path, so it
won't find that file if run from elsewhere):

```bash
python src/examples/multi_arm_bandits.py
```

This builds a bandit environment with 16 machines with random win probabilities and runs one 500-step episode by
default. Useful options:

| Flag | Purpose |
|---|---|
| `--n_machines N` | number of bandit machines with random win probabilities (default 16) |
| `-M P` (repeatable) | define a specific machine with win probability `P`, e.g. `-M 0.75 -M 0.25`; overrides `--n_machines`/randomization |
| `--steps N` | time steps per episode (default 500) |
| `--episodes N` | number of episodes (default 1) |
| `--greedy` | use a greedy (exploit-only) schema selection strategy instead of the default epsilon-greedy strategy |
| `--save_path FILE` / `--save_frequency N` | periodically checkpoint the learned schema mechanism |
| `--load_path FILE` | resume from a previously saved schema mechanism instead of starting fresh |
| `--optimize` | run an Optuna hyperparameter-optimization study instead of a normal episode (see `--optimizer_*` flags for study configuration) |

Example:

```bash
python src/examples/multi_arm_bandits.py -M 1.0 -M 0.5 -M 0.0 --steps 5000
```

### Interactive controls

While an example is running, `pynput` listens for global key presses: space pauses and resumes the run, and `Esc`
requests a stop. This listener needs OS-level input access, which differs by platform:

- **macOS** — grant the terminal application Accessibility and Input Monitoring permission under System Settings >
  Privacy & Security. Without it, the pause and stop keys have no effect, and `pynput` may log a warning that the
  process is not trusted.
- **Linux** — an X11 display is required, so `DISPLAY` must be set. Under a headless session or a strict Wayland
  compositor, the pause and stop keys have no effect.
- **Windows** — no additional configuration is required.

The run itself proceeds normally on all three platforms whether or not the listener can read key presses; only the
pause and stop keys are affected.

### Experiment sweep

`scripts/run_bandit_experiment.py` sweeps a range of machine-count configurations, running the single-run script
above as a subprocess multiple times per configuration, and writes results under `local/experiments/<timestamp>/`:

```bash
python scripts/run_bandit_experiment.py --steps_per_run 10000 --runs_per_trial 10
```

Subprocesses are launched with the same interpreter that runs the script, so the sweep works identically on macOS,
Linux, and Windows.

Use this over a single run when you want aggregate results across several bandit configurations and repeated trials
rather than watching one run's behavior directly.

## References:

Drescher, G. L. (1987). A Mechanism for Early Piagetian Learning. In AAAI (pp. 290-294).

Drescher, G. L. (1991). ***Made-up minds: a constructivist approach to artificial intelligence***. MIT press.
