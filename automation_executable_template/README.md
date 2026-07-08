# Automation Executable Template (Windows)

Template para automações complexas (Excel + web automation) com empacotamento **PyInstaller one-folder**.

## Estrutura

- `main.py`: ponto de entrada.
- `app/`: lógica principal e utilitários.
- `automation/`: ações de navegador/site interno.
- `excel/`: validação e leitura de planilhas.
- `config/`: configuração externa.
- `assets/`: arquivos auxiliares.
- `downloads/`, `uploads/`, `logs/`: criadas/usar em runtime.
- `build.spec`: configuração do PyInstaller.
- `scripts/`: scripts de build e pacote zip.

## Pré-requisitos

- Windows 64-bit
- Python 3.12+
- Dependências instaladas a partir do `requirements.lock`

## Execução local

```powershell
python main.py --check
python main.py
```

## Build do executável (one-folder)

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_windows.ps1
```

Saída esperada: `dist/TaskAutomationApp/TaskAutomationApp.exe`

## Pacote para distribuição

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\package_release.ps1 -Version v1.0.0
```

Saída esperada: `release/TaskAutomationApp-v1.0.0.zip`

## Compartilhar lógica sem enviar código-fonte

Gere um formulário preenchível:

```powershell
python .\scripts\generate_logic_intake.py
```

Ou defina o caminho de saída:

```powershell
python .\scripts\generate_logic_intake.py --output C:\temp\logic_intake.md
```

Template base: `templates/logic_intake_template.md`

## Notas importantes de navegador

- **Selenium**: use Selenium Manager (sem `chromedriver.exe` manual).
- **Playwright**: use browser gerenciado pelo Playwright.
- Evite manter pasta fixa de driver do Chrome.

## Checklist de homologação

1. Rodar em 3 máquinas diferentes da equipe.
2. Validar login/acesso ao site interno.
3. Validar fluxo de upload/download.
4. Validar leitura e gravação de Excel.
5. Validar logs e captura de erro.
