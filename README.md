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

## References:

Drescher, G. L. (1987). A Mechanism for Early Piagetian Learning. In AAAI (pp. 290-294).

Drescher, G. L. (1991). ***Made-up minds: a constructivist approach to artificial intelligence***. MIT press.
