```python
import math
import sys
import time
from decimal import Decimal, getcontext

class HesapMakinesi:
    def __init__(self):
        self.history = []
        self.memory = 0
        self.getcontext().prec = 10

    def display_menu(self):
        print("\n" + "="*50)
        print("  BİLGİSAYARLI HESAP MAKİNESİ".center(50))
        print("="*50)
        print("1. Temel İşlemler (Toplama, Çıkarma, Çarpma, Bölme)")
        print("2. Karekök ve Kuvvet Alma")
        print("3. Üslü Sayılar ve Logaritma")
        print("4. Trigonometrik Fonksiyonlar")
        print("5. Matris İşlemleri")
        print("6. Karmaşık Sayılar")
        print("7. Yüzde Hesaplama")
        print("8. Birim Dönüştürücü")
        print("9. Hafıza Fonksiyonları")
        print("10. Geometri Hesaplamaları")
        print("11. İstatistiksel İşlemler")
        print("12. Finansal Hesaplamalar")
        print("13. Programcı Hesap Makinesi (İkilik, Sekizlik, Onaltılık)")
        print("14. Dilim Hesaplama")
        print("15. Tarih Hesaplamaları")
        print("16. Geçmişi Görüntüle")
        print("17. Belleği Temizle")
        print("0. Çıkış")
        print("="*50)

    def basic_operations(self):
        print("\n" + "-"*50)
        print("  TEMEL İŞLEMLER".center(50))
        print("-"*50)
        print("1. Toplama")
        print("2. Çıkarma")
        print("3. Çarpma")
        print("4. Bölme")
        print("5. Mod Alma")
        print("6. Faktöriyel")
        print("0. Geri Dön")
        print("-"*50)

        try:
            choice = int(input("İşlem seçiniz (0-6): "))
            if choice == 0:
                return

            num1 = self.get_number_input("İlk sayıyı girin: ")
            num2 = self.get_number_input("İkinci sayıyı girin: ")

            if choice == 1:
                result = num1 + num2
                operation = f"{num1} + {num2} = {result}"
            elif choice == 2:
                result = num1 - num2
                operation = f"{num1} - {num2} = {result}"
            elif choice == 3:
                result = num1 * num2
                operation = f"{num1} × {num2} = {result}"
            elif choice == 4:
                if num2 == 0:
                    print("Hata: Sıfıra bölme yapılamaz!")
                    return
                result = num1 / num2
                operation = f"{num1} ÷ {num2} = {result}"
            elif choice == 5:
                if num2 == 0:
                    print("Hata: Sıfıra mod alma yapılamaz!")
                    return
                result = num1 % num2
                operation = f"{num1} mod {num2} = {result}"
            elif choice == 6:
                if num1 < 0:
                    print("Hata: Negatif sayıların faktöriyeli alınamaz!")
                    return
                result = math.factorial(int(num1))
                operation = f"{int(num1)}! = {result}"

            print(f"\nSonuç: {operation}")
            self.history.append(operation)
        except ValueError:
            print("Hata: Geçersiz giriş! Lütfen sayı giriniz.")
        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu: {e}")

    def root_and_power(self):
        print("\n" + "-"*50)
        print("  KAREKÖK VE KUVVET ALMA".center(50))
        print("-"*50)
        print("1. Karekök")
        print("2. Küp Kök")
        print("3. Yninci Kök")
        print("4. Kuvvet Alma")
        print("5. 10'un Kuvveti")
        print("6. e'nin Kuvveti")
        print("0. Geri Dön")
        print("-"*50)

        try:
            choice = int(input("İşlem seçiniz (0-6): "))
            if choice == 0:
                return

            if choice in [1, 2, 3, 4]:
                num = self.get_number_input("Sayıyı girin: ")
            if choice in [3, 5, 6]:
                num2 = self.get_number_input("Üs değeri girin: ")

            if choice == 1:
                if num < 0:
                    print("Hata: Negatif sayının karekökü alınamaz!")
                    return
                result = math.sqrt(num)
                operation = f"√{num} = {result}"
            elif choice == 2:
                if num < 0:
                    print("Hata: Negatif sayının küp kökü alınamaz!")
                    return
                result = num ** (1/3)
                operation = f"∛{num} = {result}"
            elif choice == 3:
                if num < 0 and num2 % 2 == 0:
                    print("Hata: Negatif sayının çift dereceli kökü alınamaz!")
                    return
                result = num ** (1/num2)
                operation = f"{num}^(1/{num2}) = {result}"
            elif choice == 4:
                result = num ** num2
                operation = f"{num}^{num2} = {result}"
            elif choice == 5:
                result = 10 ** num2
                operation = f"10^{num2} = {result}"
            elif choice == 6:
                result = math.exp(num2)
                operation = f"e^{num2} = {result}"

            print(f"\nSonuç: {operation}")
            self.history.append(operation)
        except ValueError:
            print("Hata: Geçersiz giriş! Lütfen sayı giriniz.")
        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu: {e}")

    def exponential_and_logarithm(self):
        print("\n" + "-"*50)
        print("  ÜSLÜ SAYILAR VE LOGARİTMA".center(50))
        print("-"*50)
        print("1. Doğal Logaritma (ln)")
        print("2. 10 Tabanlı Logaritma (log10)")
        print("3. Tabanlı Logaritma")
        print("4. e Tabanlı Üstel Fonksiyon")
        print("5. 10 Tabanlı Üstel Fonksiyon")
        print("6. Yninci Kuvvet")
        print("0. Geri Dön")
        print("-"*50)

        try:
            choice = int(input("İşlem seçiniz (0-6): "))
            if choice == 0:
                return

            if choice in [3, 6]:
                num = self.get_number_input("Tabanı girin: ")
                num2 = self.get_number_input("Üstel değeri girin: ")
            else:
                num = self.get_number_input("Sayıyı girin: ")

            if choice == 1:
                if num <= 0:
                    print("Hata: Logaritma sadece pozitif sayılar için tanımlıdır!")
                    return
                result = math.log(num)
                operation = f"ln({num}) = {result}"
            elif choice == 2:
                if num <= 0:
                    print("Hata: Logaritma sadece pozitif sayılar için tanımlıdır!")
                    return
                result = math.log10(num)
                operation = f"log10({num}) = {result}"
            elif choice == 3:
                if num <= 0 or num2 <= 0 or num == 1:
                    print("Hata: Geçersiz giriş! Taban 0'dan büyük ve 1'den farklı olmalı, sayı pozitif olmalıdır.")
                    return
                result = math.log(num2, num)
                operation = f"log_{num}({num2}) = {result}"
            elif choice == 4:
                result = math.exp(num)
                operation = f"e^{num} = {result}"
            elif choice == 5:
                result = 10 ** num
                operation = f"10^{num} = {result}"
            elif choice == 6:
                result = num ** num2
                operation = f"{num}^{num2} = {result}"

            print(f"\nSonuç: {operation}")
            self.history.append(operation)
        except ValueError:
            print("Hata: Geçersiz giriş! Lütfen sayı giriniz.")
        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu: {e}")

    def trigonometric_functions(self):
        print("\n" + "-"*50)
        print("  TRİGONOMETRİK FONKSİYONLAR".center(50))
        print("-"*50)
        print("1. Sinüs (sin)")
        print("2. Kosinüs (cos)")
        print("3. Tanjant (tan)")
        print("4. Kotanjant (cot)")
        print("5. Sekant (sec)")
        print("6. Kosekant (csc)")
        print("7. Ters Trigonometrik (arcsin, arccos, arctan)")
        print("0. Geri Dön")
        print("-"*50)

        try:
            choice = int(input("İşlem seçiniz (0-7): "))
            if choice == 0:
                return

            num = self.get_number_input("Açısı girin (derece cinsinden): ")
            num_rad = math.radians(num)

            if choice == 1:
                result = math.sin(num_rad)
                operation = f"sin({num}°) = {result}"
            elif choice == 2:
                result = math.cos(num_rad)
                operation = f"cos({num}°) = {result}"
            elif choice == 3:
                result = math.tan(num_rad)
                operation = f"tan({num}°) = {result}"
            elif choice == 4:
                if math.cos(num_rad) == 0:
                    print("Hata: Tanımlı değildir (90° ve katları)")
                    return
                result = 1 / math.tan(num_rad)
                operation = f"cot({num}°) = {result}"
            elif choice == 5:
                if math.cos(num_rad) == 0:
                    print("Hata: Tanımlı değildir (90° ve katları)")
                    return
                result = 1 / math.cos(num_rad)
                operation = f"sec({num}°) = {result}"
            elif choice == 6:
                if math.sin(num_rad) == 0:
                    print("Hata: Tanımlı değildir (180° ve katları)")
                    return
                result = 1 / math.sin(num_rad)
                operation = f"csc({num}°) = {result}"
            elif choice == 7:
                sub_choice = int(input("1. arcsin  2. arccos  3. arctan: "))
                if sub_choice == 1:
                    if num < -1 or num > 1:
                        print("Hata: arcsin sadece -1 ile 1 arasında tanımlıdır!")
                        return
                    result = math.degrees(math.asin(num))
                    operation = f"arcsin({num}) = {result}°"
                elif sub_choice == 2:
                    if num < -1 or num > 1:
                        print("Hata: arccos sadece -1 ile 1 arasında tanımlıdır!")
                        return
                    result = math.degrees(math.acos(num))
                    operation = f"arccos({num}) = {result}°"
                elif sub_choice == 3:
                    result = math.degrees(math.atan(num))
                    operation = f"arctan({num}) = {result}°"

            print(f"\nSonuç: {operation}")
            self.history.append(operation)
        except ValueError:
            print("Hata: Geçersiz giriş! Lütfen sayı giriniz.")
        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu: {e}")

    def matrix_operations(self):
        print("\n" + "-"*50)
        print("  MATRİS İŞLEMLERİ".center(50))
        print("-"*50)
        print("1. Matris Toplama")
        print("2. Matris Çıkarma")
        print("3. Matris Çarpma")
        print("4. Determinant Hesaplama")
        print("5. Ters Matris")
        print("6. Matrisin Transpozesi")
        print("0. Geri Dön")
        print("-"*50)

        try:
            choice = int(input("İşlem seçiniz (0-6): "))
            if choice == 0:
                return

            if choice in [1, 2, 3]:
                rows1 = int(input("1. Matrisin satır sayısı: "))
                cols1 = int(input("1. Matrisin sütun sayısı: "))
                rows2 = int(input("2. Matrisin satır sayısı: "))
                cols2 = int(input("2. Matrisin sütun sayısı: "))

                if choice in [1, 2] and (rows1 != rows2 or cols1 != cols2):
                    print("Hata: Matrisler aynı boyutta olmalıdır!")
                    return
                if choice == 3 and cols1 != rows2:
                    print("Hata: 1. matrisin sütun sayısı 2. matrisin satır sayısına eşit olmalıdır!")
                    return

                print("\n1. Matrisi girin:")
                matrix1 = self.get_matrix_input(rows1, cols1)
                print("\n2. Matrisi girin:")
                matrix2 = self.get_matrix_input(rows2, cols2)

                if choice == 1:
                    result = [[matrix1[i][j] + matrix2[i][j] for j in range(cols1)] for i in range(rows1)]
                    operation = f"Matris Toplama\n{self.format_matrix(matrix1)} + \n{self.format_matrix(matrix2)} = \n{self.format_matrix(result)}"
                elif choice == 2:
                    result = [[matrix1[i][j] - matrix2[i][j] for j in range(cols1)] for i in range(rows1)]
                    operation = f"Matris Çıkarma\n{self.format_matrix(matrix1)} - \n{self.format_matrix(matrix2)} = \n{self.format_matrix(result)}"
                elif choice == 3:
                    result = [[sum(matrix1[i][k] * matrix2[k][j] for k in range(cols1)) for j in range(cols2)] for i in range(rows1)]
                    operation = f"Matris Çarpma\n{self.format_matrix(matrix1)} × \n{self.format_matrix(matrix2)} = \n{self.format_matrix(result)}"

            elif choice == 4:
                size = int(input("Kare matrisin boyutu (n x n): "))
                matrix = self.get_matrix_input(size, size)
                det = self.calculate_determinant(matrix)
                operation = f"Determinant\n{self.format_matrix(matrix)} = {det}"

            elif choice == 5:
                size = int(input("Kare matrisin boyutu (n x n): "))
                matrix = self.get_matrix_input(size, size)
                det = self.calculate_determinant(matrix)
                if det == 0:
                    print("Hata: Determinant sıfır olduğu için ters matris yoktur!")
                    return
                inverse = self.calculate_inverse(matrix)
                operation = f"Ters Matris\n{self.format_matrix(matrix)}⁻¹ = \n{self.format_matrix(inverse)}"

            elif choice == 6:
                rows = int(input("Matrisin satır sayısı: "))
                cols = int(input("Matrisin sütun sayısı: "))
                matrix = self.get_matrix_input(rows, cols)
                transpose = [[matrix[j][i] for j in range(rows)] for i in range(cols)]
                operation = f"Transpoz\n{self.format_matrix(matrix)}ᵀ = \n{self.format_matrix(transpose)}"

            print(f"\nSonuç: {operation}")
            self.history.append(operation)
        except ValueError:
            print("Hata: Geçersiz giriş! Lütfen sayı giriniz.")
        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu: {e}")

    def get_matrix_input(self, rows, cols):
        matrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                while True:
                    try:
                        val = float(input(f"Eleman [{i+1}][{j+1}]: "))
                        row.append(val)
                        break
                    except ValueError:
                        print("Hata: Lütfen sayı giriniz!")
            matrix.append(row)
        return matrix

    def format_matrix(self, matrix):
        max_len = max(len(str(matrix[i][j])) for i in range(len(matrix)) for