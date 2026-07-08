from __future__ import annotations

import json
import logging
import os
import sys
import time
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class AppPaths:
    runtime_root: Path
    resource_root: Path


def resolve_app_paths() -> AppPaths:
    if getattr(sys, "frozen", False):
        runtime_root = Path(sys.executable).resolve().parent
        resource_root = Path(getattr(sys, "_MEIPASS", runtime_root))
        return AppPaths(runtime_root=runtime_root, resource_root=resource_root)
    project_root = Path(__file__).resolve().parent.parent
    return AppPaths(runtime_root=project_root, resource_root=project_root)


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        logging.error("JSON inválido em: %s", path)
        return {}


def load_settings(paths: AppPaths) -> dict:
    runtime_config = paths.runtime_root / "config" / "settings.json"
    bundled_config = paths.resource_root / "config" / "settings.example.json"
    return _load_json(runtime_config) or _load_json(bundled_config)


def ensure_runtime_dirs(paths: AppPaths, settings: dict) -> None:
    configured_paths = settings.get("paths", {})
    default_paths = {"downloads": "downloads", "uploads": "uploads", "logs": "logs"}
    merged_paths = {**default_paths, **configured_paths}
    for name in ("downloads", "uploads", "logs"):
        relative_path = merged_paths.get(name) or name
        (paths.runtime_root / relative_path).mkdir(parents=True, exist_ok=True)
    (paths.runtime_root / "logs" / "evidence").mkdir(parents=True, exist_ok=True)


def _write_failure_artifacts(runtime_root: Path, exc: Exception) -> None:
    evidence_dir = runtime_root / "logs" / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    traceback_file = evidence_dir / f"traceback_{timestamp}.txt"
    summary_file = evidence_dir / f"error_{timestamp}.txt"

    traceback_file.write_text(traceback.format_exc(), encoding="utf-8")
    summary_file.write_text(
        f"{type(exc).__name__}: {exc}\nPYTHONHASHSEED={os.getenv('PYTHONHASHSEED', '')}\n",
        encoding="utf-8",
    )

    try:
        import pyautogui

        screenshot_file = evidence_dir / f"screenshot_{timestamp}.png"
        pyautogui.screenshot(str(screenshot_file))
    except Exception:
        logging.warning("Não foi possível capturar screenshot de erro.", exc_info=True)


def run_with_retry(
    fn: Callable[[], None],
    runtime_root: Path,
    retries: int = 3,
    delay_seconds: float = 2.0,
) -> None:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            fn()
            return
        except Exception as exc:  # pragma: no cover - defensive runtime logic
            last_error = exc
            logging.exception("Falha na tentativa %s/%s", attempt, retries)
            if attempt < retries:
                time.sleep(delay_seconds)
    if last_error:
        _write_failure_artifacts(runtime_root, last_error)
        raise last_error
