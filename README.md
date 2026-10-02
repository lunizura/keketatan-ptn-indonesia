# Indeks &amp; Kalkulator Keketatan PTN Top Indonesia
### Indonesian Top Universities Selectivity &amp; Choice Portfolio Simulator

Repositori ini menyajikan basis data analitis dan platform visualisasi tingkat persaingan (keketatan), daya tampung, serta riwayat peminat program studi pada 15 Perguruan Tinggi Negeri (PTN) klaster utama di Indonesia untuk jalur Seleksi Nasional Berdasarkan Prestasi (SNBP) dan Seleksi Nasional Berdasarkan Tes (SNBT / UTBK).

---

## Bahasa Indonesia

### 1. Latar Belakang &amp; Tujuan
Setiap tahun, ratusan ribu calon mahasiswa baru menghadapi dilema dalam menentukan pilihan program studi pada seleksi nasional penerimaan mahasiswa baru. Ketimpangan informasi mengenai rasio persaingan nyata (*selectivity ratio*) kerap mengakibatkan pemilihan kombinasi jurusan yang terlalu berisiko (*high-risk portfolio*).

Platform ini hadir untuk menyediakan transparansi berbasis data resmi (*open educational data*) agar calon mahasiswa dapat:
- Mengetahui perbandingan riil antara kuota kursi yang tersedia dengan jumlah peminat tahun-tahun sebelumnya.
- Mengidentifikasi jurusan-jurusan dengan tingkat persaingan paling ketat secara nasional.
- Membandingkan program studi sejenis lintas kampus (misal: Teknik Informatika di ITB vs UI vs UGM vs ITS vs UNS).
- Mensimulasikan dan menguji kelayakan kombinasi Pilihan 1 dan Pilihan 2 secara objektif.

---

### 2. Metodologi &amp; Formula Perhitungan

Data diolah menggunakan dua metrik kuantitatif baku:

#### A. Persentase Keketatan (Selectivity Rate)
$$\text{Keketatan} = \left( \frac{\text{Daya Tampung}}{\text{Jumlah Peminat Terakhir}} \right) \times 100\%$$
*Semakin rendah persentasenya, semakin ketat persaingan dan semakin kecil probabilitas lolos.*

Klasifikasi Tingkat Keketatan:
- **Sangat Ketat:** $< 2.50\%$ (Persaingan puncak nasional, rasio di atas $1 : 40$).
- **Ketat:** $2.50\% - 5.00\%$ (Persaingan tinggi, rasio sekitar $1 : 20$ hingga $1 : 40$).
- **Sedang:** $5.01\% - 10.00\%$ (Persaingan moderat, rasio sekitar $1 : 10$ hingga $1 : 20$).
- **Terbuka:** $> 10.00\%$ (Peluang relatif lebih terbuka, rasio di bawah $1 : 10$).

#### B. Rasio Persaingan (Competition Ratio)
$$\text{Rasio} = 1 : \left\lceil \frac{\text{Jumlah Peminat}}{\text{Daya Tampung}} \right\rceil$$
*Contoh:* Rasio $1 : 55$ menandakan bahwa setiap 1 kursi daya tampung diperebutkan oleh 55 orang pendaftar.

---

### 3. Cakupan 15 PTN Klaster Utama

| No | PTN | Nama Lengkap Perguruan Tinggi | Kota | Klaster |
| :---: | :--- | :--- | :--- | :---: |
| 1 | UI | Universitas Indonesia | Depok | PTN-BH |
| 2 | ITB | Institut Teknologi Bandung | Bandung | PTN-BH |
| 3 | UGM | Universitas Gadjah Mada | Sleman / Yogyakarta | PTN-BH |
| 4 | IPB | IPB University | Bogor | PTN-BH |
| 5 | UNAIR | Universitas Airlangga | Surabaya | PTN-BH |
| 6 | ITS | Institut Teknologi Sepuluh Nopember | Surabaya | PTN-BH |
| 7 | UNDIP | Universitas Diponegoro | Semarang | PTN-BH |
| 8 | UB | Universitas Brawijaya | Malang | PTN-BH |
| 9 | UNPAD | Universitas Padjadjaran | Sumedang / Bandung | PTN-BH |
| 10 | UNS | Universitas Sebelas Maret | Surakarta | PTN-BH |
| 11 | UPI | Universitas Pendidikan Indonesia | Bandung | PTN-BH |
| 12 | USU | Universitas Sumatera Utara | Medan | PTN-BH |
| 13 | UNHAS | Universitas Hasanuddin | Makassar | PTN-BH |
| 14 | UNAND | Universitas Andalas | Padang | PTN-BH |
| 15 | UNUD | Universitas Udayana | Badung / Denpasar | PTN-BLU |

---

### 4. Fitur Utama Platform

1. **Peringkat Terketat Nasional (National Leaderboard):**
   - Menampilkan Top 50 jurusan dengan tingkat keketatan paling ekstrem di Indonesia.
   - Filter dinamis berdasarkan jalur seleksi (SNBT vs SNBP) dan rumpun keilmuan (Saintek vs Soshum).
2. **Komparasi Antar-Kampus (Head-to-Head Comparison):**
   - Membandingkan kuota, peminat, dan rasio persaingan program studi sejenis di berbagai universitas.
   - Dilengkapi visualisasi grafik batang komparasi untuk melihat kampus mana yang persaingannya paling tinggi vs paling terbuka.
3. **Kalkulator &amp; Simulator Strategi Pilihan (Choice Portfolio Simulator):**
   - Menguji kombinasi Pilihan 1 dan Pilihan 2 calon mahasiswa.
   - Mendeteksi risiko:
     - *Risiko Ekstrem:* Kedua pilihan berkeketatan $< 2.5\%$.
     - *Urutan Terbalik:* Pilihan 2 justru memiliki persaingan lebih ketat daripada Pilihan 1.
     - *Strategi Seimbang:* Pilihan 1 ambisius dengan Pilihan 2 sebagai jaring pengaman realistis.
4. **Direktori Jelajah &amp; Modal Detail:**
   - Pencarian instan berdasarkan nama prodi, kampus, akreditasi, dan rentang keketatan.
   - Modal detail dilengkapi grafik tren riwayat peminat 3 tahun terakhir (2022, 2023, 2024), kurikulum inti, dan prospek karir lulusan.
5. **Dukungan Dwibahasa Penuh:**
   - Beralih antara Bahasa Indonesia dan English secara instan dengan sinkronisasi URL parameter (`?lang=en`).

---

### 5. Struktur Berkas &amp; Data Terbuka (Open Data)

Dataset disediakan secara terbuka dalam beberapa format:
- `data/ptn_keketatan.json`: Dataset format JSON lengkap dengan struktur bersarang.
- `data/ptn_keketatan.js`: Format JavaScript runtime siap pakai untuk antarmuka web statis.
- `data/ptn_keketatan.csv`: Format tabular CSV untuk analisis data dan spreadsheet.
- `data/metadata.json`: Metadata pembaruan, total entri, dan lisensi.
- `scripts/build_ptn_dataset.py`: Skrip otomasi penghimpunan dan pemrosesan data.

---

## English

### 1. Overview &amp; Educational Context
Every academic cycle, hundreds of thousands of prospective university applicants navigate Indonesia's competitive public university entrance pathways: SNBP (achievement-based portfolio) and SNBT (computer-based national entrance exam / UTBK).

Information asymmetry often leads students to select poorly calibrated choice pairs (e.g., placing two hyper-competitive programs in both slots), resulting in unnecessary rejection across both options. This platform bridges that gap by providing transparent, structured analytics on university selectivity ratios, historical applicant trajectories, and portfolio risk calibration.

---

### 2. Mathematical Methodology

Selectivity is modeled using two standard quantitative metrics:

#### A. Selectivity Rate (Percentage)
$$\text{Selectivity Rate} = \left( \frac{\text{Quota (Daya Tampung)}}{\text{Applicants (Peminat)}} \right) \times 100\%$$
*A lower percentage indicates a more selective and fiercely contested major.*

Classification Thresholds:
- **Very Competitive:** $< 2.50\%$ (National peak competition, applicant-to-quota ratio $> 1 : 40$).
- **Competitive:** $2.50\% - 5.00\%$ (High competition, ratio between $1 : 20$ and $1 : 40$).
- **Moderate:** $5.01\% - 10.00\%$ (Balanced competition, ratio between $1 : 10$ and $1 : 20$).
- **Open / Accessible:** $> 10.00\%$ (More accessible, ratio $< 1 : 10$).

#### B. Competition Ratio
$$\text{Competition Ratio} = 1 : \left\lceil \frac{\text{Applicants}}{\text{Quota}} \right\rceil$$
*Example:* A $1 : 55$ ratio implies that 55 applicants compete for a single available seat.

---

### 3. Key Platform Capabilities

- **National Selectivity Leaderboard:** Top 50 most selective academic programs nationwide, filterable by admission track (SNBT vs SNBP) and scientific cluster (Science &amp; Technology vs Social Sciences &amp; Humanities).
- **Multi-Campus Head-to-Head Comparison:** Direct cross-university evaluation of equivalent majors (e.g., Computer Science across ITB, UI, UGM, ITS, and UNS).
- **Choice Portfolio Risk Simulator:** Algorithm that inspects two-choice applications to detect inverted selectivity orders or excessive risk concentrations.
- **Searchable Directory &amp; Historical Breakdown:** Interactive program lookup with 3-year applicant trend graphs (2022-2024), curriculum focuses, and career outlooks.
- **Bilingual Interface:** Real-time localization between Indonesian and English with URL state persistence.
- **Open Data Distribution:** Machine-readable datasets exported in JSON and CSV for researchers and prospective students.

---

### 4. Data Citation &amp; License

- **Data Attribution:** Compiled from official figures released by the National Selection Committee for Higher Education (Balai Pengelolaan Pengujian Pendidikan / BPPP SNPMB, Ministry of Education, Culture, Research, and Technology) and admission directories of the 15 host institutions.
- **License:** Open educational and research use. Free to share, analyze, and build upon.
