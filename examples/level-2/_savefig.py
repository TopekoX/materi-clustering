"""Pembantu untuk skrip contoh: membuat plt.show() menyimpan gambar ke file.

Skrip dijalankan tanpa layar (backend Agg), jadi plt.show() tidak menampilkan
apa pun. Modul ini mengganti plt.show() supaya setiap gambar disimpan ke
docs/assets/level-2/ dengan nama yang kita tentukan.
"""

from pathlib import Path

import matplotlib.pyplot as plt

FIG_DIR = Path(__file__).resolve().parents[2] / "docs" / "assets" / "level-2"


def install(names):
    """Setiap plt.show() berikutnya menyimpan gambar bernama berikutnya di `names`."""
    saved = []

    def _show(*args, **kwargs):
        name = names[len(saved)]
        plt.gcf().savefig(FIG_DIR / f"{name}.png", dpi=120, bbox_inches="tight")
        plt.close("all")
        saved.append(name)
        print(f"[gambar disimpan: docs/assets/level-2/{name}.png]")

    plt.show = _show
