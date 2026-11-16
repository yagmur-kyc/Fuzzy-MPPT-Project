
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from rule_base import (
    error_labels,
    delta_error_labels,
    rule_matrix
)


# ==========================================
# 1. UYELIK FONKSIYONLARI
# ==========================================

def triangular_mf(x, a, b, c):
    x = np.asarray(x, dtype=float)
    left = (x - a) / (b - a)
    right = (c - x) / (c - b)
    return np.clip(np.minimum(left, right), 0, 1)


def left_shoulder_mf(x, a, b):
    x = np.asarray(x, dtype=float)
    return np.clip((b - x) / (b - a), 0, 1)


def right_shoulder_mf(x, a, b):
    x = np.asarray(x, dtype=float)
    return np.clip((x - a) / (b - a), 0, 1)


# ==========================================
# 2. GIRIS UYELIK FONKSIYONLARI
# ==========================================

# membership.py ile ayni parametreler

INPUT_PARAMS = {
    "NB": ("left", -1.0, -0.66),
    "NM": ("tri", -1.0, -0.66, -0.33),
    "NS": ("tri", -0.66, -0.33, 0.0),
    "Z":  ("tri", -0.33, 0.0, 0.33),
    "PS": ("tri", 0.0, 0.33, 0.66),
    "PM": ("tri", 0.33, 0.66, 1.0),
    "PB": ("right", 0.66, 1.0)
}


# ==========================================
# 3. CIKIS UYELIK FONKSIYONLARI
# ==========================================

# output_membership.py ile ayni parametreler

OUTPUT_PARAMS = {
    "NB": ("left", -1.0, -0.5),
    "NM": ("tri", -1.0, -0.67, -0.33),
    "NVS": ("tri", -0.67, -0.33, -0.17),
    "NS": ("tri", -0.33, -0.17, 0.0),
    "Z": ("tri", -0.17, 0.0, 0.17),
    "PS": ("tri", 0.0, 0.17, 0.33),
    "PVS": ("tri", 0.17, 0.33, 0.67),
    "PM": ("tri", 0.33, 0.67, 1.0),
    "PB": ("right", 0.5, 1.0)
}


# ==========================================
# 4. UYELIK DERECESINI HESAPLA
# ==========================================

def calculate_membership(x, params):

    mf_type = params[0]
    values = params[1:]

    if mf_type == "tri":
        return triangular_mf(x, *values)

    if mf_type == "left":
        return left_shoulder_mf(x, *values)

    if mf_type == "right":
        return right_shoulder_mf(x, *values)

    raise ValueError("Gecersiz uyelik fonksiyonu")


# ==========================================
# 5. FUZZIFICATION
# ==========================================

def fuzzify(value):

    # Girisler normalize edilmis [-1, 1]
    if not -1 <= value <= 1:
        raise ValueError("Giris -1 ile 1 arasinda olmali")

    degrees = {}

    for label, params in INPUT_PARAMS.items():
        degrees[label] = float(
            calculate_membership(value, params)
        )

    return degrees


# ==========================================
# 6. FUZZY INFERENCE
# ==========================================

def fuzzy_inference(error, delta_error):

    error_degrees = fuzzify(error)
    delta_degrees = fuzzify(delta_error)

    # Cikis ekseni
    output_x = np.linspace(-2, 2, 2001)

    aggregated = np.zeros_like(output_x)

    active_rules = []

    # Makaledeki 49 kurali degerlendir
    for row_index, delta_label in enumerate(
        delta_error_labels
    ):

        for col_index, error_label in enumerate(
            error_labels
        ):

            output_label = rule_matrix[
                row_index
            ][col_index]

            # Mamdani AND: minimum
            strength = min(
                error_degrees[error_label],
                delta_degrees[delta_label]
            )

            if strength <= 0:
                continue

            output_mf = calculate_membership(
                output_x,
                OUTPUT_PARAMS[output_label]
            )

            # Implication: minimum
            clipped = np.minimum(strength, output_mf)

            # Aggregation: maksimum
            aggregated = np.maximum(
                aggregated,
                clipped
            )

            active_rules.append(
                (error_label, delta_label,
                 output_label, strength)
            )

    return output_x, aggregated, active_rules


# ==========================================
# 7. DEFUZZIFICATION - CENTROID
# ==========================================

def defuzzify(output_x, aggregated):

    denominator = np.trapezoid(
        aggregated, output_x
    )

    if denominator <= 0:
        raise ValueError(
            "Aktif cikis alani olusmadi"
        )

    numerator = np.trapezoid(
        output_x * aggregated,
        output_x
    )

    return float(numerator / denominator)


# ==========================================
# 8. KONTROLCUYU CALISTIR
# ==========================================

def fuzzy_controller(error, delta_error):

    output_x, aggregated, active_rules = (
        fuzzy_inference(error, delta_error)
    )

    crisp_output = defuzzify(
        output_x, aggregated
    )

    return (
        crisp_output,
        output_x,
        aggregated,
        active_rules
    )


# ==========================================
# 9. TEST VE GRAFIK
# ==========================================

if __name__ == "__main__":

    # Ornek test girisleri
    error = 0.2
    delta_error = -0.1

    result, x, y, active_rules = (
        fuzzy_controller(error, delta_error)
    )

    print("=" * 50)
    print("AFLC - FUZZY CONTROLLER TEST")
    print("=" * 50)

    print(f"Hata (e): {error}")
    print(f"Hata degisimi (Delta e): {delta_error}")

    print(f"\nKontrol cikti degeri: {result:.5f}")

    print(f"\nAktif kural sayisi: {len(active_rules)}")

    for e_label, de_label, out_label, strength in active_rules:
        print(
            f"IF e={e_label} AND Delta e={de_label}"
            f" THEN {out_label}"
            f" | Aktivasyon={strength:.3f}"
        )

    # Grafik
    fig, ax = plt.subplots(figsize=(10, 5))

    fig.patch.set_facecolor("#FFFDFE")
    ax.set_facecolor("#FCF8FF")

    ax.plot(
        x, y,
        color="#B555ED",
        linewidth=2.5,
        label="Aggregated Fuzzy Output"
    )

    ax.fill_between(
        x, y,
        color="#B555ED",
        alpha=0.22
    )

    ax.axvline(
        result,
        color="#611375",
        linestyle="--",
        linewidth=2,
        label=f"Centroid = {result:.4f}"
    )

    ax.set_title(
        "Fuzzy Inference and Defuzzification",
        color="#70209F",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_xlabel("Normalized Control Output")
    ax.set_ylabel("Membership Degree")

    ax.set_xlim(-2, 2)
    ax.set_ylim(0, 1.05)

    ax.grid(alpha=0.25, linestyle="--")
    ax.legend()

    plt.tight_layout()

    # Kaydet
    base_dir = Path(__file__).resolve().parent.parent
    output_dir = base_dir / "results" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.savefig(
        output_dir / "fuzzy_controller_output.png",
        dpi=300,
        bbox_inches="tight"
    )

    print("\nKontrolcu basariyla calisti!")
    print("Grafik kaydedildi.")

    plt.show()
