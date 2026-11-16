
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import csv

from fuzzy_controller import fuzzy_controller


# ==========================================
# 1. PANEL PARAMETRELERI
# ==========================================

V_OC = 64.2
I_SC = 5.96
V_MP = 54.6
I_MP = 5.56
G_REF = 1000.0

# Onceki basit PV modeliyle ayni parametre
K = np.log(1 - I_MP / I_SC) / np.log(V_MP / V_OC)


# ==========================================
# 2. PV GUC MODELI
# ==========================================

def pv_power(voltage, irradiance):
    voltage = np.asarray(voltage, dtype=float)

    v_normalized = np.clip(voltage / V_OC, 0, 1)

    current = (
        I_SC
        * (irradiance / G_REF)
        * (1 - v_normalized ** K)
    )

    return voltage * np.maximum(current, 0)


# ==========================================
# 3. GUNES ISINIMI SENARYOSU
# ==========================================

def solar_irradiance(t):

    if t < 1:
        return 700.0

    elif t < 2:
        return 900.0

    elif t < 3:
        return 1100.0

    else:
        return 800.0


# ==========================================
# 4. MPPT HATA HESABI
# ==========================================

# Guc-gerilim egrisinin egimini yaklasik hesapla.
# Pozitif egim: gerilimi artirmak gucu artirir.
# Negatif egim: gerilimi azaltmak gucu artirir.

def power_slope(voltage, irradiance):

    h = 0.05

    v1 = max(0, voltage - h)
    v2 = min(V_OC, voltage + h)

    if v2 <= v1:
        return 0.0

    p1 = pv_power(v1, irradiance)
    p2 = pv_power(v2, irradiance)

    return float((p2 - p1) / (v2 - v1))


# ==========================================
# 5. SIMULASYON AYARLARI
# ==========================================

DT = 0.02
TIME = np.arange(0, 4.0 + DT / 2, DT)

INITIAL_VOLTAGE = 30.0

# Sabit adimli karsilastirma yontemi
FIXED_STEP = 0.5

# Bulanik destekli adim parametreleri
BASE_STEP = 0.35
FUZZY_GAIN = 2.0
MAX_STEP = 2.0

# Maksimum guc noktasina yakinlik toleransi
SLOPE_TOLERANCE = 0.02


# ==========================================
# 6. IKI YONTEMIN SIMULASYONU
# ==========================================

def simulate():

    voltage_fixed = INITIAL_VOLTAGE
    voltage_fuzzy = INITIAL_VOLTAGE

    previous_error = 0.0

    results = []

    for t in TIME:

        g = solar_irradiance(t)

        power_fixed = float(
            pv_power(voltage_fixed, g)
        )

        power_fuzzy = float(
            pv_power(voltage_fuzzy, g)
        )

        # Referans maksimum guc:
        # Sadece performans olcumu icin kullanilir.
        search_v = np.linspace(0, V_OC, 1000)
        possible_powers = pv_power(search_v, g)

        maximum_power = float(
            np.max(possible_powers)
        )

        # Iki yontemin egimleri
        slope_fixed = power_slope(
            voltage_fixed, g
        )

        slope_fuzzy = power_slope(
            voltage_fuzzy, g
        )

        # Normalize edilmis fuzzy girisleri
        # Isinim degisimine gore olcekleme
        slope_scale = max(
            I_SC * g / G_REF, 0.001
        )

        error = float(
            np.clip(
                slope_fuzzy / slope_scale,
                -1, 1
            )
        )

        delta_error = float(
            np.clip(
                error - previous_error,
                -1, 1
            )
        )

        # Bulanik kontrolcu
        fuzzy_output, _, _, _ = fuzzy_controller(
            error, delta_error
        )

        # Burada bulanık kontrolcu adim BUYUKLUGUNU
        # ayarlar. Yon, guc egiminden belirlenir.
        adaptive_step = np.clip(
            BASE_STEP + FUZZY_GAIN * abs(fuzzy_output),
            BASE_STEP,
            MAX_STEP
        )

        # Sonuclari kaydet
        results.append([
            float(t),
            g,
            float(voltage_fixed),
            float(voltage_fuzzy),
            power_fixed,
            power_fuzzy,
            maximum_power,
            float(fuzzy_output),
            float(adaptive_step)
        ])

        # Sabit adimli kontrol
        if abs(slope_fixed) > SLOPE_TOLERANCE:

            voltage_fixed += (
                np.sign(slope_fixed) * FIXED_STEP
            )

        # Bulanik destekli kontrol
        if abs(slope_fuzzy) > SLOPE_TOLERANCE:

            voltage_fuzzy += (
                np.sign(slope_fuzzy) * adaptive_step
            )

        voltage_fixed = float(
            np.clip(voltage_fixed, 0, V_OC)
        )

        voltage_fuzzy = float(
            np.clip(voltage_fuzzy, 0, V_OC)
        )

        previous_error = error

    return np.array(results)


# ==========================================
# 7. SONUCLARI HESAPLA
# ==========================================

data = simulate()

time = data[:, 0]
irradiance = data[:, 1]

v_fixed = data[:, 2]
v_fuzzy = data[:, 3]

p_fixed = data[:, 4]
p_fuzzy = data[:, 5]
p_max = data[:, 6]

fuzzy_outputs = data[:, 7]
adaptive_steps = data[:, 8]

# Ortalama mutlak guc takip hatasi
mae_fixed = np.mean(np.abs(p_max - p_fixed))
mae_fuzzy = np.mean(np.abs(p_max - p_fuzzy))

# Ortalama karekok hata
rmse_fixed = np.sqrt(
    np.mean((p_max - p_fixed) ** 2)
)

rmse_fuzzy = np.sqrt(
    np.mean((p_max - p_fuzzy) ** 2)
)

# Ortalama takip verimi (%)
eff_fixed = 100 * np.mean(
    p_fixed / np.maximum(p_max, 0.001)
)

eff_fuzzy = 100 * np.mean(
    p_fuzzy / np.maximum(p_max, 0.001)
)

print("=" * 55)
print("MPPT SIMULATION RESULTS")
print("=" * 55)

print(f"Fixed Step MAE:   {mae_fixed:.4f} W")
print(f"Fuzzy Step MAE:   {mae_fuzzy:.4f} W")

print(f"Fixed Step RMSE:  {rmse_fixed:.4f} W")
print(f"Fuzzy Step RMSE:  {rmse_fuzzy:.4f} W")

print(f"Fixed Efficiency: {eff_fixed:.2f} %")
print(f"Fuzzy Efficiency: {eff_fuzzy:.2f} %")


# ==========================================
# 8. GRAFIKLER
# ==========================================

base_dir = Path(__file__).resolve().parent.parent

figure_dir = base_dir / "results" / "figures"
table_dir = base_dir / "results" / "tables"

figure_dir.mkdir(parents=True, exist_ok=True)
table_dir.mkdir(parents=True, exist_ok=True)


def style_plot(ax, title, ylabel):

    ax.set_facecolor("#FCF8FF")
    ax.set_title(
        title,
        color="#70209F",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Time (s)")
    ax.set_ylabel(ylabel)

    ax.grid(
        True,
        linestyle="--",
        alpha=0.3
    )

    ax.legend()


# Grafik 1: Gunes isinimi
fig1, ax1 = plt.subplots(figsize=(10, 4))

ax1.plot(
    time, irradiance,
    color="#F4DC50",
    linewidth=2.5,
    label="Solar Irradiance"
)

style_plot(
    ax1,
    "Solar Irradiance Profile",
    "Irradiance (W/m2)"
)

fig1.tight_layout()
fig1.savefig(
    figure_dir / "mppt_irradiance.png",
    dpi=300
)


# Grafik 2: Cikis gucu
fig2, ax2 = plt.subplots(figsize=(11, 5))

ax2.plot(
    time, p_max,
    color="#611375",
    linestyle="--",
    linewidth=2,
    label="Reference Maximum Power"
)

ax2.plot(
    time, p_fixed,
    color="#3EE2FF",
    linewidth=1.8,
    label="Fixed Step"
)

ax2.plot(
    time, p_fuzzy,
    color="#B555ED",
    linewidth=2,
    label="Fuzzy-Assisted Step"
)

style_plot(
    ax2,
    "MPPT Power Tracking Comparison",
    "PV Power (W)"
)

fig2.tight_layout()
fig2.savefig(
    figure_dir / "mppt_power_comparison.png",
    dpi=300
)


# Grafik 3: Gerilim
fig3, ax3 = plt.subplots(figsize=(11, 5))

ax3.plot(
    time, v_fixed,
    color="#3EE2FF",
    linewidth=2,
    label="Fixed Step Voltage"
)

ax3.plot(
    time, v_fuzzy,
    color="#B555ED",
    linewidth=2,
    label="Fuzzy-Assisted Voltage"
)

style_plot(
    ax3,
    "MPPT Operating Voltage",
    "Voltage (V)"
)

fig3.tight_layout()
fig3.savefig(
    figure_dir / "mppt_voltage_comparison.png",
    dpi=300
)


# ==========================================
# 9. CSV SONUCLARINI KAYDET
# ==========================================

csv_path = table_dir / "mppt_results.csv"

headers = [
    "time_s",
    "irradiance_wm2",
    "voltage_fixed_v",
    "voltage_fuzzy_v",
    "power_fixed_w",
    "power_fuzzy_w",
    "reference_max_power_w",
    "fuzzy_output",
    "adaptive_step_v"
]

with open(
    csv_path, "w", newline="", encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow(headers)
    writer.writerows(data)


print("\nGrafikler kaydedildi.")
print("CSV sonuclari kaydedildi.")
print("Simulasyon tamamlandi!")

plt.show()
