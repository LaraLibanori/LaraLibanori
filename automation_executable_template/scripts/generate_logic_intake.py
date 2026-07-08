from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera um arquivo preenchível para mapear a lógica do robô."
    )
    parser.add_argument(
        "--output",
        help="Caminho de saída do arquivo markdown. Se omitido, usa a pasta atual.",
    )
    return parser.parse_args()


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    template_path = script_dir.parent / "templates" / "logic_intake_template.md"
    if not template_path.exists():
        raise SystemExit(f"Template não encontrado: {template_path}")

    content = template_path.read_text(encoding="utf-8")

    args = parse_args()
    if args.output:
        output_path = Path(args.output).expanduser().resolve()
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path.cwd() / f"logic_intake_{timestamp}.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"Arquivo gerado: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
