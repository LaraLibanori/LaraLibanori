from __future__ import annotations

import argparse
import logging
from pathlib import Path

from app.runtime import ensure_runtime_dirs, run_with_retry
from excel.validator import validate_input_headers


def setup_logging(base_dir: Path) -> None:
    logs_dir = base_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(logs_dir / "automation.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def health_check(base_dir: Path) -> int:
    required = ["downloads", "uploads", "logs", "config", "assets"]
    missing = [name for name in required if not (base_dir / name).exists()]
    if missing:
        logging.error("Pastas ausentes: %s", ", ".join(missing))
        return 1
    logging.info("Check OK: estrutura mínima encontrada.")
    return 0


def run_pipeline(base_dir: Path) -> int:
    input_file = base_dir / "assets" / "input.xlsx"
    if input_file.exists():
        valid, message = validate_input_headers(
            input_file,
            required_headers=["id", "nome", "status"],
        )
        if not valid:
            logging.error("Excel inválido: %s", message)
            return 1
    else:
        logging.info("Arquivo Excel de entrada não encontrado (template).")

    def _workflow() -> None:
        logging.info("Executando fluxo principal (template).")
        # Substituir por integração real com Selenium/Playwright/PyAutoGUI.

    run_with_retry(_workflow, retries=3)
    logging.info("Fluxo concluído.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Task Automation App")
    parser.add_argument("--check", action="store_true", help="Valida estrutura e encerra.")
    return parser.parse_args()


def main() -> int:
    base_dir = Path(__file__).resolve().parent
    setup_logging(base_dir)
    ensure_runtime_dirs(base_dir)
    args = parse_args()
    if args.check:
        return health_check(base_dir)
    return run_pipeline(base_dir)


if __name__ == "__main__":
    raise SystemExit(main())
