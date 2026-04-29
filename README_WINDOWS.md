# Como gerar dev_mode.exe no Windows

## 1. Instale Python e dependências
- Baixe e instale o Python 3.x (https://www.python.org/downloads/)
- Instale o Pillow e o PyInstaller:

```powershell
python -m pip install --upgrade pip
pip install pillow pyinstaller
```

## 2. Gere o executável
- No terminal (PowerShell ou CMD), navegue até a pasta do projeto e execute:

```powershell
pyinstaller --noconfirm --onefile --windowed --name dev_mode src/dev_mode/__main__.py
```

- O executável será criado em `dist/dev_mode.exe`.

## 3. Execute o Dev Mode

```powershell
cd dist
./dev_mode.exe
```

## 4. Observações
- Se faltar algum arquivo de fonte ou asset, copie a pasta `fonts` (ou outros assets necessários) para o mesmo diretório do `.exe`.
- O ajuste de brilho pode não funcionar em todos os hardwares Windows.
- Se aparecer "DLL load failed" ou erro de `tkinter`, instale o Python oficial e certifique-se de marcar a opção "tcl/tk and IDLE" no instalador.
- Para empacotar ícones personalizados, consulte a documentação do PyInstaller (`--icon=icone.ico`).

---

Dúvidas ou problemas? Me envie o erro para análise!
