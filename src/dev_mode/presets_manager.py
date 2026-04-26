"""Gerenciamento de presets (carregar, salvar, excluir)."""

import json
import os
from .config import PRESETS_FILE


def load_presets():
    """Carrega a lista de presets do arquivo JSON."""
    if os.path.exists(PRESETS_FILE):
        with open(PRESETS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []


def save_presets(presets):
    """Salva a lista de presets no arquivo JSON."""
    with open(PRESETS_FILE, "w", encoding="utf-8") as f:
        json.dump(presets, f, ensure_ascii=False, indent=2)


def get_preset_names():
    """Retorna apenas os nomes dos presets salvos."""
    try:
        return [p["name"] for p in load_presets()]
    except Exception:
        return []


def delete_preset_by_name(name):
    """Remove um preset pelo nome e retorna a lista atualizada."""
    presets = load_presets()
    presets = [p for p in presets if p.get("name") != name]
    save_presets(presets)
    return presets


def add_preset(name, ide, playlist="", brightness=100):
    """Adiciona um novo preset se o nome não existir."""
    presets = load_presets()
    if not any(p.get("name") == name for p in presets):
        presets.append(
            {"name": name, "ide": ide, "playlist": playlist, "brightness": brightness}
        )
        save_presets(presets)


def get_preset_by_name(name):
    """Retorna um preset pelo nome ou None se não encontrar."""
    for p in load_presets():
        if p.get("name") == name:
            return p
    return None


def update_preset(old_name, new_name, ide, playlist="", brightness=100):
    """Atualiza um preset existente, permitindo renomear."""
    presets = load_presets()
    target = None
    for p in presets:
        if p.get("name") == old_name:
            target = p
            break
    if not target:
        return False

    # Se o nome mudou, verifica se já existe outro preset com esse nome
    if new_name != old_name:
        if any(p.get("name") == new_name for p in presets):
            return False  # nome já existe
        target["name"] = new_name

    target["ide"] = ide
    target["playlist"] = playlist
    target["brightness"] = brightness
    save_presets(presets)
    return True
