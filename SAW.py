import numpy as np

def tampilkan_judul():
    print("=" * 60)
    print("   SISTEM PENDUKUNG KEPUTUSAN - METODE SAW")
    print("   (Simple Additive Weighting)")
    print("=" * 60)

def input_kriteria():
    """Input jumlah kriteria dan detail tiap kriteria"""
    while True:
        try:
            n_kriteria = int(input("\nMasukkan jumlah kriteria: "))
            if n_kriteria <= 0:
                print("  Jumlah kriteria harus lebih dari 0!")
                continue
            break
        except ValueError:
            print("  Input tidak valid! Masukkan angka bulat.")

    kriteria = []
    bobot = []
    atribut = []

    print(f"\n--- Input Detail {n_kriteria} Kriteria ---")
    for i in range(n_kriteria):
        print(f"\nKriteria {i+1}:")
        nama = input(f"  Nama/Deskripsi kriteria {i+1}: ").strip()
        if not nama:
            nama = f"Kriteria {i+1}"

        while True:
            jenis = input(f"  Atribut (benefit/cost): ").strip().lower()
            if jenis in ["benefit", "cost", "b", "c"]:
                jenis = "benefit" if jenis in ["benefit", "b"] else "cost"
                break
            print("  Masukkan 'benefit' atau 'cost'!")

        while True:
            try:
                w = float(input(f"  Bobot kriteria (0-1 atau angka): "))
                if w < 0:
                    print("  Bobot tidak boleh negatif!")
                    continue
                break
            except ValueError:
                print("  Input tidak valid! Masukkan angka.")

        kriteria.append(nama)
        atribut.append(jenis)
        bobot.append(w)

    return n_kriteria, kriteria, atribut, bobot


def input_alternatif(n_kriteria, kriteria):
    """Input jumlah alternatif dan nilai tiap alternatif"""
    while True:
        try:
            n_alt = int(input("\nMasukkan jumlah alternatif: "))
            if n_alt <= 0:
                print("  Jumlah alternatif harus lebih dari 0!")
                continue
            break
        except ValueError:
            print("Input tidak valid! Masukkan angka bulat.")

    nama_alt = []
    matriks = []

    print(f"\n--- Input Nilai untuk {n_alt} Alternatif ---")
    for i in range(n_alt):
        print(f"\nAlternatif {i+1}:")
        nama = input(f"  Nama alternatif {i+1}: ").strip()
        if not nama:
            nama = f"Alternatif {i+1}"
        nama_alt.append(nama)

        nilai_alt = []
        for j in range(n_kriteria):
            while True:
                try:
                    v = float(input(f"  Nilai untuk '{kriteria[j]}': "))
                    if v < 0:
                        print("  Nilai tidak boleh negatif!")
                        continue
                    break
                except ValueError:
                    print("  Input tidak valid! Masukkan angka.")
            nilai_alt.append(v)
        matriks.append(nilai_alt)

    return n_alt, nama_alt, np.array(matriks, dtype=float)


def normalisasi_matriks(matriks, atribut):
    """Normalisasi matriks keputusan sesuai atribut benefit/cost"""
    n_alt, n_kriteria = matriks.shape
    matriks_normal = np.zeros_like(matriks)

    for j in range(n_kriteria):
        kolom = matriks[:, j]
        if atribut[j] == "benefit":
            max_val = np.max(kolom)
            if max_val == 0:
                matriks_normal[:, j] = 0
            else:
                matriks_normal[:, j] = kolom / max_val
        else:  # cost
            min_val = np.min(kolom)
            if min_val == 0:
                matriks_normal[:, j] = 0
            else:
                matriks_normal[:, j] = min_val / kolom

    return matriks_normal


def hitung_saw(matriks_normal, bobot):
    """Hitung nilai preferensi SAW (V = R * W)"""
    bobot_array = np.array(bobot)
    total_bobot = np.sum(bobot_array)
    if total_bobot != 1.0:
        bobot_normal = bobot_array / total_bobot
    else:
        bobot_normal = bobot_array

    nilai_v = np.dot(matriks_normal, bobot_normal)
    return nilai_v, bobot_normal


def tampilkan_hasil(nama_alt, kriteria, atribut, bobot, bobot_normal,
                    matriks, matriks_normal, nilai_v):
    """Tampilkan seluruh hasil perhitungan SAW"""
    print("\n" + "=" * 60)
    print("   HASIL PERHITUNGAN SAW")
    print("=" * 60)

    # Informasi Kriteria
    print("\n[1] KRITERIA & BOBOT")
    print("-" * 50)
    header = f"{'No':<4} {'Kriteria':<20} {'Atribut':<10} {'Bobot Asli':<12} {'Bobot Normal'}"
    print(header)
    print("-" * 50)
    for i, (k, a, b, bn) in enumerate(zip(kriteria, atribut, bobot, bobot_normal)):
        print(f"{i+1:<4} {k:<20} {a:<10} {b:<12.4f} {bn:.4f}")

    # Matriks Keputusan Awal
    print("\n[2] MATRIKS KEPUTUSAN AWAL")
    print("-" * (20 + 12 * len(kriteria)))
    header = f"{'Alternatif':<20}" + "".join(f"{k[:10]:<12}" for k in kriteria)
    print(header)
    print("-" * (20 + 12 * len(kriteria)))
    for i, nama in enumerate(nama_alt):
        baris = f"{nama:<20}" + "".join(f"{matriks[i][j]:<12.4f}" for j in range(len(kriteria)))
        print(baris)

    # Matriks Normalisasi
    print("\n[3] MATRIKS NORMALISASI (R)")
    print("-" * (20 + 12 * len(kriteria)))
    print(header)
    print("-" * (20 + 12 * len(kriteria)))
    for i, nama in enumerate(nama_alt):
        baris = f"{nama:<20}" + "".join(f"{matriks_normal[i][j]:<12.4f}" for j in range(len(kriteria)))
        print(baris)

    # Nilai Preferensi
    print("\n[4] NILAI PREFERENSI (V) & PERINGKAT")
    print("-" * 40)
    print(f"{'No':<4} {'Alternatif':<20} {'Nilai V':<12} {'Peringkat'}")
    print("-" * 40)

    ranking = np.argsort(nilai_v)[::-1]  # Descending
    peringkat = np.empty_like(ranking)
    peringkat[ranking] = np.arange(1, len(ranking) + 1)

    for i, nama in enumerate(nama_alt):
        print(f"{i+1:<4} {nama:<20} {nilai_v[i]:<12.4f} {peringkat[i]}")

    # Rekomendasi
    terbaik_idx = np.argmax(nilai_v)
    print("\n" + "=" * 60)
    print(f"  REKOMENDASI TERBAIK: {nama_alt[terbaik_idx]}")
    print(f"  Nilai Preferensi   : {nilai_v[terbaik_idx]:.4f}")
    print("=" * 60)


def main():
    tampilkan_judul()

    # Input kriteria
    n_kriteria, kriteria, atribut, bobot = input_kriteria()

    # Input alternatif
    nama_alt, matriks = input_alternatif(n_kriteria, kriteria)

    # Proses SAW
    matriks_normal = normalisasi_matriks(matriks, atribut)
    nilai_v, bobot_normal = hitung_saw(matriks_normal, bobot)

    # Tampilkan hasil
    tampilkan_hasil(nama_alt, kriteria, atribut, bobot, bobot_normal, matriks, matriks_normal, nilai_v)