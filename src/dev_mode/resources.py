import os


def resource_path(*parts: str) -> str:
    """Resolve paths inside the installed package (assets, fonts, etc.)."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, *parts)

