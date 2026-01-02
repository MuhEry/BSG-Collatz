import time

class CollatzRNG:
    def __init__(self, seed=None):
        """
        Başlangıç tohumunu ayarlar. Eğer seed verilmezse 
        sistem saatini kullanır.
        """
        if seed is None:
            # Sistem zamanını milisaniye cinsinden alıp int'e çeviriyoruz
            self.state = int(time.time() * 1000)
        else:
            self.state = seed
        
        self.initial_seed = self.state

    def next_bit(self):
        """
        Collatz algoritmasına göre bir sonraki biti üretir (0 veya 1).
        """
        # 1. Biti al (Sayının tek mi çift mi olduğu)
        bit = self.state % 2
        
        # 2. Collatz Adımı
        if self.state % 2 == 0:
            self.state = self.state // 2
        else:
            self.state = 3 * self.state + 1
            
        # 3. 4-2-1 Döngüsü Koruması
        # Eğer 1'e ulaştıysa, rastgeleliği devam ettirmek için 
        # state'i başlangıç tohumuyla karıştırarak yeniden başlat.
        if self.state <= 1:
            self.state = (self.state + self.initial_seed + 12345) 
            # Not: Basit bir toplama yerine daha karmaşık bir karıştırma da yapılabilir.

        return bit

    def generate_block(self, size):
        """
        Belirtilen boyutta (size) bir bit listesi döndürür.
        """
        bits = []
        for _ in range(size):
            bits.append(self.next_bit())
        return bits

# --- Test Amaçlı Çalıştırma (Doğrudan bu dosya çalıştırılırsa) ---
if __name__ == "__main__":
    rng = CollatzRNG(seed = int(time.time() * 1000))
    print(f"Kullanılan Seed: {rng.initial_seed}")
    print("Örnek 20 Bit:", rng.generate_block(20))  