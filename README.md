# Bulanık Mantık Tabanlı Fotovoltaik Sistemlerde Maksimum Güç Noktası Takibi (MPPT)

**İstanbul Üniversitesi-Cerrahpaşa – Bilgisayar Mühendisliği**

**Ders:** Bulanık Mantık  
**Proje türü:** Dönem Projesi  
**Öğrenci:** Yağmur [Soyadı]  
**Öğrenci Numarası:** [Öğrenci numarası]  
**Teslim Tarihi:** 16 Kasım 2026

---

## 1. Projenin Amacı ve Problem Tanımı

Fotovoltaik (PV) sistemlerde üretilen güç; güneş ışınımı, sıcaklık ve çalışma gerilimi gibi değişkenlere bağlıdır. PV sistemlerin maksimum verimle çalışabilmesi için maksimum güç noktasının (Maximum Power Point – MPP) sürekli olarak takip edilmesi gerekir.

Geleneksel sabit adımlı MPPT yöntemlerinde adım büyüklüğünün seçimi önemli bir problemdir. Büyük adımlar hızlı yakınsama sağlayabilirken maksimum güç noktası çevresindeki salınımları artırabilir. Küçük adımlar ise daha kararlı çalışmasına rağmen değişen çevre koşullarına daha yavaş tepki verebilir.

Bu projede, bulanık mantık kullanılarak MPPT kontrolünün geliştirilmesi ve farklı kontrol yaklaşımlarının karşılaştırılması amaçlanmıştır.

Çalışmada üç yöntem değerlendirilmiştir:

1. Sabit adımlı MPPT
2. Bulanık mantık destekli MPPT
3. Önerilen adaptif adımlı ve ölü bölgeli (deadband) MPPT

## 2. Referans Makale

Çalışmanın bilimsel dayanağı aşağıdaki makaledir:

Elnaghi ve diğerleri (2025). *Experimental validation of an adaptive fuzzy logic controller for MPPT of grid connected PV system.* Scientific Reports, 15, Article 27173.

**DOI:** https://doi.org/10.1038/s41598-025-10188-7

Referans çalışmada adaptif bulanık mantık kontrolünün PV sistemlerde MPPT performansını geliştirmeye yönelik kullanımı incelenmektedir.

Bu projede makaledeki bulanık kontrol yaklaşımından yararlanılmış; üyelik fonksiyonları, kural tabanı, bulanık çıkarım ve durulaştırma süreçleri Python ortamında incelenmiştir.

**Kapsam ayrımı:** Bu proje referans makalenin deneysel AFLC-PI sisteminin eksiksiz yeniden üretimi değildir. Makaledeki temel prensiplerden hareketle sadeleştirilmiş bir PV modeli üzerinde sayısal karşılaştırmalar gerçekleştirilmiştir.

## 3. Kullanılan Yöntem

### 3.1. Bulanık mantık denetleyicisi

Bulanık denetleyicide iki giriş değişkeni bulunmaktadır:

- **e:** Hata
- **Δe:** Hatanın değişimi

Her iki giriş değişkeni de [-1, 1] aralığında normalize edilmiştir.

Girişler için yedi dilsel bulanık küme tanımlanmıştır:

- NB: Negative Big
- NM: Negative Medium
- NS: Negative Small
- Z: Zero
- PS: Positive Small
- PM: Positive Medium
- PB: Positive Big

Kontrol çıkışı için dokuz üyelik fonksiyonu kullanılmıştır.

### 3.2. Üyelik fonksiyonları

Bulanık değişkenleri temsil etmek için üçgensel, omuz ve uygun bölgelerde trapez üyelik fonksiyonlarından yararlanılmıştır.

Üyelik dereceleri 0 ile 1 arasında değer almaktadır.

### 3.3. Kural tabanı

Sistemde iki girişin yedişer bulanık kümesi bulunduğundan toplam:

**7 × 7 = 49 bulanık kural**

kullanılmıştır.

Kurallar, hata ve hata değişiminin farklı kombinasyonlarına göre kontrol çıktısını belirlemektedir.

### 3.4. Mamdani bulanık çıkarım

Bulanık çıkarım sisteminde Mamdani min–max yaklaşımı uygulanmıştır.

Her kuralın ateşlenme derecesi:

**α = min(μ(e), μ(Δe))**

şeklinde hesaplanmaktadır.

Kuralların sonuçları maksimum operatörü kullanılarak birleştirilmektedir.

### 3.5. Durulaştırma

Birleştirilen bulanık çıkış kümesi, ağırlık merkezi yöntemi (centroid defuzzification) ile tek bir sayısal kontrol çıktısına dönüştürülmektedir.

Bu işlem, denetleyicinin MPPT algoritmasında kullanılabilecek sayısal bir kontrol değeri üretmesini sağlar.

## 4. PV Modeli ve Kullanılan Veri

Çalışmada SPR-305 panel parametrelerinden yararlanan sadeleştirilmiş bir fotovoltaik model kullanılmıştır.

Temel model parametreleri:

| Parametre | Değer |
|---|---|
| Nominal maksimum güç | 305 W |
| Açık devre gerilimi (Voc) | 64,2 V |
| Kısa devre akımı (Isc) | 5,96 A |
| Maksimum güç noktası gerilimi (Vmp) | 54,6 V |
| Maksimum güç noktası akımı (Imp) | 5,56 A |
| Sabit sıcaklık | 25°C |

Modelde gerilim, akım ve güç arasındaki ilişkiler kullanılarak maksimum güç noktası hesaplanmaktadır.

### Veri kaynağı ve senaryo

Bu çalışmada harici bir gerçek zamanlı ölçüm veri seti kullanılmamıştır. Deney verileri, Python ile oluşturulan sayısal PV modeli ve önceden belirlenen güneş ışınımı senaryosu üzerinden üretilmiştir.

| Zaman aralığı | Işınım |
|---|---|
| 0–1 saniye | 700 W/m² |
| 1–2 saniye | 900 W/m² |
| 2–3 saniye | 1100 W/m² |
| 3–4 saniye | 800 W/m² |

Toplam simülasyon süresi 4 saniye, örnekleme aralığı 0,02 saniye ve başlangıç çalışma gerilimi 30 V olarak belirlenmiştir.

Bu senaryo, değişen ışınım koşullarında MPPT algoritmalarının davranışlarını karşılaştırmak amacıyla kullanılmıştır.

## 5. Baseline ve Reproduction Çalışmaları

### 5.1. Sabit adımlı MPPT

İlk karşılaştırma yöntemi, 0,5 V adım büyüklüğüne sahip sabit adımlı MPPT yaklaşımıdır.

Bu yöntem, diğer kontrol yaklaşımlarının sonuçlarını değerlendirmek için referans (baseline) olarak kullanılmıştır.

### 5.2. Bulanık mantık destekli MPPT

İkinci yaklaşımda, bulanık mantık denetleyicisinden elde edilen kontrol çıktısı MPPT adım büyüklüğünün ayarlanmasında kullanılmıştır.

Bu yöntem ile geleneksel sabit adımlı yöntemin performansı karşılaştırılmıştır.

### 5.3. Referans çalışmanın yeniden üretim kapsamı

Referans makaledeki bulanık kontrol prensiplerinin yazılım ortamında incelenmesine odaklanılmıştır.

Üyelik fonksiyonları, 49 kurallı yapı, Mamdani çıkarım ve centroid durulaştırma uygulanmıştır.

Ancak referans çalışmadaki fiziksel deney düzeneği, güç elektroniği bileşenleri ve tam AFLC-PI mimarisi yeniden oluşturulmamıştır. Bu nedenle sonuçlar makaledeki deneysel ölçümlerle doğrudan eşdeğer kabul edilmemelidir.

## 6. Geliştirilen Özgün Yöntem

Proje kapsamında bulanık mantık destekli MPPT yaklaşımına ek olarak adaptif adım büyüklüğü ve ölü bölge mekanizmasını birleştiren bir yöntem geliştirilmiştir.

Önerilen yöntemde:

- Hata büyüklüğü kontrol adımının belirlenmesinde kullanılmaktadır.
- Bulanık kontrol çıktısı adaptif adım hesabına katkıda bulunmaktadır.
- Maksimum güç noktası yakınında çok küçük güç değişimleri için deadband uygulanmaktadır.
- Böylece kararlı çalışma bölgesinde gereksiz kontrol hareketlerinin azaltılması hedeflenmektedir.

Bu yaklaşımın temel amacı, değişen ışınım koşullarına tepki verme yeteneğini korurken maksimum güç noktası çevresindeki salınımları sınırlamaktır.

**Özgün katkı:** Baseline ve bulanık destekli yönteme ek olarak adaptif adım ve deadband mekanizmalarının aynı sayısal deney ortamında uygulanması ve üç yaklaşımın nicel olarak karşılaştırılmasıdır.

Bu yöntem, küresel olarak yeni olduğu kanıtlanmış bir kontrol algoritması olarak değil, dönem projesi kapsamında geliştirilen ve değerlendirilen bir yöntem olarak sunulmaktadır.

## 7. Deneysel Kurulum ve Değerlendirme Metrikleri

Simülasyonlar Python ortamında gerçekleştirilmiştir.

Kontrol yöntemlerinin performansı aşağıdaki metriklerle değerlendirilmiştir:

- **MAE:** Ortalama mutlak güç takip hatası
- **RMSE:** Kök ortalama kare güç takip hatası
- **Tracking Efficiency:** Sayısal maksimum güç takip verimi

MAE ve RMSE değerlerinin düşük olması, referans maksimum güce daha yakın takip gerçekleştirildiğini gösterir.

Takip veriminin yüksek olması ise simülasyon boyunca erişilebilir maksimum gücün daha büyük bölümünün takip edilebildiğini ifade eder.

Burada kullanılan takip verimi, fiziksel DC-DC dönüştürücü veya inverter verimi değildir.

## 8. Deneysel Sonuçlar

| Yöntem | MAE (W) | RMSE (W) | Takip Verimi (%) |
|---|---:|---:|---:|
| Sabit Adımlı MPPT | 9,6044 | 23,5778 | 95,49 |
| Bulanık Destekli MPPT | 3,1306 | 13,1785 | 98,55 |
| **Önerilen Yöntem** | **2,7265** | **12,6972** | **98,72** |

Önerilen yöntem, bulanık destekli MPPT ile karşılaştırıldığında:

- MAE değerinde yaklaşık **%12,91 azalma**
- RMSE değerinde yaklaşık **%3,65 azalma**
- Takip veriminde **0,17 yüzde puan artış**

sağlamıştır.

Bu sonuçlar kullanılan PV modeli ve ışınım senaryosu için geçerlidir.

Simülasyon çıktıları `results/tables/` ve grafikler `results/figures/` klasörlerinde bulunmaktadır.

## 9. Proje Dosya Yapısı

```text
Fuzzy-MPPT-Project/
├── src/
│   ├── membership.py
│   ├── output_membership.py
│   ├── rule_base.py
│   ├── fuzzy_controller.py
│   ├── pv_model.py
│   ├── mppt_simulation.py
│   └── proposed_experiment.py
├── results/
│   ├── figures/
│   └── tables/
│       ├── mppt_results.csv
│       ├── proposed_results.csv
│       └── method_comparison.csv
├── demo.py
├── requirements.txt
├── .gitignore
└── README.md
```

`src/` klasöründe kaynak kodlar, `results/` klasöründe deney çıktıları ve `demo.py` dosyasında etkileşimli bulanık denetleyici gösterimi bulunmaktadır.

## 10. Kurulum ve Gereksinimler

**Programlama dili:** Python

**Temel kütüphaneler:**

- NumPy
- Matplotlib

Projenin bağımlılıkları `requirements.txt` dosyasında belirtilmiştir.

### 10.1. Repository'yi indirme

```bash
git clone https://github.com/yagmur-kyc/Fuzzy-MPPT-Project.git
cd Fuzzy-MPPT-Project
```

### 10.2. Sanal ortam oluşturma

```bash
python -m venv .venv
```

Windows PowerShell üzerinde etkinleştirme:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 10.3. Kütüphaneleri yükleme

```bash
python -m pip install -r requirements.txt
```

## 11. Projeyi Çalıştırma

Komutlar proje ana klasöründe çalıştırılmalıdır.

**Üyelik fonksiyonları ve bulanık çıkarım:**

```bash
python src/fuzzy_controller.py
```

**Sabit adımlı ve bulanık destekli MPPT karşılaştırması:**

```bash
python src/mppt_simulation.py
```

**Önerilen yöntem ve üç algoritmanın karşılaştırması:**

```bash
python src/proposed_experiment.py
```

**Etkileşimli canlı demo:**

```bash
python demo.py
```

Canlı demoda kullanıcı, `e` ve `Δe` girişlerini [-1, 1] aralığında değiştirerek bulanık denetleyicinin ürettiği centroid kontrol çıktısını inceleyebilir.

## 12. Yeniden Üretilebilirlik

Deney sonuçlarını yeniden elde etmek için:

1. Repository'yi bilgisayara indirin.
2. Python sanal ortamı oluşturun.
3. `requirements.txt` dosyasındaki bağımlılıkları yükleyin.
4. Önce `mppt_simulation.py` dosyasını çalıştırın.
5. Ardından `proposed_experiment.py` dosyasını çalıştırın.
6. Terminal çıktılarındaki MAE, RMSE ve takip verimi değerlerini Bölüm 8'deki sonuçlarla karşılaştırın.
7. Oluşturulan grafik ve CSV dosyalarını `results/` klasöründe inceleyin.

Dış veri setine ihtiyaç duyulmamaktadır; kullanılan ışınım senaryosu model içerisinde tanımlanmıştır.

## 13. Sınırlılıklar

Çalışmanın başlıca sınırlılıkları şunlardır:

- PV sistemi sadeleştirilmiş bir sayısal modelle temsil edilmiştir.
- Sıcaklık 25°C'de sabit kabul edilmiştir.
- Gerçek PV paneli veya fiziksel MPPT donanımı kullanılmamıştır.
- DC-DC dönüştürücü ve şebeke bağlantılı inverter ayrıntılı olarak modellenmemiştir.
- Deneyler belirli bir dört saniyelik ışınım senaryosuyla sınırlandırılmıştır.
- Ölçülen performans değerleri donanım deneyleriyle doğrulanmamıştır.
- Farklı parametreler ve daha kapsamlı senaryolar için ek doğrulama gereklidir.

Bu nedenle elde edilen sonuçlar, önerilen yaklaşımın tanımlanan simülasyon koşullarındaki performansını göstermektedir.

## 14. Sonuç

Bu projede bulanık mantık tabanlı kontrolün PV sistemlerde maksimum güç noktası takibine katkısı incelenmiştir.

Sabit adımlı MPPT, bulanık destekli MPPT ve önerilen adaptif MPPT yöntemi karşılaştırılmıştır.

Deneyler sonucunda önerilen yöntem, incelenen senaryoda en düşük MAE ve RMSE değerlerini ve en yüksek sayısal takip verimini sağlamıştır.

Çalışma, bulanık mantık sistemlerinin kontrol problemlerinde uygulanmasını ve elde edilen sonuçların sayısal olarak karşılaştırılmasını göstermektedir.

## 15. Kaynakça

1. Elnaghi ve diğerleri (2025). *Experimental validation of an adaptive fuzzy logic controller for MPPT of grid connected PV system.* Scientific Reports, 15, Article 27173. https://doi.org/10.1038/s41598-025-10188-7

2. NumPy Documentation. https://numpy.org/doc/

3. Matplotlib Documentation. https://matplotlib.org/stable/

---

**Not:** Bu repository akademik bir dönem projesi kapsamında hazırlanmıştır. Referans makalenin deneysel sisteminin birebir kopyası değildir.
