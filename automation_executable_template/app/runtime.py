from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Callable


def ensure_runtime_dirs(base_dir: Path) -> None:
    for name in ("downloads", "uploads", "logs"):
        (base_dir / name).mkdir(parents=True, exist_ok=True)


def run_with_retry(fn: Callable[[], None], retries: int = 3, delay_seconds: float = 2.0) -> None:
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
        raise last_error
