using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

class CollatzCipher
{
    static long _currentCollatzState;

    static void Main(string[] args)
    {
        Console.WriteLine("=== COLLATZ ŞİFRELEME SİMÜLASYONU ===");
        
        Console.Write("Şifrelenecek Mesaj: ");
        string plainText = Console.ReadLine();

        Console.Write("Başlangıç Tohumu (Seed - Sayı): ");
        long seed = long.Parse(Console.ReadLine());
        _currentCollatzState = seed;

        Console.WriteLine("\n--- ADIM 1: ŞİFRELEME SÜRECİ ---");
        string cipherTextHex = EncryptVisual(plainText);
        
        Console.WriteLine($"\n--> SONUÇ (Hex): {cipherTextHex}");

        Console.WriteLine("\n--- ADIM 2: DEŞİFRELEME SÜRECİ ---");
        _currentCollatzState = seed; 
        string decryptedText = Decrypt(cipherTextHex);
        Console.WriteLine($"--> ÇÖZÜLEN MESAJ: {decryptedText}");

        Console.ReadLine();
    }

    static string EncryptVisual(string plainText)
    {
        byte[] messageBytes = Encoding.UTF8.GetBytes(plainText);
        List<int> messageBits = BytesToBits(messageBytes);
        
        Console.WriteLine($"1. Mesajın Bit Hali ({messageBits.Count} bit):");
        Console.WriteLine(string.Join("", messageBits));

        List<int> keyBits = GenerateCollatzKeyStream(messageBits.Count);
        Console.WriteLine($"\n2. Collatz & Von Neumann ile Üretilen Anahtar:");
        Console.WriteLine(string.Join("", keyBits));

        List<int> xoredBits = new List<int>();
        for (int i = 0; i < messageBits.Count; i++)
        {
            xoredBits.Add(messageBits[i] ^ keyBits[i]);
        }
        Console.WriteLine($"\n3. XOR İşlemi Sonrası (Gizlilik Katmanı):");
        Console.WriteLine(string.Join("", xoredBits));

        int midPoint = xoredBits.Count / 2;
        List<int> leftHalf = xoredBits.GetRange(0, midPoint);
        List<int> rightHalf = xoredBits.GetRange(midPoint, xoredBits.Count - midPoint);

        if (leftHalf.Count > 0)
        {
            int first = leftHalf[0];
            leftHalf.RemoveAt(0);
            leftHalf.Add(first);
        }

        if (rightHalf.Count > 0)
        {
            int last = rightHalf[rightHalf.Count - 1];
            rightHalf.RemoveAt(rightHalf.Count - 1);
            rightHalf.Insert(0, last);
        }

        List<int> finalBits = new List<int>();
        finalBits.AddRange(leftHalf);
        finalBits.AddRange(rightHalf);

        Console.WriteLine($"\n4. İkiye Bölüp Kaydırma Sonrası (Karıştırma Katmanı):");
        Console.WriteLine(string.Join("", finalBits));

        return BitsToHex(finalBits);
    }

    static string Decrypt(string cipherHex)
    {
        List<int> cipherBits = HexToBits(cipherHex);
        
        int midPoint = cipherBits.Count / 2;
        List<int> leftHalf = cipherBits.GetRange(0, midPoint);
        List<int> rightHalf = cipherBits.GetRange(midPoint, cipherBits.Count - midPoint);

        if (leftHalf.Count > 0)
        {
            int last = leftHalf[leftHalf.Count - 1];
            leftHalf.RemoveAt(leftHalf.Count - 1);
            leftHalf.Insert(0, last);
        }

        if (rightHalf.Count > 0)
        {
            int first = rightHalf[0];
            rightHalf.RemoveAt(0);
            rightHalf.Add(first);
        }

        List<int> unshiftedBits = new List<int>();
        unshiftedBits.AddRange(leftHalf);
        unshiftedBits.AddRange(rightHalf);

        List<int> keyBits = GenerateCollatzKeyStream(unshiftedBits.Count);

        List<int> plainBits = new List<int>();
        for (int i = 0; i < unshiftedBits.Count; i++)
        {
            plainBits.Add(unshiftedBits[i] ^ keyBits[i]);
        }

        byte[] plainBytes = BitsToBytes(plainBits);
        return Encoding.UTF8.GetString(plainBytes).TrimEnd('\0');
    }

    static List<int> GenerateCollatzKeyStream(int requiredLength)
    {
        List<int> keyStream = new List<int>();
        while (keyStream.Count < requiredLength)
        {
            long val1 = CollatzStep();
            long val2 = CollatzStep();
            int bit1 = (int)(val1 % 2);
            int bit2 = (int)(val2 % 2);

            if (bit1 == 0 && bit2 == 1) keyStream.Add(1);
            else if (bit1 == 1 && bit2 == 0) keyStream.Add(0);
        }
        return keyStream;
    }

    static long CollatzStep()
    {
        if (_currentCollatzState <= 1) _currentCollatzState = 9999; 
        if (_currentCollatzState % 2 == 0) _currentCollatzState /= 2;
        else _currentCollatzState = (3 * _currentCollatzState) + 1;
        return _currentCollatzState;
    }

    static List<int> BytesToBits(byte[] bytes)
    {
        List<int> bits = new List<int>();
        foreach (byte b in bytes)
        {
            for (int i = 7; i >= 0; i--) bits.Add((b >> i) & 1);
        }
        return bits;
    }

    static byte[] BitsToBytes(List<int> bits)
    {
        int numBytes = (bits.Count + 7) / 8;
        byte[] bytes = new byte[numBytes];
        for (int i = 0; i < bits.Count; i++)
        {
            if (bits[i] == 1) bytes[i / 8] |= (byte)(1 << (7 - (i % 8)));
        }
        return bytes;
    }

    static string BitsToHex(List<int> bits)
    {
        byte[] bytes = BitsToBytes(bits);
        return BitConverter.ToString(bytes).Replace("-", "");
    }

    static List<int> HexToBits(string hex)
    {
        int numberChars = hex.Length;
        byte[] bytes = new byte[numberChars / 2];
        for (int i = 0; i < numberChars; i += 2) bytes[i / 2] = Convert.ToByte(hex.Substring(i, 2), 16);
        return BytesToBits(bytes);
    }
}