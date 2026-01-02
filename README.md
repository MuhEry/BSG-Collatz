# Collatz Tabanlı Sözde Rastgele Sayı Üreteci (Collatz-PRNG)

Bu proje, matematiksel bir problem olan **Collatz Sanısı (3n+1 Problemi)** yörüngelerindeki kaotik yapıyı kullanarak istatistiksel olarak doğrulanabilir rastgele sayılar (bitler) üretmeyi amaçlayan bir yazılım projesidir.

**Bilgi Sistemleri ve Güvenliği** dersi kapsamında, kriptografik ilkelere uygunluk ve rastgelelik testleri gözetilerek geliştirilmiştir.

---

## 📖 Proje Hakkında

Rastgele sayı üretimi, siber güvenlikten simülasyonlara kadar bilgisayar bilimlerinin temel taşlarından biridir. Bu proje, standart kütüphanelerin deterministik yapılarına alternatif olarak, sayıların **Collatz (Hailstone)** dizisindeki öngörülemez hareketlerinden entropi (düzensizlik) elde eder.

Proje şunları içerir:
- Özgün bir **PRNG (Pseudo-Random Number Generator)** algoritması.
- 4-2-1 döngüsüne karşı geliştirilmiş dinamik tuzlama (salting) mekanizması.
- Üretilen verinin kalitesini ölçen **Frequency, Runs, Serial ve Autocorrelation** test süiti.

---

## 🧮 Algoritma Mantığı

Algoritma, kullanıcıdan veya sistem saatinden alınan bir tohum (seed) değeri ile başlar ve her adımda şu matematiksel fonksiyonu uygular:

$f(n) = \begin{cases} n/2 & \text{eğer } n \equiv 0 \pmod{2} \\ 3n+1 & \text{eğer } n \equiv 1 \pmod{2} \end{cases}$

### Bit Üretim Süreci:
1.  **Bit Çıkarımı (Extraction):** Mevcut durumun mod 2'si alınarak ($n \pmod{2}$) çıktı bitine (0 veya 1) karar verilir.
2.  **Durum Güncelleme:** Sayı çift ise ikiye bölünür, tek ise 3 ile çarpılıp 1 eklenir.
3.  **Döngü Koruması:** Collatz dizisi doğası gereği eninde sonunda 4-2-1 döngüsüne girer. Algoritma, sayı 1'e ulaştığında `Seed + i` değerini kullanarak durumu yeniden karıştırır (Re-seeding) ve döngüden çıkarır.

---

## 📂 Dosya Yapısı

```text
.
├── collatz_rng.py    # Algoritmanın Çekirdek Sınıfı (Generator)
├── diehard_test.py   # İstatistiksel Test Modülü (Frequency, Runs, vb.)
├── README.md         # Proje Dokümantasyonu
├── Çıktı             # Örnek Kod Çıktıları
├── SözdeKod.txt      # Pseudocode
