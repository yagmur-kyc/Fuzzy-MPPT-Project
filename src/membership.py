
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ==========================================
# 1. UYELIK FONKSIYONLARI
# ==========================================

def triangular_mf(x, a, b, c):
    """Ucgensel uyelik fonksiyonu."""
    if not a < b < c:
        raise ValueError("a < b < c olmali.")

    x = np.asarray(x, dtype=float)

    left = (x - a) / (b - a)
    right = (c - x) / (c - b)

    return np.clip(np.minimum(left, right), 0, 1)


def left_shoulder_mf(x, a, b):
    """Sol omuz uyelik fonksiyonu."""
    if not a < b:
        raise ValueError("a < b olmali.")

    x = np.asarray(x, dtype=float)

    return np.clip((b - x) / (b - a), 0, 1)


def right_shoulder_mf(x, a, b):
    """Sag omuz uyelik fonksiyonu."""
    if not a < b:
        raise ValueError("a < b olmali.")

    x = np.asarray(x, dtype=float)

    return np.clip((x - a) / (b - a), 0, 1)


# ==========================================
# 2. GIRIS DEGERLERI
# ==========================================

# Normalize edilmis giris araligi
x = np.linspace(-1, 1, 1000)


# ==========================================
# 3. BULANIK UYELIK KUMELERI
# ==========================================

# Makaledeki Fig. 6 temel alinarak
# olusturulan yaklasik parametreler.

input_mfs = {
    "NB": left_shoulder_mf(x, -1.0, -0.66),

    "NM": triangular_mf(x, -1.0, -0.66, -0.33),

    "NS": triangular_mf(x, -0.66, -0.33, 0.0),

    "Z": triangular_mf(x, -0.33, 0.0, 0.33),

    "PS": triangular_mf(x, 0.0, 0.33, 0.66),

    "PM": triangular_mf(x, 0.33, 0.66, 1.0),

    "PB": right_shoulder_mf(x, 0.66, 1.0)
}


# ==========================================
# 4. MOR / LILAC RENK PALETI
# ==========================================

colors = {
    "NB": "#611375",
    "NM": "#AA4CE0",
    "NS": "#3EE2FF",
    "Z":  "#DF37AD",
    "PS": "#F4DC50",
    "PM": "#00F6A4",
    "PB": "#B200C3"
}


# ==========================================
# 5. GRAFIK TASARIMI
# ==========================================

fig, ax = plt.subplots(figsize=(11, 6))

# Arka plan renkleri
fig.patch.set_facecolor("#FFFDFE")
ax.set_facecolor("#FCF8FF")

# Uyelik fonksiyonlarini ciz
for label, membership in input_mfs.items():

    ax.plot(
        x,
        membership,
        label=label,
        color=colors[label],
        linewidth=2.8
    )

# Grafik basligi
ax.set_title(
    "AFLC - Input Membership Functions",
    fontsize=16,
    fontweight="bold",
    color="#70209F",
    pad=20
)

# Eksen isimleri
ax.set_xlabel(
    "Normalized Input (e / Delta e)",
    fontsize=12
)

ax.set_ylabel(
    "Membership Degree",
    fontsize=12
)

# Eksen sinirlari
ax.set_xlim(-1.05, 1.05)
ax.set_ylim(-0.05, 1.10)

# Izgara
ax.grid(
    True,
    linestyle="--",
    alpha=0.25
)

# Lejant
ax.legend(
    title="Fuzzy Sets",
    loc="upper right",
    ncol=2,
    frameon=True
)

# Cerceve duzenlemesi
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()


# ==========================================
# 6. GRAFIGI KAYDET
# ==========================================

# Proje ana klasoru
BASE_DIR = Path(__file__).resolve().parent.parent

# Grafiklerin kaydedilecegi klasor
output_dir = BASE_DIR / "results" / "figures"

# Klasor yoksa otomatik olustur
output_dir.mkdir(parents=True, exist_ok=True)

# Grafik dosyasi
output_path = output_dir / "input_membership_functions.png"

# Yuksek cozunurlukte kaydet
plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

print("7 uyelik fonksiyonu olusturuldu.")
print("Grafik basariyla kaydedildi!")
print(f"Kayit konumu: {output_path}")

# Grafigi ekranda goster
plt.show()
