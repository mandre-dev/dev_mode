# Dev Mode

Automatize o ambiente de desenvolvedor com um clique!

## Funcionalidades

- Abre o VS Code
- Abre uma playlist de música no navegador
- Diminui o brilho do monitor em 10%
- Atalho com ícone personalizado

## Como usar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/mandre-dev/dev_mode.git
   cd dev_mode
   ```
2. **(Linux) Torne o atalho executável:**
   ```bash
   chmod +x dev_mode.desktop
   ```
3. **(Linux) Dê dois cliques no arquivo `dev_mode.desktop` para ativar o modo desenvolvedor.**
   - O ícone será exibido automaticamente se o arquivo `dev_mode_icon.png` estiver na mesma pasta.
   - Se necessário, marque como confiável ("Permitir Lançamento").

4. **(Windows) Execute o `dev_mode.bat`**
   - É necessário ter Python instalado.
   - Para ajuste de brilho, instale a biblioteca:
     ```bash
     pip install screen-brightness-control
     ```

## Estrutura do projeto

```
dev_mode/
├── dev_mode.py           # Script principal
├── dev_mode.desktop      # Atalho para Linux
├── dev_mode.bat          # Atalho para Windows
├── dev_mode_icon.png     # Ícone personalizado
```

## Observações

- O caminho do ícone no .desktop é relativo, então mantenha o ícone na mesma pasta do atalho.
- No Linux, o ajuste de brilho usa `xrandr` (deve estar instalado).
- No Windows, o ajuste de brilho usa a biblioteca `screen-brightness-control`.

---

Repositório oficial: https://github.com/mandre-dev/dev_mode.git
