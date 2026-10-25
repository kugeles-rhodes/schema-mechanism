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

- **Python 3.12 or later** is required. Python 3.12, 3.13, and 3.14 are tested in CI on Linux, macOS, and Windows;
  3.13 is used for development (pinned in `.python-version`).
- **[uv](https://docs.astral.sh/uv/)** (0.12.18 or later) manages the Python version, the virtual environment, and
  the dependencies. You don't need to install Python separately; uv downloads the right version if it's missing.
- macOS (12+ on Apple Silicon, 10.15+ on Intel), Linux (x86_64 and aarch64), and Windows (x86_64) are all supported.
  There are no compiled components in this project, and every locked dependency ships prebuilt wheels for these
  platforms, with one exception: on Linux, the keyboard-input library (`pynput`) depends on `evdev`, which is built
  from source during installation and needs a C compiler and the C library headers (e.g. the `build-essential`
  package on Debian/Ubuntu).

### Installing uv

macOS and Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

uv can also be installed with Homebrew (`brew install uv`), `pipx install uv`, or `pip install uv`; see the
[installation guide](https://docs.astral.sh/uv/getting-started/installation/) for details.

### Setting up the project

From the project root:

```bash
uv sync
```

This creates a virtual environment in `.venv/` using the Python version from `.python-version`, installs the exact
dependency versions recorded in `uv.lock` (including the development tools in the `dev` dependency group, such as
`coverage`), and installs this project in editable mode, so changes under `src/` take effect without reinstalling.
`pyproject.toml` declares the compatible dependency version ranges; `uv.lock` records the exact versions, resolved for
every supported platform and Python version.

### Running commands

Prefix commands with `uv run`, which runs them in the project's environment (and re-syncs it first if `pyproject.toml`
or `uv.lock` changed):

```bash
uv run python -m unittest discover -s tests -v
```

Alternatively, activate the environment once per shell, after which `python` refers to `.venv`'s interpreter:

```bash
source .venv/bin/activate        # macOS and Linux (bash/zsh)
```

```powershell
.venv\Scripts\Activate.ps1       # Windows PowerShell (or .venv\Scripts\activate.bat in cmd)
```

If PowerShell refuses to run `Activate.ps1` because of its execution policy, either use the `activate.bat` form or
allow local scripts for the current user with `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.
`deactivate` restores the original shell environment.

**The commands in the rest of this README assume an activated environment.** Without activating, prefix them with
`uv run`, e.g. `python src/examples/multi_arm_bandits.py` becomes `uv run python src/examples/multi_arm_bandits.py`.

### Managing dependencies

```bash
uv add <package>          # add a runtime dependency (updates pyproject.toml and uv.lock)
uv add --dev <package>    # add a development-only dependency
uv lock --upgrade         # upgrade all locked versions within the ranges in pyproject.toml
```

Commit `pyproject.toml` and `uv.lock` together. CI installs with `uv sync --locked`, which fails if `uv.lock` is out of
date with `pyproject.toml`.

### Installing without uv

The project is a standard `pyproject.toml` package, so pip can install it into any Python 3.12+ environment:

```bash
pip install -e .          # or `pip install .` for a non-editable install
```

pip installs the newest dependency versions allowed by the ranges in `pyproject.toml`, not the exact versions in
`uv.lock`, and doesn't install the `dev` dependency group.

### Running tests

Tests use Python's built-in `unittest` framework and live under `tests/`:

```bash
python -m unittest discover -s tests -v
```

A single test module or test case can be run directly, e.g.:

```bash
python -m unittest tests.test_schema -v
```

With coverage (configured in `.coveragerc` to measure `src/schema_mechanism` only):

```bash
coverage run -m unittest discover -s tests && coverage report
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

One listener is shared by all episodes in a run. For non-interactive runs, pass `--no_keyboard` to skip the listener
entirely. It's skipped automatically with `--optimize`, and the experiment sweep passes `--no_keyboard` to every run.

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
