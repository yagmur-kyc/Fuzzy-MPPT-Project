
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ==========================================
# 1. OUTPUT MEMBERSHIP FUNCTIONS
# ==========================================

def triangular_mf(x, a, b, c):
    """Ucgensel uyelik fonksiyonu."""
    x = np.asarray(x, dtype=float)

    if not a < b < c:
        raise ValueError("a < b < c olmali.")

    left = (x - a) / (b - a)
    right = (c - x) / (c - b)

    return np.clip(np.minimum(left, right), 0, 1)


def left_shoulder_mf(x, a, b):
    """Sol omuz uyelik fonksiyonu."""
    x = np.asarray(x, dtype=float)

    if not a < b:
        raise ValueError("a < b olmali.")

    return np.clip((b - x) / (b - a), 0, 1)


def right_shoulder_mf(x, a, b):
    """Sag omuz uyelik fonksiyonu."""
    x = np.asarray(x, dtype=float)

    if not a < b:
        raise ValueError("a < b olmali.")

    return np.clip((x - a) / (b - a), 0, 1)


# ==========================================
# 2. OUTPUT RANGE
# ==========================================

# Makaledeki Fig. 6(b) ekseni: -2 ile 2
x = np.linspace(-2, 2, 2000)


# ==========================================
# 3. OUTPUT FUZZY SETS
# ==========================================

# Fig. 6(b) temel alinarak secilmis
# yaklasik parametreler.
# Bunlar yazarlarin yayinladigi kesin
# sayisal parametreler degildir.

output_mfs = {
    "NB": left_shoulder_mf(x, -1.0, -0.5),

    "NM": triangular_mf(x, -1.0, -0.67, -0.33),

    "NVS": triangular_mf(x, -0.67, -0.33, -0.17),

    "NS": triangular_mf(x, -0.33, -0.17, 0.0),

    "Z": triangular_mf(x, -0.17, 0.0, 0.17),

    "PS": triangular_mf(x, 0.0, 0.17, 0.33),

    "PVS": triangular_mf(x, 0.17, 0.33, 0.67),

    "PM": triangular_mf(x, 0.33, 0.67, 1.0),

    "PB": right_shoulder_mf(x, 0.5, 1.0)
}


# ==========================================
# 4. RENK PALETI
# ==========================================

colors = {
    "NB": "#611375",
    "NM": "#AA4CE0",
    "NVS": "#9061D8",
    "NS": "#3EE2FF",
    "Z": "#DF37AD",
    "PS": "#F4DC50",
    "PVS": "#FF9955",
    "PM": "#4AFFC3",
    "PB": "#B200C3"
}


# ==========================================
# 5. GRAFIK
# ==========================================

fig, ax = plt.subplots(figsize=(12, 6))

fig.patch.set_facecolor("#FFFDFE")
ax.set_facecolor("#FCF8FF")

for label, membership in output_mfs.items():

    ax.plot(
        x,
        membership,
        label=label,
        color=colors[label],
        linewidth=2.6
    )

ax.set_title(
    "AFLC - Output Membership Functions",
    fontsize=16,
    fontweight="bold",
    color="#70209F",
    pad=20
)

ax.set_xlabel(
    "Normalized Output",
    fontsize=12
)

ax.set_ylabel(
    "Membership Degree",
    fontsize=12
)

ax.set_xlim(-2.05, 2.05)
ax.set_ylim(-0.05, 1.10)

ax.grid(
    True,
    linestyle="--",
    alpha=0.3
)

ax.legend(
    title="Output Fuzzy Sets",
    loc="upper right",
    ncol=3
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()


# ==========================================
# 6. GRAFIGI KAYDET
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

output_dir = BASE_DIR / "results" / "figures"

output_dir.mkdir(parents=True, exist_ok=True)

output_path = (
    output_dir / "output_membership_functions.png"
)

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

print("9 cikis uyelik fonksiyonu olusturuldu.")
print("Grafik kaydedildi!")
print(f"Kayit konumu: {output_path}")

plt.show()
