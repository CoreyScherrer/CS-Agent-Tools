"""Configuration resolution.

Precedence, lowest to highest: built-in defaults, ``config.example.json``,
``config.local.json`` (gitignored, written by ``ma doctor``), environment
variables. Nothing about the host machine is hardcoded — every path is derived
or configured, which is what makes the repo portable to an unexamined machine.
"""

import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL_CONFIG = os.path.join(REPO_ROOT, "config.local.json")
EXAMPLE_CONFIG = os.path.join(REPO_ROOT, "config.example.json")

DEFAULTS = {
    "storage": {
        "backend": "sqlite",          # 'sqlite' | 'postgres'
        "sqlite_path": "data/memory.db",
        "postgres_dsn": "",
    },
    "identity": {
        "agent_key": "claude-code",
        "default_project": "",
    },
    "recall": {
        "token_budget": 2000,
        "max_items": 25,
        "recency_half_life_days": 30.0,
    },
    "capture": {
        "default_importance": 0.5,
    },
}

ENV_MAP = {
    "MA_BACKEND": ("storage", "backend"),
    "MA_SQLITE_PATH": ("storage", "sqlite_path"),
    "MA_POSTGRES_DSN": ("storage", "postgres_dsn"),
    "MA_AGENT_KEY": ("identity", "agent_key"),
    "MA_PROJECT": ("identity", "default_project"),
    "MA_TOKEN_BUDGET": ("recall", "token_budget"),
}


def _merge(base, overlay):
    out = dict(base)
    for key, value in (overlay or {}).items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _merge(out[key], value)
        else:
            out[key] = value
    return out


def _read_json(path):
    """Read a config file, tolerating absence and malformed content.

    A broken config file must not make the archive unusable — the caller falls
    back to defaults and the CLI surfaces the problem in `ma status`.
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def load(overrides=None):
    cfg = _merge(DEFAULTS, _read_json(EXAMPLE_CONFIG))
    cfg = _merge(cfg, _read_json(LOCAL_CONFIG))

    for env_name, (section, key) in ENV_MAP.items():
        raw = os.environ.get(env_name)
        if raw:
            cfg.setdefault(section, {})[key] = _coerce(DEFAULTS[section][key], raw)

    return _merge(cfg, overrides or {})


def _coerce(reference, raw):
    if isinstance(reference, bool):
        return raw.strip().lower() in ("1", "true", "yes", "on")
    if isinstance(reference, int) and not isinstance(reference, bool):
        try:
            return int(raw)
        except ValueError:
            return reference
    if isinstance(reference, float):
        try:
            return float(raw)
        except ValueError:
            return reference
    return raw


def save_local(cfg):
    """Persist resolved settings to the gitignored local config."""
    with open(LOCAL_CONFIG, "w", encoding="utf-8") as fh:
        json.dump(cfg, fh, indent=2, sort_keys=True)
        fh.write("\n")
    return LOCAL_CONFIG


def resolve_path(path):
    """Interpret a relative path against the repo root, not the caller's cwd."""
    expanded = os.path.expanduser(path)
    if os.path.isabs(expanded):
        return expanded
    return os.path.join(REPO_ROOT, expanded)
