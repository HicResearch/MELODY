# Developer Guide

## Repository layout

```
melody_wrapper/
├── pyproject.toml              # package metadata and dependencies
└── melody_wrapper/
    ├── __init__.py
    ├── cli.py                  # entry point — command dispatch
    ├── config.py               # config file loading (melody.toml)
    ├── checks.py               # pre-run enforcement checks
    ├── git_snapshot.py         # app snapshotting into a git repo
    └── sacroml_runner.py       # SACRO-ML attack subcommands
```

## Development setup

```bash
git clone <repo>
cd melody_wrapper
pip install -e .
```

`pip install -e .` registers the `melody` console script from your local checkout so
changes take effect immediately without reinstalling.

The project requires Python ≥ 3.8. On Python < 3.11 the `tomli` package is
installed automatically as a backport for TOML parsing; on 3.11+ the standard
library `tomllib` is used.

---

## Architecture

`melody` is a thin dispatch layer over three external tools:

| Tool | Role | Docs |
|------|------|------|
| [Flower (`flwr`)](https://flower.ai) | Federated learning runtime | https://flower.ai/docs |
| [flwrCrate](https://github.com/eScienceLab/flwrCrate) | Provenance capture (RO-Crate) | repo README |
| [SACRO-ML (`sacroml`)](https://github.com/AI-SDC/SACRO-ML) | Privacy attack assessment | https://ai-sdc.github.io/SACRO-ML |

### Request flow for `melody run`

```
melody run myapp/
  │
  ├─ config.py  ──  strip --config/-c, load melody.toml
  ├─ checks.py  ──  abort if FLCrateTracker not present in app source
  ├─ git_snapshot.py  ──  copy app into git repo, commit if changed
  └─ subprocess  ──  exec `flwr run myapp/` (original args unchanged)
```

### Request flow for `melody attack`

```
melody attack [target_dir] [attack.yaml]
  │
  ├─ config.py  ──  strip --config/-c, load melody.toml
  └─ sacroml_runner.py  ──  exec `sacroml run <target_dir> <attack.yaml>`
```

All other subcommands (e.g. `melody new`, `melody log`) are forwarded to `flwr`
unchanged.

---

## Module reference

### `cli.py` — entry point

`main()` is the sole entry point registered in `pyproject.toml`. It:

1. Calls `find_and_strip_config_arg` to peel off `--config`/`-c` before the
   subcommand.
2. Loads the config file if one was found or defaulted.
3. Dispatches on `args[0]` (the subcommand).

**Dispatch table:**

| `args[0]` | Handler |
|-----------|---------|
| `run` | `checks.check_flwrcrate_usage` → `git_snapshot.snapshot` → `flwr run` |
| `attack` | `sacroml_runner.run_attacks` |
| `gen-target` | `sacroml_runner.gen_target` |
| `gen-attack` | `sacroml_runner.gen_attack` |
| anything else | forwarded to `flwr` |

---

### `config.py` — config loading

**`find_and_strip_config_arg(args)`**

Scans only the *leading* flags (before the first positional / subcommand) for
`--config` / `-c`. Stops at the subcommand so that flags belonging to `flwr`
subcommands (e.g. `flwr run -c run-config.toml`) are never consumed.

Falls back to `melody.toml` in the current directory if no explicit flag is given.

**`load_config(path)`**

Opens the TOML file and returns a plain `dict`. All downstream modules receive
this dict and look up their own section (e.g. `config.get("git", {})`).

**Config file structure:**

```toml
[git]
directory = "/absolute/path/to/snapshot/repo"

[sacroml]
target_dir   = "./sacroml_target"
attack_config = "./attack.yaml"
```

---

### `checks.py` — pre-run enforcement

**`check_flwrcrate_usage(app_path)`**

Walks every `.py` file under `app_path` looking for the string `FLCrateTracker`.
Exits with a human-readable error if none is found.

This is the enforcement mechanism that ensures all runs produce RO-Crate
provenance records. To add further enforcement checks (e.g. licence headers,
required config keys), add them here and call them from `cli.py` inside the
`subcommand == "run"` block.

---

### `git_snapshot.py` — app versioning

**`resolve_app_path(flwr_args)`**

Extracts the `APP` positional from `flwr run [APP] [SUPERLINK] [OPTIONS]` by
taking the first non-flag argument after `"run"`. Defaults to `.`.

**`snapshot(flwr_args, config)`**

1. Reads `config["git"]["directory"]` for the target repo path.
2. Copies the app directory into `<git_dir>/<app_name>/`, skipping `.git`,
   `__pycache__`, `*.pyc`, `.venv`, and `venv`.
3. Stages all changes with `git add -A`.
4. Commits only if `git status --porcelain` shows a diff, using the message
   `melody snapshot <app_name>: <ISO-8601 timestamp>`.

The destination repo must already exist and be a valid git repository. `melody`
does not create it.

---

### `sacroml_runner.py` — privacy attack wrapper

**`run_attacks(args, config)`**

Resolves `target_dir` and `attack_config` from positional args first, then falls
back to `config["sacroml"]["target_dir"]` / `config["sacroml"]["attack_config"]`.
Shells out to `sacroml run <target_dir> <attack_config> [flags]`.

**`gen_target()` / `gen_attack()`**

Thin proxies to `sacroml gen-target` and `sacroml gen-attack` respectively. These
are interactive wizards that write `target.yaml` and `attack.yaml` to disk.

---

## Adding a new `melody` subcommand

1. Create a module in `melody_wrapper/` for the new behaviour.
2. Add a branch in `cli.py`:

```python
if subcommand == "my-command":
    from melody_wrapper.my_module import my_function
    sys.exit(my_function(args[1:], config))
```

3. If the subcommand should not be forwarded to `flwr`, make sure it is handled
   before the final `subprocess.run(["flwr"] + args)` fallthrough.

## Adding a new pre-run check

Add a function to `checks.py` with the signature:

```python
def check_something(app_path: Path) -> None:
    ...
    # call sys.exit(1) on failure
```

Then call it in `cli.py` inside the `subcommand == "run"` block alongside
`check_flwrcrate_usage`.

## Adding a new config section

Config is a plain `dict` passed through to every module. Add a new top-level
table to `melody.toml` and read it in your module with
`config.get("my_section", {})`. No schema registration is needed.
