"""Naming helpers so a parallel V2 stack does not collide with legacy physical names."""

from typing import Optional


def normalize_generation(generation: Optional[str]) -> str:
    return (generation or "").strip().lower()


def name_segment(generation: Optional[str]) -> str:
    """Return 'v2-' when generation is v2, otherwise empty string."""
    g = normalize_generation(generation)
    return f"{g}-" if g else ""


def ssm_mss_path(generation: Optional[str]) -> str:
    """SSM path root: legacy 'devmedias', V2 'devmedias-v2'."""
    g = normalize_generation(generation)
    return f"devmedias-{g}" if g else "devmedias"
