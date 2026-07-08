# Automation Executable Template (Windows)

Template para automações complexas (Excel + web automation) com empacotamento **PyInstaller one-folder** + instalador **Inno Setup**.

## Estrutura

- `main.py`: ponto de entrada.
- `app/runtime.py`: detecção de modo congelado, leitura de config e runtime.
- `automation/`: ações de navegador/site interno.
- `excel/`: validação e leitura de planilhas.
- `config/`: configuração externa (`settings.json` no cliente).
- `assets/`: arquivos auxiliares.
- `downloads/`, `uploads/`, `logs/`: pastas de runtime.
- `build.spec`: configuração do PyInstaller.
- `scripts/`: build, pacote zip, checksum e instalador.

## Arquitetura recomendada

1. Escolha **um motor principal** de browser (Selenium ou Playwright).
2. Use PyAutoGUI só como último recurso.
3. Deixe URLs, timeout, flags e paths na configuração externa.
4. Mantenha logs/evidências fora do código.

## Execução local

```powershell
python main.py --check
python main.py
```

## Build reproduzível do executável (one-folder)

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_windows.ps1 -BuildEpoch 1751932800
```

- `PYTHONHASHSEED=0`
- `SOURCE_DATE_EPOCH` fixo
- Saída: `dist/TaskAutomationApp/TaskAutomationApp.exe`

## Empacotamento e instalador

1) ZIP + checksum:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\package_release.ps1 -Version v1.0.0
```

Saídas:
- `release/TaskAutomationApp-v1.0.0.zip`
- `release/TaskAutomationApp-v1.0.0.zip.sha256`

2) Instalador único (Inno Setup):

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_installer.ps1 -Version v1.0.0
```

Saída:
- `release/TaskAutomationApp-v1.0.0-setup.exe`

## Conteúdo obrigatório do pacote

- Executável principal.
- Configuração externa (`config/settings.json`).
- Assets necessários.
- Pastas de runtime criadas no primeiro uso.
- Logs e evidências de erro (traceback + screenshot quando possível).

## Browser/driver (durabilidade)

- **Selenium**: use Selenium Manager (sem `chromedriver` fixo manual).
- **Playwright**: use browser gerenciado pelo próprio Playwright.

## Checklist de homologação (mínimo)

1. Instalação limpa em 3 máquinas reais.
2. Login/site interno.
3. Upload/download.
4. Leitura/escrita Excel.
5. Mensagens de erro amigáveis.
6. Logs completos para suporte.

## Operação

- Versionamento semântico (v1.0.0, v1.0.1...).
- Release note curto por versão.
- Manter última versão estável para rollback.
- Novo instalador substitui versão anterior.
- Distribuição interna em canal único.
