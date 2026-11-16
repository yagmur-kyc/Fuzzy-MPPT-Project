
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ==========================================
# 1. SUNPOWER SPR-305 PANEL PARAMETRELERI
# ==========================================

P_MAX = 305.0       # Watt
V_OC = 64.2         # Volt
I_SC = 5.96         # Amper
V_MP = 54.6         # Volt
I_MP = 5.56         # Amper

G_REF = 1000.0      # W/m2
T_REF = 25.0        # Celsius


# ==========================================
# 2. BASITLESTIRILMIS PV MODELI
# ==========================================

# Model: I = Isc * (1 - (V/Voc)^k)
# k, Vmp ve Imp noktasindan hesaplanir.
#
# Bu model bir yaklasimdir.
# Makalenin ayrintili diyot modeli degildir.

K = np.log(1 - I_MP / I_SC) / np.log(V_MP / V_OC)


def pv_current(voltage, irradiance=1000.0):
    """
    Gerilim ve gunes isinimina gore
    panel akimini hesaplar.

    Sicaklik sabit 25 C kabul edilir.
    """

    voltage = np.asarray(voltage, dtype=float)

    if irradiance < 0:
        raise ValueError("Isinim negatif olamaz.")

    normalized_v = np.clip(voltage / V_OC, 0, 1)

    current = (
        I_SC
        * (irradiance / G_REF)
        * (1 - normalized_v ** K)
    )

    return np.maximum(current, 0)


def pv_power(voltage, irradiance=1000.0):
    """
    Panel gucu: P = V * I
    """

    current = pv_current(voltage, irradiance)

    return np.asarray(voltage) * current


# ==========================================
# 3. GERILIM DEGERLERI
# ==========================================

voltage = np.linspace(0, V_OC, 1000)

irradiance_levels = [600, 800, 1000]

colors = {
    600: "#3EE2FF",
    800: "#DF37AD",
    1000: "#B555ED"
}


# ==========================================
# 4. GRAFIK TASARIMI
# ==========================================

fig, ax = plt.subplots(figsize=(11, 6))

fig.patch.set_facecolor("#FFFDFE")
ax.set_facecolor("#FCF8FF")

for g in irradiance_levels:

    power = pv_power(voltage, g)

    ax.plot(
        voltage,
        power,
        color=colors[g],
        linewidth=2.8,
        label=f"{g} W/m2"
    )

    index = np.argmax(power)

    maximum_voltage = voltage[index]
    maximum_power = power[index]

    ax.scatter(
        maximum_voltage,
        maximum_power,
        color=colors[g],
        s=60,
        zorder=5
    )

    print(
        f"Isinim: {g} W/m2 | "
        f"MPP gerilimi: {maximum_voltage:.2f} V | "
        f"Maksimum guc: {maximum_power:.2f} W"
    )


ax.set_title(
    "Photovoltaic Panel - Power Voltage Curves",
    fontsize=16,
    fontweight="bold",
    color="#70209F",
    pad=20
)

ax.set_xlabel("Voltage (V)", fontsize=12)
ax.set_ylabel("Power (W)", fontsize=12)

ax.grid(True, linestyle="--", alpha=0.3)
ax.legend(title="Solar Irradiance")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()


# ==========================================
# 5. GRAFIGI KAYDET
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

output_dir = BASE_DIR / "results" / "figures"

output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "pv_power_curves.png"

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

print("\nPV modeli basariyla calisti!")
print(f"Grafik kaydedildi: {output_path}")

plt.show()
