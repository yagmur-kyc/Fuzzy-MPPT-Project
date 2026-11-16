
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from fuzzy_controller import fuzzy_controller


print("=" * 55)
print("BULANIK MANTIK MPPT - CANLI DEMO")
print("49 Kural | Mamdani Min-Max | Centroid")
print("=" * 55)

print("\nİstenilen hata degerleri.")
print("Gecerli aralik: -1 ile +1")
print("Cikmak icin q yazin.\n")


while True:
    try:
        giris_e = input("Hata (e) = ").strip()

        if giris_e.lower() == "q":
            break

        giris_de = input("Hata degisimi (Delta e) = ").strip()

        if giris_de.lower() == "q":
            break

        e = float(giris_e.replace(",", "."))
        de = float(giris_de.replace(",", "."))

        if not (-1 <= e <= 1 and -1 <= de <= 1):
            print("\nHATA: Degerler -1 ile 1 arasinda olmali.\n")
            continue

        # Mevcut projedeki gercek kontrolcu
        result = fuzzy_controller(e, de)

        if isinstance(result, (tuple, list)):
            u = float(result[0])
            active_rules = result[3] if len(result) > 3 else None
        else:
            u = float(result)
            active_rules = None

        print("\n" + "-" * 55)
        print("BULANIK KONTROLCU SONUCU")
        print("-" * 55)

        print(f"Girilen e       : {e:+.4f}")
        print(f"Girilen Delta e : {de:+.4f}")
        print(f"Centroid u      : {u:+.6f}")

        if active_rules is not None:
            print(f"\nAktif kural sayisi: {len(active_rules)}")
            for rule in active_rules:
                print(" ", rule)

        if u > 0.00001:
            print("\nYorum: Pozitif kontrol ciktisi.")
        elif u < -0.00001:
            print("\nYorum: Negatif kontrol ciktisi.")
        else:
            print("\nYorum: Sifira yakin kontrol ciktisi.")

        print("\nYeni deger girebilirsiniz.\n")

    except ValueError:
        print("\nHATA: Lutfen sayisal bir deger girin.\n")

    except Exception as error:
        print(f"\nKontrolcu hatasi: {error}\n")


print("\nCanli demo tamamlandi.")
