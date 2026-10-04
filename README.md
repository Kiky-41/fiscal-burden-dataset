# Dataset G — Beban fiskal transisi energi: subsidi, kompensasi, dan PLN

Sumber: **Nota Keuangan APBN TA 2025** (Lampiran Tabel 1, 2, 5; Bab 1 sensitivitas; Bab 3 subsidi; Bab 6 risiko fiskal), **LK PLN 2015–2024** (lewat `../PLN-Health-Dataset/pln_financial_panel.csv`), **Statistik PLN 2023** (Grafik 11 BPP vs tarif). Jalankan `python3 build_fiscal.py`; 9 cek validasi, semua lulus.

| File | Isi |
|---|---|
| `news_updates_2024_2026.csv` | Pembaruan dari internet (21 Sep 2026): subsidi listrik 2024 Rp75,8 T (prelim), subsidi+kompensasi listrik 2025 Rp210 T, subsidi+kompensasi seluruh energi Jan–Agu 2025 Rp218 T dan Jan–Agu 2026 Rp331,4 T, harga jual rata-rata PLN 2024 Rp1.153,38/kWh. Berasal dari berita/pernyataan pejabat, bukan audit; rincian listrik 2025 dan 2026 tidak tersedia |
| `apbn_energy_subsidy_2020_2025.csv` | Asumsi makro (kurs, ICP, dll.), postur APBN, subsidi energi/non-energi; subsidi listrik & BBM/LPG (2020, 2023, 2024 outlook, 2025); rasio terhadap belanja pusat dan PDB. Satuan miliar Rp |
| `pln_gov_support_2015_2024.csv` | Subsidi dan kompensasi dalam LK PLN (triliun Rp), penerimaan kas, piutang pemerintah, dibanding APBN |
| `bpp_tariff_gap_2019_2023.csv` | BPP audit vs harga jual rata-rata (Rp/kWh) 2019–2023, volume implisit, biaya selisih vs subsidi+kompensasi tercatat |
| `apbn_sensitivity_2025.csv` | Sensitivitas APBN 2025 (triliun Rp) untuk kurs, ICP, pertumbuhan, inflasi, SBN, lifting |
| `scenario_icp_fx_apbn2025.csv` | Grid ICP (60–120) × kurs (15.500–17.500), linier dari sensitivitas Nota |
| `scenario_bpp_shock.csv` | Kenaikan BPP 0–20% dengan tarif tetap, pemerintah menanggung 100% atau 50% |
| `pln_gov_receivables_bridge_2024_2025.csv` | Bridge rekonsiliasi kenaikan piutang 2025 (juta Rp + triliun): kompensasi, subsidi, diskon Jan-Feb 2025. Kenaikan 67,45 = akrual-kas 53,84 + diskon 13,61; tiap baris ada sumber (LK PLN 2025 Note 16/37, LKPP 2025, BPK/BPKP) |
| `pln_fiscal_exposure_facts.csv` | Jaminan pemerintah, PMN, jumlah penerima subsidi (dikutip dari Bab 6 dan 3) |

## Temuan yang bisa langsung dipakai
- Dukungan pemerintah ke PLN (subsidi + kompensasi) naik dari Rp56,6 T (2015) ke Rp177,2 T (2024), atau 32% pendapatan PLN; tanpa dukungan itu laba usaha 2024 negatif Rp116,6 T.
- Subsidi listrik di LK PLN 2023 (Rp68,64 T) sangat dekat dengan APBN (Rp68,70 T); selisih 2020 dan 2024 mencerminkan diskon pandemi dan outlook.
- Kompensasi (bukan subsidi) adalah komponen yang membesar: Rp17,9 T (2020) → Rp100,2 T (2024); Nota tidak memuat tabel kompensasi terpisah, sehingga angkanya hanya dari LK PLN.

## Keterbatasan
1. Nota 2025 hanya memberi subsidi listrik untuk 2020, 2023, 2024 (outlook), 2025. Untuk 2022 dipakai sumber sekunder (BPK/LKPP 2022 via Databoks, Rp56,1 T, naik 17% dari 2021), sehingga 2021 (≈Rp47,9 T) adalah turunan perkiraan; keduanya ada di kolom `subsidy_electricity_secondary_bn` dan `subsidy_electricity_best_bn`, bukan di kolom utama. Subsidi 2015–2019 tidak ada di dokumen ini (gunakan kolom LK PLN).
2. Angka 2024 di Nota adalah **outlook**, 2025 adalah **APBN** (bukan realisasi).
3. Sensitivitas Nota linier dan ceteris paribus, sudah memasukkan kompensasi energi, tetapi belum diskresi kebijakan. Grid jauh dari basis (ICP 60 atau 120) hanya indikatif.
4. Skenario BPP memakai BPP 2023 (Rp1.599/kWh) dan volume 2024 yang diturunkan dari pendapatan listrik ÷ tarif 2023 (perkiraan, bukan data). Kompensasi PLN mencakup lebih dari selisih BPP–tarif (rasio implisit 0,75–1,08 terhadap yang tercatat), sehingga skenario adalah orde besaran.
5. Pendapatan PLN pada Tabel 6.4 Nota untuk 2023 (333,2 T) adalah pendapatan penjualan listrik saja; 2019–2022 setara pendapatan total LK.
6. Angka 2025–2026 di `news_updates_2024_2026.csv` berasal dari berita dan pernyataan pejabat; BPP 2024 satu tahun tetap tidak ditemukan (hanya rata-rata 2021–2024 Rp1.445/kWh dari Databoks). Statistik PLN 2024 tidak dapat diunduh dari lingkungan ini (akses ke web.pln.co.id diblokir proxy), sehingga versi 2024 dataset F/E belum dibuat.

## Pembaruan 2025-2026 (`news_updates_2024_2026.csv`, kini 15 uji)
Ditambahkan angka LK PLN 2025 dari media (pendapatan Rp582,68 T; subsidi 87,46; kompensasi 112,73; piutang pemerintah 110,73; laba 7,26; rugi kurs 12,46), anggaran subsidi listrik APBN 2026 Rp104,6 T (outlook 2025 Rp89 T), serta dua penanda BPP (proyeksi RUPTL PSO7 Rp1.829/kWh untuk 2025; pernyataan Dirut PLN Rp1.600-1.700/kWh). **Peringatan**: PDF LK 2025 di IDX tidak dapat diakses (403), sehingga semua angka 2025 bersumber berita. Pembanding laba 2024 di media (Rp21,2 T) tidak sama dengan LK Audited 2024 di panel E (Rp17,76 T); selisih belum terjelaskan.
Tambahan dari pencarian kedua: pelanggan PLN 2025 96,2 juta, penjualan 317,69 TWh, subsidi+kompensasi listrik Jan-Agu 2025 (48,1 + 37,5 + 2,0 kurang bayar = 87,6; pagu 127,2), proyeksi subsidi energi 2026 Rp227,26 T. Selisih laba 2024 (17,76 vs 21,23 di berita) hanya terjadi di bawah biaya operasi (komponen biaya pembanding sama dengan panel E), jadi kemungkinan penyajian kembali pajak/lain-lain, bukan revisi biaya. Realisasi BPP 2024/2025 dan subsidi listrik setahun penuh 2025 tetap tidak ditemukan dari sumber yang bisa dibuka.

Penemuan ketiga (via ekstensi Chrome, Kemenkeu): slide "Subsidi dan Kompensasi APBN 2025" (Konpers 13 Mar 2025) memuat **harga seharusnya listrik RT 900VA bersubsidi Rp1.800/kWh vs harga masyarakat Rp600** (ditanggung APBN Rp1.200, 67%), serta subsidi listrik 2024 Rp75,8 T dan alokasi 2025 Rp89,7 T; Konpers 8 Jan 2026 memuat realisasi sementara 2025 (subsidi semua jenis Rp281,6 T; subsidi+kompensasi Rp401,6 T; pelanggan listrik bersubsidi 42,8 juta). Ini proksi biaya penyediaan resmi untuk 900VA, **bukan BPP rata-rata nasional realisasi**, yang tetap belum ditemukan. Subsidi listrik 2025 realisasi setahun penuh (terpisah dari BBM/LPG) juga belum ada di dokumen tersebut.

**LK PLN 2025 audited (ditambahkan).** Laba bersih 2025 = 7.260.708 juta; laba 2024 disajikan kembali dari 17.763.024 menjadi 21.231.284 (Catatan 58, koreksi pajak tangguhan 7.905.235 juta). `news_updates_2024_2026.csv` memuat baris `pln_lk_net_profit_restated` dan `pln_lk_deferred_tax_overstatement_dec2024`; angka 2025 diuji terhadap panel E dan Statistik PLN 2025 Tabel 62-63 (piutang pemerintah 110.738, subsidi 87.461, kompensasi 112.735 miliar Rp).

**Subsidi listrik 2025 penuh (LKPP 2025 audited, dicari lewat Chrome 21 Sep 2026).** Belanja Subsidi Listrik (kas) 2025 = Rp81,036 T (pagu 89,747 T; 2024: 75,817 T); Kompensasi Tarif Listrik kas 2025 = Rp65,321 T (pagu 92,411 T). Beban akrual subsidi listrik 2025 = Rp87,461 T, sama dengan pendapatan subsidi di LK PLN dan Statistik PLN 2025 (selisih akrual-kas 6,42 T = subsidi yang belum dibayar). Baris ada di `news_updates_2024_2026.csv` (item `apbn_electricity_*`, `subsidized_electricity_gwh_realized` 2020-2024 dari Laporan Kinerja Ditjen Gatrik 2025).
**BPP realisasi nasional 2025: tidak ditemukan sebagai angka resmi.** Yang ada: proyeksi RUPTL 2025 Rp1.829/kWh (sumber sekunder). Kolom `derived_bpp_proxy_*` adalah proksi turunan (beban usaha [+ beban keuangan] / kWh terjual, Statistik PLN 2025 T63/T46): 2025 = 1.679 (1.757 dengan beban keuangan); jangan diperlakukan sebagai BPP resmi.

## ML (`ml_fiscal.py`, sampai 2025)

Numpy+pandas. Keluaran: `ml_fiscal_backtest.csv`, `ml_fiscal_2025_forecast.csv`, `ml_fiscal_gap_model.csv`, `ml_fiscal_mc_2026.csv`.

- **Backtest 2025 (latih 2015-2024)**: dukungan pemerintah aktual 200,2 T; tren 5 tahun 203,8 (galat 3,6), naif 177,2, rata-rata 3 tahun 147,4. **Piutang pemerintah 110,7 T** tidak terprakirakan (galat 67-95 T; rata-rata 3 tahun ditandai kejutan), demikian pula selisih akrual-kas 53,8 T.
- **Model celah biaya** (dukungan ~ opex − pendapatan ex-dukungan; identitas laba usaha diuji): LOYO R² 0,955; prediksi 2025 = 214,4 vs aktual 200,2 (residu −14 T).
- **Monte Carlo 2026 (bootstrap pertumbuhan tahunan 2016-2025, kondisional, bukan prakiraan)**: dukungan yang dibutuhkan agar margin laba usaha tetap seperti 2025: p05 182, median 233, p95 282 T; peluang melebihi 2025 sekitar 70%. Rumus diuji: pertumbuhan nol mereproduksi 200,2 T.

## Realisasi makro 2025 (LKPP 2025 via BPK, ditambahkan ke `news_updates_2024_2026.csv`)

Pertumbuhan 5,11% (asumsi 5,2), inflasi 2,92% y/y (asumsi 2,5), kurs rata-rata Rp16.475 (asumsi 16.000; cocok dengan panel kurs D 16.474), SBN 10 tahun 6,71% (asumsi 7,0), **ICP 67,38 USD/barel (asumsi 82; 2024: 78,14)**, lifting minyak 605,86 ribu bph. Baris `apbn_energy_subsidy_2020_2025.csv` untuk 2025 tetap **asumsi APBN**, bukan realisasi; pakai baris `macro_realized_*` untuk realisasi. Tambahan dari Ditjen Gatrik: konsumsi listrik per kapita 2025 1.584 kWh (2024: 1.411), kapasitas terpasang nasional 107,51 GW.

## BPP realisasi: pencarian lanjutan (21 Sep 2026)

Dicari lagi lewat Chrome: Kepmen/Permen ESDM tentang BPP, bahan rapat DPR Komisi XII, LK PLN 2025, laporan tahunan PLN, laporan kinerja, Nota Keuangan RAPBN 2026, serta pencarian bahasa Inggris (IEEFA/IESR). Hasil: **tidak ada angka BPP nasional realisasi 2024 atau 2025**. Yang ditemukan hanya BPP 2019-2023 (Statistik PLN 2023), formula subsidi (PMK 20/2025: subsidi = BPP x (1+margin) - harga jual, dikali volume; dikutip dari cuplikan artikel MDPI 2026) dan mekanisme penetapan BPP (Kepmen 169.K/2021). Halaman berita esdm.go.id tidak bisa dibaca ekstensi (izin domain ditolak) dan tidak dicari lewat jalan lain. Angka 2024-2025 di dataset tetap proksi turunan.

- **Makro realisasi vs biaya energi PLN** (`ml_fiscal_macro_realized_link.csv`): ICP realisasi 2025 turun 13,8% (67,4 dari 78,1) tetapi biaya bahan bakar + pembelian listrik PLN naik 10,0% (393,8 T dari 357,9 T) dan dukungan pemerintah naik 13,0%. Korelasi Spearman perubahan ICP vs biaya energi 2021-2025 = -0,30 (n=5, hanya deskriptif). Penyebab tidak diuji.

## ML modern: state-space local trend (`ml_modern_fiscal_bsts.py`, ML bukan Bayesian)

Unobserved Components local linear trend, maximum likelihood via Kalman filter (bukan Bayesian: tanpa prior/posterior). Uji 2025 dukungan pemerintah: prakiraan 205,0 T (selang 90%: 170,5-239,4) vs aktual 200,2 T; MAE 2021-2024 19,7 vs naif 27,8 (2021-2025: 16,7 vs 26,0 bila 2025 dimasukkan). Piutang pemerintah 2025 (110,7 T) **tidak terdeteksi sebagai kejutan** karena deretnya baru 6 tahun sehingga selangnya sangat lebar (prakiraan 86,6 ± 29). Prakiraan kondisional 2026: dukungan 226,5 T (194-259), 2027: 252,5 T (198-307); piutang 2026: 178 T (132-224) dari ekstrapolasi univariat. Bukan prakiraan resmi. Butuh statsmodels.

## Model utama yang dipilih: prakiraan probabilistik koheren per komponen (`ml_hier_fiscal_coherent.py`)

Dukungan pemerintah adalah identitas: opex/(1−margin) − pendapatan ex-dukungan (diuji, semua tahun). Empat komponen (bahan bakar, pembelian listrik, biaya lain, pendapatan) diprakirakan sebagai random walk dengan drift pada log (6 tahun terakhir), digabung dengan kopula Gaussian dari korelasi residual (menyusut 50%), lalu dijumlahkan menurut identitas dengan margin dari 5 tahun terakhir. Rolling origin stokastik (seed 0, 4000 path): MAE 2021-2025 19,7 vs naif 26,9; **2023-2025: 6,8 vs 25,9**. Varian deterministik di `ml_select_fiscal_scores.csv` (`koheren_komponen`): 20,2/7,4 — beda noise simulasi + agregasi median, bukan model berbeda. Tahun 2021-2022 sangat buruk (origin hanya 5 pertumbuhan yang bergejolak; selang > 900 T), jadi hanya 2023-2025 yang bisa dinilai. 2025: median 209,6 T (90%: 151,6-279,9) vs aktual 200,2 T. Ketajaman 2023-2025: lebar rata-rata koheren 119 T vs state-space 71 T (keduanya coverage 100% 3/3) — liputan penuh dibayar dengan interval lebih lebar. Prakiraan kondisional: 2026 256,6 T (195,5-330,2), 2027 301,6 T (212,9-419,5), memakai pertumbuhan rata-rata ~15%/tahun; hasil ini lebih agresif daripada state-space (226,5) dan Monte Carlo (233) di atas. Model memproyeksikan kebutuhan $G_t$, bukan timing kas/piutang.
