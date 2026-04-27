#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# O parâmetro -name força o binário a se identificar como 'dev_mode' no painel
exec "$SCRIPT_DIR/dev_mode" -name "dev_mode"