## Dev_Mode

App desktop simples para aplicar um preset de desenvolvimento:
- abrir uma IDE
- abrir música/playlist
- ajustar brilho (quando suportado)

### Rodar (modo simples)

```bash
python3 run_dev_mode.py
```

### Rodar como pacote (recomendado)

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
python -m dev_mode
```

Ou via script instalado:

```bash
dev-mode
```

