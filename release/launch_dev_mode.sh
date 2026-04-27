#!/usr/bin/env bash
# Launcher do Dev Mode — executa sempre a partir da própria pasta
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec "$SCRIPT_DIR/dev_mode"