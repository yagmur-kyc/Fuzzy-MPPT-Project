
import csv
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from fuzzy_controller import fuzzy_controller


# ==========================================
# 1. PROJE YOLLARI
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
TABLE_DIR = BASE_DIR / "results" / "tables"
FIGURE_DIR = BASE_DIR / "results" / "figures"

FIGURE_DIR.mkdir(parents=True, exist_ok=True)

BASELINE_FILE = TABLE_DIR / "mppt_results.csv"


# ==========================================
# 2. PV MODEL PARAMETRELERI
# ==========================================

V_OC = 64.2
I_SC = 5.96
V_MP = 54.6
I_MP = 5.56
G_REF = 1000.0

K = np.log(1 - I_MP / I_SC) / np.log(V_MP / V_OC)


def pv_power(voltage, irradiance):
    v = np.asarray(voltage, dtype=float)
    vn = np.clip(v / V_OC, 0, 1)

    current = I_SC * (irradiance / G_REF) * (
        1 - vn ** K
    )

    return v * np.maximum(current, 0)


def power_slope(voltage, irradiance):
    h = 0.05

    v1 = max(0, voltage - h)
    v2 = min(V_OC, voltage + h)

    if v2 <= v1:
        return 0.0

    return float(
        (pv_power(v2, irradiance)
         - pv_power(v1, irradiance))
        / (v2 - v1)
    )


# ==========================================
# 3. ONCEKI DENEYIN SONUCLARINI OKU
# ==========================================

with open(
    BASELINE_FILE, newline="", encoding="utf-8"
) as file:
    rows = list(csv.DictReader(file))

if not rows:
    raise ValueError("Baseline CSV dosyasi bos.")

time = np.array(
    [float(r["time_s"]) for r in rows]
)

irradiance = np.array(
    [float(r["irradiance_wm2"]) for r in rows]
)

p_fixed = np.array(
    [float(r["power_fixed_w"]) for r in rows]
)

p_fuzzy = np.array(
    [float(r["power_fuzzy_w"]) for r in rows]
)

v_fixed = np.array(
    [float(r["voltage_fixed_v"]) for r in rows]
)

v_fuzzy = np.array(
    [float(r["voltage_fuzzy_v"]) for r in rows]
)

p_max = np.array(
    [float(r["reference_max_power_w"]) for r in rows]
)


# ==========================================
# 4. GELISTIRILEN KONTROLCU
# ==========================================

# Deneysel olarak denenecek parametreler
MIN_STEP = 0.04
MAX_STEP = 2.0
ERROR_GAIN = 1.6
FUZZY_GAIN = 0.35

# Maksimum guc noktasina yakin tolerans
SLOPE_DEADBAND = 0.12

voltage = 30.0
previous_error = 0.0

proposed_voltage = []
proposed_power = []
proposed_steps = []

for t, g in zip(time, irradiance):

    # Mevcut calisma noktasini kaydet
    proposed_voltage.append(voltage)
    proposed_power.append(float(pv_power(voltage, g)))

    slope = power_slope(voltage, g)

    slope_scale = max(I_SC * g / G_REF, 0.001)

    error = float(
        np.clip(slope / slope_scale, -1, 1)
    )

    delta_error = float(
        np.clip(error - previous_error, -1, 1)
    )

    fuzzy_output, _, _, _ = fuzzy_controller(
        error, delta_error
    )

    # Yakin noktada kucuk adim,
    # uzak noktada buyuk adim
    adaptive_step = (
        MIN_STEP
        + ERROR_GAIN * abs(error)
        + FUZZY_GAIN * abs(fuzzy_output)
    )

    adaptive_step = float(
        np.clip(adaptive_step, MIN_STEP, MAX_STEP)
    )

    # Deadband: MPP yakininda gerilimi tut
    if abs(slope) <= SLOPE_DEADBAND:
        adaptive_step = 0.0
    else:
        voltage += np.sign(slope) * adaptive_step

    voltage = float(np.clip(voltage, 0, V_OC))

    proposed_steps.append(adaptive_step)
    previous_error = error

proposed_voltage = np.array(proposed_voltage)
proposed_power = np.array(proposed_power)


# ==========================================
# 5. PERFORMANS METRIKLERI
# ==========================================

def calculate_metrics(power):
    error = p_max - power

    mae = float(np.mean(np.abs(error)))

    rmse = float(np.sqrt(np.mean(error ** 2)))

    efficiency = float(
        100 * np.mean(
            power / np.maximum(p_max, 0.001)
        )
    )

    return mae, rmse, efficiency


methods = {
    "Fixed Step": p_fixed,
    "Fuzzy-Assisted": p_fuzzy,
    "Proposed": proposed_power
}

print("\n" + "=" * 65)
print("THREE-METHOD MPPT COMPARISON")
print("=" * 65)

print(
    f"{'Method':<20}"
    f"{'MAE (W)':>12}"
    f"{'RMSE (W)':>14}"
    f"{'Efficiency (%)':>18}"
)

print("-" * 65)

metrics = {}

for name, power in methods.items():
    mae, rmse, efficiency = calculate_metrics(power)

    metrics[name] = (mae, rmse, efficiency)

    print(
        f"{name:<20}"
        f"{mae:>12.4f}"
        f"{rmse:>14.4f}"
        f"{efficiency:>18.2f}"
    )


# ==========================================
# 6. GUC KARSILASTIRMA GRAFIGI
# ==========================================

fig, ax = plt.subplots(figsize=(12, 6))

fig.patch.set_facecolor("#FFFDFE")
ax.set_facecolor("#FCF8FF")

ax.plot(
    time, p_max,
    "--", color="#611375",
    linewidth=2,
    label="Reference Maximum Power"
)

ax.plot(
    time, p_fixed,
    color="#3EE2FF",
    linewidth=1.6,
    label="Fixed Step"
)

ax.plot(
    time, p_fuzzy,
    color="#DF37AD",
    linewidth=1.6,
    label="Fuzzy-Assisted"
)

ax.plot(
    time, proposed_power,
    color="#B555ED",
    linewidth=2.3,
    label="Proposed Controller"
)

ax.set_title(
    "MPPT - Baseline vs Proposed Method",
    fontsize=16,
    fontweight="bold",
    color="#70209F"
)

ax.set_xlabel("Time (s)")
ax.set_ylabel("PV Power (W)")

ax.grid(alpha=0.3, linestyle="--")
ax.legend()

plt.tight_layout()

fig.savefig(
    FIGURE_DIR / "proposed_power_comparison.png",
    dpi=300
)


# ==========================================
# 7. GERILIM KARSILASTIRMA GRAFIGI
# ==========================================

fig2, ax2 = plt.subplots(figsize=(12, 6))

fig2.patch.set_facecolor("#FFFDFE")
ax2.set_facecolor("#FCF8FF")

ax2.plot(
    time, v_fixed,
    color="#3EE2FF",
    label="Fixed Step"
)

ax2.plot(
    time, v_fuzzy,
    color="#DF37AD",
    label="Fuzzy-Assisted"
)

ax2.plot(
    time, proposed_voltage,
    color="#B555ED",
    linewidth=2,
    label="Proposed Controller"
)

ax2.set_title(
    "MPPT - Operating Voltage Comparison",
    fontsize=16,
    fontweight="bold",
    color="#70209F"
)

ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Voltage (V)")
ax2.grid(alpha=0.3, linestyle="--")
ax2.legend()

plt.tight_layout()

fig2.savefig(
    FIGURE_DIR / "proposed_voltage_comparison.png",
    dpi=300
)


# ==========================================
# 8. DENEY SONUCLARINI KAYDET
# ==========================================

output_csv = TABLE_DIR / "proposed_results.csv"

with open(
    output_csv, "w", newline="", encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "time_s",
        "irradiance_wm2",
        "voltage_proposed_v",
        "power_proposed_w",
        "reference_max_power_w",
        "step_size_v"
    ])

    for i in range(len(time)):
        writer.writerow([
            time[i],
            irradiance[i],
            proposed_voltage[i],
            proposed_power[i],
            p_max[i],
            proposed_steps[i]
        ])


summary_csv = TABLE_DIR / "method_comparison.csv"

with open(
    summary_csv, "w", newline="", encoding="utf-8"
) as file:

    writer = csv.writer(file)
    writer.writerow([
        "method", "mae_w", "rmse_w",
        "efficiency_percent"
    ])

    for name, values in metrics.items():
        writer.writerow([name, *values])


print("\nDeney tamamlandi.")
print("Grafikler ve CSV sonuclari kaydedildi.")

plt.show()
