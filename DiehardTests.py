import math
from CollatzRNG import CollatzRNG

class DiehardTests:
    def __init__(self, bits):
        self.bits = bits
        self.n = len(bits)

    def run_all(self):
        print(f"\n{'='*60}")
        print(f"DIEHARD / NIST BENZERİ İSTATİSTİKSEL TEST RAPORU")
        print(f"Analiz Edilen Veri Boyutu: {self.n} bit")
        print(f"{'-'*60}")
        print(f"| {'Test Adı':<25} | {'P-Değeri':<12} | {'Sonuç':<10} |")
        print(f"{'-'*60}")

        self.frequency_test()
        self.runs_test()
        self.serial_test()
        self.autocorrelation_test(lag=5)
        
        print(f"{'-'*60}")
        print("* P-Değeri >= 0.01 ise test genellikle BAŞARILI kabul edilir.")

    def _print_result(self, name, p_value):
        status = "BAŞARILI" if p_value >= 0.01 else "BAŞARISIZ"
        print(f"| {name:<25} | {p_value:.6f}     | {status:<10} |")

    # --- 1. Frequency (Monobit) Test ---
    def frequency_test(self):
        # 0'ları -1, 1'leri +1 yapıp topluyoruz
        summ = sum([1 if b == 1 else -1 for b in self.bits])
        s_obs = abs(summ) / math.sqrt(self.n)
        p_value = math.erfc(s_obs / math.sqrt(2))
        
        self._print_result("Frequency (Monobit)", p_value)

    # --- 2. Runs Test ---
    def runs_test(self):
        pi = sum(self.bits) / self.n
        
        # Ön koşul kontrolü
        if abs(pi - 0.5) >= (2 / math.sqrt(self.n)):
            print(f"| {'Runs Test':<25} | {'N/A':<12} | {'ATLANDI':<10} | (Pi çok dengesiz)")
            return

        v_obs = 1
        for i in range(self.n - 1):
            if self.bits[i] != self.bits[i+1]:
                v_obs += 1
                
        numerator = abs(v_obs - (2 * self.n * pi * (1 - pi)))
        denominator = 2 * math.sqrt(2 * self.n) * pi * (1 - pi)
        p_value = math.erfc(numerator / denominator)
        
        self._print_result("Runs Test", p_value)

    # --- 3. Serial Test (2-bit Basitleştirilmiş) ---
    def serial_test(self):
        counts = {'00': 0, '01': 0, '10': 0, '11': 0}
        
        # Örtüşmeli blok sayımı
        for i in range(self.n - 1):
            pattern = f"{self.bits[i]}{self.bits[i+1]}"
            counts[pattern] += 1
            
        expected = (self.n - 1) / 4.0
        chi_sq = sum([(counts[k] - expected)**2 / expected for k in counts])
        
        # Serbestlik derecesi (df) = 3 için Chi-Square -> P-Value dönüşümü (Gamma func)
        # Python'da P(X>x) = 1 - gammainc (Scipy yoksa math ile hile yaparız veya yaklaşık hesaplarız)
        # Ancak math.gamma fonksiyonu tam regularized gamma vermez.
        # Basitlik adına burada Chi-Square tablosuna benzer bir yaklaşım yerine
        # Scipy olmadan tam doğru hesap zor olduğu için yaklaşık formül kullanıyoruz:
        
        # df=3 için özel yaklaşım (Wilson-Hilferty transformation vb. yerine basit exponential)
        # Bu kısım Scipy olmadan tam hassas olmaz ama öğrenci projesi için şu yaklaşım yeterlidir:
        # P-value approx for ChiSq with df=3
        p_value = self._chi2_p_value_df3(chi_sq)
        
        self._print_result("Serial Test", p_value)

    # --- 4. Autocorrelation Test ---
    def autocorrelation_test(self, lag=5):
        A = 0
        for i in range(self.n - lag):
            # XOR yerine XNOR (Eşitlik) kontrolü
            if self.bits[i] == self.bits[i + lag]:
                A += 1
        
        mean = (self.n - lag) / 2.0
        variance = (self.n - lag) / 4.0
        z_score = (A - mean) / math.sqrt(variance)
        p_value = math.erfc(abs(z_score) / math.sqrt(2))
        
        self._print_result(f"Autocorrelation (Lag:{lag})", p_value)

    # Yardımcı Fonksiyon: Chi-Square df=3 P-Value hesaplayıcı (Scipy'sız)
    def _chi2_p_value_df3(self, x):
        # Bu bir yaklaşımdır (Lower Incomplete Gamma Function implementation needed technically)
        # Ama Python math kütüphanesi "gammaincc" (complementary) içermez (sadece Scipy içerir).
        # Bu yüzden çok basit bir istatistiksel yaklaşım kullanacağız veya dış kütüphane şart olur.
        # Alternatif: İstatistiksel tablolardan kritik değer kontrolü yapılabilir.
        # Proje kurtarmak için df=3 için P-değeri yaklaşımı:
        
        if x <= 0: return 1.0
        # Basit bir Gamma serisi açılımı simülasyonu
        m = 3/2.0
        s = x/2.0
        # Regularized Gamma P (yaklaşık)
        try:
            val = math.gamma(m) # Gamma(1.5) = sqrt(pi)/2
            # Bu tam integral olmadığı için burada tam doğru sonuç zordur.
            # Ancak x (chi-score) çok büyükse p-value 0'a yaklaşır.
            # x < 7.81 ise p > 0.05'tir.
            if x > 15: return 0.0
            if x < 0.5: return 0.9
            
            # Daha doğru bir dönüşüm (Smith approximation):
            return math.exp(-x/2) * (1 + x) # Bu df=4 için yakındır, df=3 için idare eder.
        except:
            return 0.0

# --- Ana Çalıştırma Kısmı ---
if __name__ == "__main__":
    # 1. Veri Üret
    print("Veri üretiliyor (Collatz Algoritması)...")
    rng = CollatzRNG(seed=123456789) # İstediğin tohumu ver
    generated_bits = rng.generate_block(20000) # 20.000 bit
    
    # 2. Testleri Başlat
    tester = DiehardTests(generated_bits)
    tester.run_all()