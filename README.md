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

- **Python 3.9** is required. 

### Setting up a virtual environment

Using `pyenv` to install the required Python version and create a virtual environment:

```bash
pyenv install -s 3.9.23
~/.pyenv/versions/3.9.23/bin/python3.9 -m venv venv
```

### Installing dependencies

Dependencies are pinned in `requirements.txt`. With the virtual environment created above:

```bash
venv/bin/pip install -r requirements.txt
venv/bin/pip install -e .
```

The `pip install -e .` step performs an editable install of this project (configured via `setup.py`), which puts the
`schema_mechanism` package on the Python path without needing to set `PYTHONPATH` manually.

### Running tests

Tests use Python's built-in `unittest` framework and live under `tests/`:

```bash
venv/bin/python -m unittest discover -s tests -v
```

A single test module or test case can be run directly, e.g.:

```bash
venv/bin/python -m unittest tests.test_schema -v
```

## Running the Multi-Armed Bandit example

`src/examples/multi_arm_bandits.py` runs the schema mechanism against a multi-armed bandit environment. There are
two ways to run it.

### Single run

Run the example directly from the project root (it loads `config/logging.conf` via a relative path, so it won't
find that file if run from elsewhere):

```bash
venv/bin/python src/examples/multi_arm_bandits.py
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
venv/bin/python src/examples/multi_arm_bandits.py -M 1.0 -M 0.5 -M 0.0 --steps 5000
```

### Experiment sweep

`scripts/run_bandit_experiment.py` sweeps a range of machine-count configurations, running the single-run script
above as a subprocess multiple times per configuration, and writes results under `local/experiments/<timestamp>/`:

```bash
venv/bin/python scripts/run_bandit_experiment.py --steps_per_run 10000 --runs_per_trial 10
```

Use this over a single run when you want aggregate results across several bandit configurations and repeated trials
rather than watching one run's behavior directly.

## References:

Drescher, G. L. (1987). A Mechanism for Early Piagetian Learning. In AAAI (pp. 290-294).

Drescher, G. L. (1991). ***Made-up minds: a constructivist approach to artificial intelligence***. MIT press.
