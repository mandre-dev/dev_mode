# Dev_Mode

Aplicativo desktop para aplicar presets de desenvolvimento com um único clique. Automatize sua rotina de trabalho abrindo sua IDE favorita, iniciando sua playlist e ajustando o brilho do monitor — tudo de forma centralizada e visualmente customizada.

---

## Funcionalidades

- **Presets de Desenvolvimento**: Crie, edite, exclua e aplique presets que combinam IDE, playlist e brilho do monitor.
- **Detecção Automática de IDEs**: Detecta automaticamente mais de 30 IDEs instaladas no sistema (VS Code, Cursor, Windsurf, Zed, JetBrains suite, Sublime Text, Neovim, etc.).
- **Detecção de Apps de Música**: Identifica players de música instalados (Spotify, Rhythmbox, Audacious, etc.) e permite uso de URLs customizadas.
- **Controle de Brilho**: Ajusta o brilho do monitor via `xrandr` (Linux/X11) ou PowerShell/WMI (Windows).
- **Interface Customizada**: UI estilizada com fontes TTF customizadas (Press Start 2P, JetBrains Mono), animações de hover suaves, tooltips e botões com sombra.
- **Persistência Local**: Presets são salvos em JSON no diretório home do usuário (`~/.dev_mode_presets.json`).

---

## Tecnologias Utilizadas

### Python 3.10+

Linguagem principal do projeto. Todo o aplicativo é escrito em Python puro, aproveitando a biblioteca padrão e módulos internos para criar uma aplicação desktop completa sem dependências pesadas de GUI externas.

### tkinter

Framework GUI nativo do Python, utilizado para construir toda a interface do usuário:

- **Janela principal** (`tk.Tk`) com dimensões e cores customizadas.
- **Frames** (`tk.Frame`) para organização de layout.
- **Comboboxes** (`ttk.Combobox`) para seleção de IDEs, apps de música e presets.
- **Canvas** (`tk.Canvas`) para renderização de botões customizados com sombra de texto.
- **Labels** (`tk.Label`) exibindo imagens renderizadas via PIL para texto com fontes customizadas.
- **Scale** (`tk.Scale`) para controle deslizante de brilho do monitor.
- **Sistema de eventos** (`bind`) para animações de hover e tooltips.

### Pillow (PIL Fork)

Biblioteca de processamento de imagens, utilizada extensivamente para:

- **Renderização de texto customizado**: Como o tkinter não suporta nativamente fontes TTF externas de forma consistente, o Pillow renderiza textos em imagens PNG que são exibidas em Labels.
- **Fontes aplicadas**: Press Start 2P (título), JetBrains Mono ExtraBold (labels e banners).
- **Conversão para PhotoImage**: Imagens PIL são convertidas para `tkinter.PhotoImage` via codificação base64, eliminando a necessidade do `ImageTk`.
- **Manipulação de ícones**: Carregamento e redimensionamento proporcional de ícones PNG da pasta `assets/`.
- **Criação de elementos gráficos**: Geração dinâmica de underlines e elementos visuais customizados.

### setuptools

Sistema de build e empacotamento configurado via `pyproject.toml`:

- Define o pacote `dev-mode` com instalação editável (`pip install -e .`).
- Registra o entry point `dev-mode` no PATH do usuário após instalação.
- Organiza o código fonte no diretório `src/` seguindo a estrutura moderna de pacotes Python.

### JSON

Formato de serialização utilizado para persistência dos presets:

- Estrutura simples e legível: `{ "name", "ide", "playlist", "brightness" }`.
- Armazenado em `~/.dev_mode_presets.json` para manter dados entre execuções.
- Leitura e escrita via `json.load`/`json.dump` com encoding UTF-8.

### subprocess

Módulo da biblioteca padrão para execução de processos externos:

- **Abertura de IDEs**: `subprocess.Popen` para lançar editores de código em segundo plano.
- **Abertura de players de música**: Execução de apps de música detectados.
- **Controle de brilho no Linux**: Chamada ao comando `xrandr --brightness` para displays X11.
- **Controle de brilho no Windows**: Execução de script PowerShell via `powershell.exe` com WMI (`WmiMonitorBrightnessMethods`).

### shutil

Utilizado para verificação de disponibilidade de comandos no PATH do sistema:

- `shutil.which(cmd)` verifica se uma IDE ou app de música está instalado e acessível.
- Base da detecção automática de software instalado, funcionando de forma cross-platform.

### webbrowser

Módulo da biblioteca padrão para abertura de URLs:

- Quando o usuário seleciona "Custom URL" ou o preset contém uma URL (`http://`/`https://`), o `webbrowser.open()` inria o navegador padrão do sistema com a playlist.

### platform

Detecção do sistema operacional para rotear funcionalidades:

- `platform.system()` identifica Linux ou Windows.
- No Linux, usa `xrandr` para controle de brilho.
- No Windows, usa PowerShell/WMI.
- Outros sistemas (macOS) não possuem suporte a brilho nesta versão.

### base64 + io

Conversão de imagens PIL para formato compatível com tkinter:

- `io.BytesIO` salva a imagem PIL em memória no formato PNG.
- `base64.b64encode` codifica os bytes para uma string data URI.
- `tk.PhotoImage(data=...)` carrega diretamente sem arquivos temporários.

---

## Estrutura do Projeto

```
dev_mode/
├── pyproject.toml              # Configuração de build e dependências
├── run_dev_mode.py             # Script de entrada para execução direta
├── README.md                   # Este arquivo
├── src/
│   └── dev_mode/
│       ├── __init__.py
│       ├── __main__.py         # Entry point: python -m dev_mode
│       ├── app.py              # Classe principal DevModeApp (GUI)
│       ├── config.py           # Cores, fontes, constantes e paths
│       ├── font_renderer.py    # Renderização de texto com PIL → PhotoImage
│       ├── label_renderer.py   # Labels customizados com JetBrains Mono
│       ├── ui_components.py    # Botões, tooltips, animações de hover
│       ├── ide_detector.py     # Detecção automática de IDEs instaladas
│       ├── music_detector.py   # Detecção de apps de música e abertura
│       ├── brightness_controller.py  # Controle de brilho (Linux/Windows)
│       ├── presets_manager.py  # CRUD de presets em JSON
│       ├── preset_applier.py   # Orquestra a aplicação de um preset
│       ├── resources.py        # Resolvedor de paths de assets/fonts
│       ├── assets/             # Ícones PNG (adicionar, editar, excluir)
│       └── fonts/              # Fontes TTF (Press Start 2P, JetBrains Mono)
```

---

## Como Instalar e Rodar com dev_mode.desktop (Linux)

O jeito mais fácil é baixar os arquivos `dev_mode.desktop`, `dev_mode.AppImage` e `dev_mode.png` (ícone) da pasta `release/` ou da página de Releases do projeto e colocá-los na mesma pasta.

### Passos:

1. Baixe os arquivos `dev_mode.desktop`, `dev_mode.AppImage` e `dev_mode.png`.
2. Dê permissão de execução ao `.desktop` e ao AppImage:
   ```bash
   chmod +x dev_mode.desktop dev_mode.AppImage
   ```
3. Dê duplo clique no `dev_mode.desktop` para rodar o Dev_Mode!

Se aparecer um aviso de segurança, clique com o botão direito, vá em "Propriedades" e marque como confiável.

Pronto! Não precisa instalar Python nem dependências.

---

## Como Rodar

### Pré-requisitos

- **Python** >= 3.10
- **Pillow** (instalada automaticamente via `pip install -e .`)
- **Linux**: `xrandr` instalado (geralmente presente em sistemas X11)
- **Windows**: PowerShell com acesso a WMI

### Método 1: Execução Direta (rápido, sem instalação)

```bash
python3 run_dev_mode.py
```

> ⚠️ Não instala o pacote nem adiciona o comando `dev-mode` ao PATH.

### Método 2: Instalação como Pacote Editável (recomendado)

```bash
# 1. Crie um ambiente virtual
python3 -m venv .venv

# 2. Ative o ambiente
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate        # Windows

# 3. Instale o pacote em modo editável
pip install -e .

# 4. Execute via módulo
python -m dev_mode
```

### Método 3: Comando Global (após instalação)

Após `pip install -e .`, o entry point `dev-mode` fica disponível no PATH:

```bash
dev-mode
```

---

## Como Usar

1. **Na tela principal**, selecione um preset existente no dropdown ou crie um novo.
2. **Para criar/editar**: Clique em ➕ (Adicionar) ou ✏️ (Editar). Preencha:
   - **Nome do preset**: identificador único.
   - **IDE padrão**: selecione entre as IDEs detectadas automaticamente.
   - **Playlist**: escolha um app de música detectado ou "Custom URL" para inrir uma URL no navegador.
   - **Brilho**: ajuste o slider de 10% a 100%.
3. **Clique em "Apply"** para executar o preset: a IDE será aberta, a playlist iniciada e o brilho ajustado.
4. **Feedback visual**: uma mensagem temporária aparece indicando quais ações foram aplicadas com sucesso.

---

## IDEs Suportadas (Detecção Automática)

| IDE                     | Comando                 |
| ----------------------- | ----------------------- |
| VS Code                 | `code`                  |
| VS Code Insiders        | `code-insiders`         |
| Cursor                  | `cursor`                |
| Windsurf                | `windsurf`              |
| Zed                     | `zed`                   |
| JetBrains Fleet         | `fleet`                 |
| VSCodium                | `codium`                |
| PyCharm                 | `pycharm`               |
| PyCharm Community       | `pycharm-community`     |
| IntelliJ IDEA           | `idea`                  |
| IntelliJ IDEA Community | `idea-community`        |
| PhpStorm                | `phpstorm`              |
| WebStorm                | `webstorm`              |
| CLion                   | `clion`                 |
| Rider                   | `rider`                 |
| GoLand                  | `goland`                |
| RubyMine                | `rubymine`              |
| DataGrip                | `datagrip`              |
| Android Studio          | `android-studio`        |
| Sublime Text            | `subl` / `sublime_text` |
| Atom                    | `atom`                  |
| Gedit                   | `gedit`                 |
| Kate                    | `kate`                  |
| Geany                   | `geany`                 |
| Emacs                   | `emacs`                 |
| Vim                     | `vim`                   |
| Neovim                  | `nvim`                  |
| Nano                    | `nano`                  |
| Micro                   | `micro`                 |
| Lapce                   | `lapce`                 |
| Helix                   | `helix`                 |
| Oni / Oni 2             | `oni` / `oni2`          |

> A detecção também busca em caminhos alternativos como `/opt`, `/snap/bin`, `~/.local/bin`, Flatpak e AppImages.

---

## Apps de Música Suportados

| App        | Comando      |
| ---------- | ------------ |
| Spotify    | `spotify`    |
| Rhythmbox  | `rhythmbox`  |
| Audacious  | `audacious`  |
| Clementine | `clementine` |
| Amarok     | `amarok`     |
| DeaDBeeF   | `deadbeef`   |
| Lollypop   | `lollypop`   |

> Também é possível usar qualquer URL de playlist (YouTube, Spotify Web, etc.) via opção **Custom URL**.

---

## Autor

Desenvolvido por **Marcos André** © 2026
