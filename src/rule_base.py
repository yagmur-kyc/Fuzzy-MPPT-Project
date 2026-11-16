
# ==========================================
# BULANIK MANTIK DONEM PROJESI
# AFLC - 49 KURALLI BULANIK KURAL TABANI
#
# Referans:
# Elnaghi et al. (2025)
# Experimental validation of an adaptive
# fuzzy logic controller for MPPT
#
# Makale: Table 2, Sayfa 10
# ==========================================


# ==========================================
# 1. GIRIS DEGISKENLERI
# ==========================================

# e = Error (Hata)
# Makaledeki sutun sirasi

error_labels = [
    "NS", "NM", "NB", "PB", "PS", "PM", "Z"
]


# Delta e = Change of Error
# Makaledeki satir sirasi

delta_error_labels = [
    "NB",
    "PS",
    "NS",
    "NM",
    "Z",
    "PB",
    "PM"
]


# ==========================================
# 2. BULANIK KURAL MATRISI
# ==========================================

# Her satir Delta e degerini,
# her sutun e degerini temsil eder.
#
# Makaledeki Tablo 2'den alinmistir.

rule_matrix = [

    # e: NS    NM     NB    PB     PS     PM     Z

    ["NB",  "NB",  "NB",  "Z",   "NS",  "NVS", "NM"],

    ["Z",   "NVS", "NS",  "PB",  "PS",  "PM",  "PVS"],

    ["NS",  "NM",  "NB",  "PS",  "Z",   "PVS", "NVS"],

    ["NM",  "NB",  "NB",  "PVS", "NVS", "Z",   "NS"],

    ["NVS", "NS",  "NM",  "PM",  "PVS", "PS",  "Z"],

    ["PS",  "PVS", "Z",   "PB",  "PB",  "PB",  "PM"],

    ["PVS", "Z",   "NVS", "PB",  "PM",  "PB",  "PS"]

]


# ==========================================
# 3. KURAL SAYISINI KONTROL ET
# ==========================================

def count_rules():
    """Toplam bulanık kural sayisini hesaplar."""

    return sum(len(row) for row in rule_matrix)


# ==========================================
# 4. KURAL SORGULAMA FONKSIYONU
# ==========================================

def get_rule(error_label, delta_error_label):
    """
    Girilen iki dilsel degere gore
    bulanık kural sonucunu dondurur.

    Parametreler:
        error_label: e
        delta_error_label: Delta e

    Ornek:
        e = NB
        Delta e = NB

    Cikti:
        NB
    """

    if error_label not in error_labels:
        raise ValueError(
            f"Gecersiz hata etiketi: {error_label}"
        )

    if delta_error_label not in delta_error_labels:
        raise ValueError(
            f"Gecersiz hata degisimi: {delta_error_label}"
        )

    column_index = error_labels.index(error_label)

    row_index = delta_error_labels.index(
        delta_error_label
    )

    result = rule_matrix[row_index][column_index]

    return result


# ==========================================
# 5. TUM KURALLARI YAZDIR
# ==========================================

def print_all_rules():
    """49 bulanık kuralin tamamini yazdirir."""

    rule_number = 1

    for row_index, delta_label in enumerate(
        delta_error_labels
    ):

        for col_index, error_label in enumerate(
            error_labels
        ):

            output_label = rule_matrix[
                row_index
            ][col_index]

            print(
                f"Rule {rule_number:02d}: "
                f"IF e is {error_label} "
                f"AND Delta e is {delta_label} "
                f"THEN output is {output_label}"
            )

            rule_number += 1


# ==========================================
# 6. KURAL TABLOSUNU YAZDIR
# ==========================================

def print_rule_table():
    """Kural matrisini tablo halinde gosterir."""

    print("\nAFLC FUZZY RULE TABLE\n")

    header = "Delta e / e".ljust(14)

    for label in error_labels:
        header += label.center(8)

    print(header)
    print("-" * len(header))

    for row_index, delta_label in enumerate(
        delta_error_labels
    ):

        row_text = delta_label.ljust(14)

        for output in rule_matrix[row_index]:
            row_text += output.center(8)

        print(row_text)


# ==========================================
# 7. KURAL TABANINI DOGRULA
# ==========================================

def validate_rule_base():
    """Kural matrisinin yapisal kontrolu."""

    assert len(error_labels) == 7
    assert len(delta_error_labels) == 7
    assert len(rule_matrix) == 7

    for row in rule_matrix:
        assert len(row) == 7

    # Cikti etiketlerini kontrol et
    output_labels = {
        "NB", "NM", "NS", "NVS",
        "Z", "PVS", "PS", "PM", "PB"
    }

    for row in rule_matrix:
        for output in row:
            assert output in output_labels

    print("Kural tabani dogrulamasi basarili!")


# ==========================================
# 8. PROGRAMI CALISTIR
# ==========================================

if __name__ == "__main__":

    print("=" * 55)
    print("AFLC - FUZZY LOGIC CONTROLLER")
    print("49 RULE BASE IMPLEMENTATION")
    print("=" * 55)

    # Dogrulama
    validate_rule_base()

    # Kural sayisi
    total_rules = count_rules()

    print("\nToplam kural sayisi:", total_rules)

    # Ornek kurallar
    print("\nORNEK KURAL TESTLERI")
    print("-" * 35)

    result1 = get_rule("NB", "NB")
    print("e=NB, Delta e=NB ->", result1)

    result2 = get_rule("Z", "Z")
    print("e=Z, Delta e=Z ->", result2)

    result3 = get_rule("PB", "PS")
    print("e=PB, Delta e=PS ->", result3)

    # Kural tablosu
    print_rule_table()

    # Tum kurallar
    print("\nTUM BULANIK KURALLAR")
    print("-" * 55)

    print_all_rules()

    print("\nProgram basariyla tamamlandi!")
