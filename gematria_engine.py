# gematria_engine.py
# MOTOR GEMÁTRICO CANÓNICO
# (Módulo importable — NO se ejecuta)

import unicodedata
import re


# =========================
# UTILIDADES
# =========================

def normalize_text(text: str) -> str:
    text = text.upper()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = re.sub(r"[^A-Z ]", "", text)
    return text.strip()


def reduce_digit(n: int) -> int:
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


# =========================
# TABLAS
# =========================

def ordinal_value(letter: str) -> int:
    return ord(letter) - 64  # A=1 … Z=26


def reverse_ordinal_value(letter: str) -> int:
    return 27 - ordinal_value(letter)


# =========================
# MÉTODOS GEMÁTRICOS
# =========================

def ordinal(text: str) -> int:
    text = normalize_text(text)
    return sum(ordinal_value(c) for c in text if c != " ")


def digital_root(n: int) -> int:
    return reduce_digit(n)


def letter_reduction(text: str) -> int:
    text = normalize_text(text)
    total = 0
    for c in text:
        if c != " ":
            total += reduce_digit(ordinal_value(c))
    return total


def reverse_ordinal(text: str) -> int:
    text = normalize_text(text)
    return sum(reverse_ordinal_value(c) for c in text if c != " ")


def reverse_letter_reduction(text: str) -> int:
    text = normalize_text(text)
    total = 0
    for c in text:
        if c != " ":
            total += reduce_digit(reverse_ordinal_value(c))
    return total


# =========================
# FUNCIÓN MAESTRA
# =========================

def gematria_full(text: str) -> dict:
    o = ordinal(text)
    rev = reverse_ordinal(text)

    return {
        "TEXT": normalize_text(text),
        "O": o,
        "DR": digital_root(o),
        "LR": letter_reduction(text),
        "REV": rev,
        "RR": digital_root(rev),
        "RLR": reverse_letter_reduction(text),
    }