#!/usr/bin/env bash
# build.sh — Gera o executável standalone do Dev Mode via PyInstaller
set -e

echo "📦 Instalando dependências de build..."
pip install pyinstaller pillow --break-system-packages 2>/dev/null || pip install pyinstaller pillow

echo "🔨 Gerando executável..."
pyinstaller dev_mode.spec --noconfirm

echo "✅ Executável gerado em: dist/dev_mode"

# Copia para a pasta release/
mkdir -p release
cp dist/dev_mode release/dev_mode
cp src/dev_mode/assets/dev-mode.png release/dev-mode.png 2>/dev/null || true
cp release/dev_mode.desktop release/dev_mode.desktop 2>/dev/null || true
cp release/launch_dev_mode.sh release/launch_dev_mode.sh 2>/dev/null || true

echo "📁 Arquivos prontos em release/"