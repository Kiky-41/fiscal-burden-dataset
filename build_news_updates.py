#!/usr/bin/env python3
"""Pembaruan 2024-2026 dari sumber publik (berita/pernyataan resmi, dicari via internet 21 Sep 2026).
Bukan audit; setiap baris punya sumber dan status. Cek konsistensi terhadap data LK PLN di folder ini."""
import os, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
rows = [
 (2024,'apbn_electricity_subsidy_realized_prelim',75.8,'Rp triliun','realisasi per 24 Des 2024; 73,24 (tahun berjalan) + 2,58 (kurang bayar 2022)','Menkeu Sri Mulyani, 6 Jan 2025 (dikutip Warta Ekonomi)','https://wartaekonomi.co.id/read554249/realisasi-subsidi-listrik-2024-capai-rp758-triliun-ini-detailnya','preliminary'),
 (2024,'apbn_electricity_subsidy_arrears_2022_paid',2.58,'Rp triliun','pembayaran kurang bayar subsidi 2022','idem','idem','preliminary'),
 (2024,'pln_lk_subsidy_revenue',77.045334,'Rp triliun','Statistik PLN 2024, ikhtisar laba rugi (Rp77.045.334 juta)','PLN, Statistik 2024','https://web.pln.co.id/statics/uploads/2025/09/Statistik-PLN-2024-Ind-Eng.pdf','PDF tidak dapat diunduh dari sandbox; angka dari ringkasan halaman ikhtisar'),
 (2024,'pln_lk_compensation_revenue',100.184044,'Rp triliun','Statistik PLN 2024 (Rp100.184.044 juta)','PLN, Statistik 2024','idem','idem'),
 (2024,'pln_lk_electricity_sales_revenue',353.176019,'Rp triliun','Statistik PLN 2024 (Rp353.176.019 juta)','PLN, Statistik 2024','idem','idem'),
 (2024,'pln_avg_selling_price',1153.38,'Rp/kWh','harga jual rata-rata 2024 (2023: 1.155,47)','PLN, Statistik 2024','idem','idem'),
 (2023,'pln_avg_selling_price',1155.47,'Rp/kWh','dari Statistik PLN 2024','PLN, Statistik 2024','idem','idem'),
 (2025,'electricity_subsidy_and_compensation_total',210.0,'Rp triliun','termasuk Rp12 T diskon tarif Mar-Mei 2025; rincian subsidi vs kompensasi tidak dipublikasikan di sumber','Menteri ESDM Bahlil Lahadalia, 16 Des 2025','https://most1058fm.com/2025/12/realisasi-subsidi-dan-kompensasi-listrik-2025-capai-rp-210-triliun/','pernyataan resmi, belum audit'),
 (2025,'electricity_tariff_stimulus_discount',12.0,'Rp triliun','diskon tarif listrik Mar-Mei 2025','idem','idem','pernyataan resmi'),
 (2025,'energy_subsidy_compensation_jan_aug',218.0,'Rp triliun','seluruh energi (BBM, LPG, listrik) Jan-Agu 2025','Kemenkeu, dikutip Jawa Pos 18 Sep 2026','https://www.jawapos.com/ekonomi/2609180254/realisasi-subsidi-energi-tembus-rp-331-triliun-naik-rp-113-triliun-dari-2025','berita'),
 (2026,'energy_subsidy_compensation_jan_aug',331.4,'Rp triliun','seluruh energi Jan-Agu 2026; rincian listrik tidak tersedia','Kemenkeu, Jawa Pos 18 Sep 2026','idem','berita'),
 (2026,'energy_subsidy_compensation_jan_aug_yoy_increase',113.0,'Rp triliun','+51,8% terhadap Jan-Agu 2025','idem','idem','berita'),

 (2025,'pln_lk_operating_revenue_total',582.68,'Rp triliun','LK PLN 2025 (media); pembanding 2024 = 545,38','CNBC Indonesia 2 Jun 2026; Katadata','https://www.cnbcindonesia.com/news/20260602161044-4-739489/pln-cetak-laba-rp-726-triliun-di-2025','berita; PDF IDX 403'),
 (2025,'pln_lk_subsidy_revenue',87.46,'Rp triliun','+13,52% YoY','Katadata (LK PLN 2025)','https://katadata.co.id/amp/finansial/korporasi/6a39457acf3c0/utang-pemerintah-ke-pln-membengkak-ke-rp-110-triliun-laba-susut-67-di-2025','berita'),
 (2025,'pln_lk_compensation_revenue',112.73,'Rp triliun','+12,53% YoY; CNBC sama (112,73)','Katadata; CNBC','idem','berita'),
 (2025,'pln_lk_govt_receivable',110.73,'Rp triliun','piutang pemerintah, +155,8% dari 43,29 (2024) = sama dengan panel E','Katadata','idem','berita'),
 (2025,'pln_lk_net_profit',7.260708,'Rp triliun','LK Audited 2025 (Rp7.260.708 juta). Pembanding 2024 disajikan kembali dari 17,763 menjadi 21,231 T: koreksi lebih catat beban pajak tangguhan Rp3,468 T (pajak tangguhan atas biaya pemeliharaan yang dikapitalisasi secara fiskal sejak 2020; Catatan 58 LK 2025). Laba sebelum pajak 2024 tidak berubah (28,270 T)','PLN, LK Audited 2025 (disetujui 19 Mei 2026), Catatan 58','LK-PLN 2025 Audited.pdf (folder Data)','audited'),
 (2025,'pln_lk_fx_loss',12.46,'Rp triliun','rugi kurs 2025 (2024 pembanding 6,78 = panel E)','CNBC','https://www.cnbcindonesia.com/news/20260602161044-4-739489/pln-cetak-laba-rp-726-triliun-di-2025','berita'),
 (2025,'pln_lk_gov_support_total',200.19,'Rp triliun','subsidi 87,46 + kompensasi 112,73 (dihitung); 2024: 177,23','dihitung','idem','turunan'),
 (2026,'apbn_electricity_subsidy_budget',104.6,'Rp triliun','APBN 2026, +17,5% dari outlook 2025 Rp89 T; penyebab: kurs, biomass cofiring, bauran BBM 3T','Investortrust (dokumen anggaran)','https://investortrust.id/business/76355/subsidi-listrik-2026-naik-17-5-tembus-rp-104-6-triliun-ternyata-karena-faktor-ini','berita'),
 (2025,'apbn_electricity_subsidy_outlook',89.0,'Rp triliun','outlook 2025 (bukan realisasi audit)','idem','idem','berita'),
 (2025,'bpp_ruptl2025_pso7_scenario',1829.0,'Rp/kWh','BPP rata-rata 2025 skenario PSO7 RUPTL 2025-2034 (Plan-Financing-Gap-Dataset/ruptl2025_bpp_subsidy_scenarios.csv); proyeksi, bukan realisasi','RUPTL PLN 2025-2034','Plan-Financing-Gap-Dataset','proyeksi resmi'),
 (2025,'bpp_ceo_statement_approx',1650.0,'Rp/kWh','"BPP saat ini sekitar Rp1.600-1.700/kWh" (Dirut PLN, saat tarif tak naik akhir 2024); nilai tengah; tanggal pasti belum diverifikasi','Bloomberg Technoz','https://www.bloombergtechnoz.com/detail-news/57176/bos-pln-beber-nasib-tarif-listrik-2025-usai-tak-naik-akhir-2024/2','pernyataan lisan dari hasil pencarian'),
 (2025,'pln_customers',96.2,'juta pelanggan','LK/rilis PLN 2025 (2024: 92,88 juta dari Statistik 2024)','Infobanknews (rilis PLN)','https://infobanknews.com/pln-bukukan-laba-bersih-rp726-triliun-sepanjang-2025','berita'),
 (2025,'pln_electricity_sold',317.69,'TWh','+3,75% dari 306,21 TWh (2024; Statistik 2024: 306.219 GWh)','Infobanknews (rilis PLN)','idem','berita'),
 (2025,'pln_connected_capacity',192621,'MVA','+5,82% dari 182.026 MVA (2024)','Infobanknews (rilis PLN)','idem','berita'),
 (2025,'pln_lk_2024_net_profit_as_comparative_in_media',21.23,'Rp triliun','angka pembanding 2024 di berita LK 2025 (Bloomberg Technoz; -65,8% ke 7,26). Komponen biaya pembanding 2024 (BBM 179,29; IPP 178,63; pemeliharaan 31,55) SAMA dengan panel E, jadi selisih laba 17,76 vs 21,23 (= 3,47 T) terjadi di bawah biaya operasi; kemungkinan penyajian kembali, belum terkonfirmasi','Bloomberg Technoz','https://www.bloombergtechnoz.com/detail-news/110581/laba-bersih-anjlok-65-8-sepanjang-2025-pln-kantongi-rp7-26-t','berita; perlu LK 2025 asli'),
 (2025,'apbn_electricity_subsidy_realized_jan_aug',48.1,'Rp triliun','55,9% dari pagu subsidi; termasuk kurang bayar 2023','Menkeu Purbaya via Bloomberg Technoz','https://www.bloombergtechnoz.com/detail-news/85564/subsidi-kompensasi-listrik-tembus-rp87-triliun-per-agustus-2025','berita'),
 (2025,'apbn_electricity_compensation_realized_jan_aug',37.5,'Rp triliun','100% dari target kompensasi periode berjalan','idem','idem','berita'),
 (2025,'apbn_electricity_subsidy_compensation_budget',127.2,'Rp triliun','total pagu subsidi + kompensasi listrik 2025 (dasar penghitungan)','idem','idem','berita'),
 (2025,'apbn_electricity_arrears_component_jan_aug',2.0,'Rp triliun','kurang bayar tahun sebelumnya dalam total 87,6','idem','idem','berita'),
 (2025,'apbn_subsidy_total_all_types',281.6,'Rp triliun','realisasi subsidi pemerintah total 2025 (BBM, LPG, listrik, pupuk, dll.), tanpa kompensasi','Tempo/Kompas 8 Jan 2026 (judul)','https://www.tempo.co/ekonomi/realisasi-subsidi-pemerintah-pada-2025-naik-jadi-rp-281-6-t-2105784','berita; isi tidak dapat diambil (robots)'),
 (2026,'apbn_energy_subsidy_outlook_all',227.26,'Rp triliun','proyeksi subsidi energi (BBM, LPG, listrik) akhir 2026; rata-rata 2022-2025 Rp174,73 T','CNBC Indonesia 18 Agu 2026','https://www.cnbcindonesia.com/news/20260818142222-4-760308/subsidi-bbm-lpg-listrik-di-2026-diperkirakan-naik-jadi-rp-227-triliun/amp','berita (dokumen pemerintah)'),
 (2025,'bpp_proxy_900va_price_should_be',1800.0,'Rp/kWh','"harga seharusnya" listrik RT 900VA bersubsidi (proksi biaya penyediaan pemerintah): 1.800; harga masyarakat 600; ditanggung APBN 1.200 (67%); 41,5 juta pelanggan','Kemenkeu, Konferensi Pers APBN Kita 13 Mar 2025, hlm. 21','https://media.kemenkeu.go.id/getmedia/b6026682-cd60-48f9-9183-f03d51df9479/Publikasi-Web-Konpers-APBN-Kita-(Maret-2025).pdf','dokumen resmi (bukan BPP realisasi)'),
 (2025,'bpp_proxy_900va_price_paid_by_public',600.0,'Rp/kWh','harga jual ke masyarakat 900VA RT bersubsidi','idem','idem','dokumen resmi'),
 (2025,'bpp_proxy_900va_borne_by_apbn',1200.0,'Rp/kWh','selisih yang ditanggung APBN (67% dari 1.800)','idem','idem','dokumen resmi'),
 (2024,'apbn_electricity_subsidy_realized_kemenkeu',75.8,'Rp triliun','subsidi listrik realisasi 2024 (sama dengan Menkeu 6 Jan 2025)','Kemenkeu, Konpers 13 Mar 2025','idem','dokumen resmi'),
 (2025,'apbn_electricity_subsidy_apbn_allocation',89.7,'Rp triliun','subsidi listrik APBN 2025 (kolom 2025, bukan realisasi); outlook Investortrust 89,0','Kemenkeu, Konpers 13 Mar 2025','idem','dokumen resmi'),
 (2024,'apbn_energy_subsidy_total',177.6,'Rp triliun','BBM 21,6 + LPG 80,2 + listrik 75,8','idem','idem','dokumen resmi'),
 (2024,'apbn_energy_compensation_total',209.3,'Rp triliun','kompensasi energi (BBM+listrik) 2024','idem','idem','dokumen resmi'),
 (2025,'apbn_energy_subsidy_total_allocation',203.4,'Rp triliun','BBM 26,7 + LPG 87,0 + listrik 89,7 (alokasi APBN 2025)','idem','idem','dokumen resmi'),
 (2025,'apbn_energy_compensation_total_allocation',190.9,'Rp triliun','kompensasi energi 2025 (alokasi)','idem','idem','dokumen resmi'),
 (2025,'apbn_subsidy_all_types_realized',281.6,'Rp triliun','realisasi subsidi semua jenis s.d. 31 Des 2025 (BBM, LPG, listrik, pupuk, perumahan)','Kemenkeu, Konpers realisasi sementara APBN 2025, 8 Jan 2026, hlm. 28','https://media.kemenkeu.go.id/getmedia/b7f00cc5-15ad-4d8d-9bb5-42e18e8494a8/Publikasi-Web-Konpers-APBN-Kita-(Januari-2026).pdf','dokumen resmi (sementara)'),
 (2025,'apbn_subsidy_and_compensation_realized',401.6,'Rp triliun','subsidi + kompensasi semua jenis s.d. 31 Des 2025','idem','idem','dokumen resmi (sementara)'),
 (2025,'subsidized_electricity_customers',42.8,'juta pelanggan','pelanggan listrik bersubsidi 2025 (2024: 41,7; +2,6%)','idem','idem','dokumen resmi (sementara)'),
 (2024,'subsidized_electricity_customers',41.7,'juta pelanggan','pelanggan listrik bersubsidi 2024','idem','idem','dokumen resmi (sementara)'),
 (2024,'pln_lk_net_profit_restated',21.231284,'Rp triliun','laba tahun berjalan 2024 disajikan kembali (semula 17,763024); penyesuaian +3,468260 = beban pajak lebih catat','PLN, LK Audited 2025, Catatan 58','LK-PLN 2025 Audited.pdf (folder Data)','audited'),
 (2024,'pln_lk_deferred_tax_overstatement_dec2024',7.905235,'Rp triliun','lebih catat liabilitas pajak tangguhan 31 Des 2024 (1 Jan 2024: 4,436975); ekuitas induk naik 7,905 T menjadi 1.067.870 juta','PLN, LK Audited 2025, Catatan 58','LK-PLN 2025 Audited.pdf (folder Data)','audited'),
 (2025,'pln_lk_total_assets',1837.409908,'Rp triliun','JUMLAH ASET 31 Des 2025 (2024: 1.772,375266)','PLN, LK Audited 2025','LK-PLN 2025 Audited.pdf (folder Data)','audited'),
  (2025,'pln_lk_operating_profit',49.226013,'Rp triliun','laba usaha 2025 (2024: 60,621006)','PLN, LK Audited 2025','LK-PLN 2025 Audited.pdf (folder Data)','audited'),
  (2025,'pln_govt_receivable_compensation',84.864811,'Rp triliun','piutang kompensasi 31 Des 2025 (2024: 37,450898); saldo awal + pendapatan 112,734817 - kas 65,320904','PLN, LK Audited 2025, Note 16','LK-PLN 2025 Audited.pdf (folder Data)','audited'),
  (2025,'pln_govt_receivable_subsidy',12.26409,'Rp triliun','piutang subsidi listrik 31 Des 2025 (2024: 5,839850); akrual 87,460664 - kas 81,036424','PLN, LK Audited 2025, Notes 16/37','LK-PLN 2025 Audited.pdf (folder Data)','audited'),
  (2025,'pln_govt_receivable_discount_jan_feb',13.609498,'Rp triliun','piutang diskon tarif Jan-Feb 2025, diakui terpisah di luar G_t; menjelaskan selisih rekonsiliasi 67,447651-53,838153','PLN, LK Audited 2025, Note 16; BPKP Review + Kemenko letter 31-Dec-2025','LK-PLN 2025 Audited.pdf (folder Data)','audited'),
]

# ---- Ditemukan via Chrome 21 Sep 2026: LKPP 2025 audited, Laporan Kinerja Ditjen Gatrik 2025, APBN KiTa Sep 2026
LKPP='LKPP 2025 (Audited), DJPb Kemenkeu'; LKPPU='https://djpb.kemenkeu.go.id/portal/images/lkpp/LKPP-2025.pdf'
rows += [
 (2025,'apbn_electricity_subsidy_realized_lkpp_cash',81.036424,'Rp triliun','Belanja Subsidi Listrik (LRA, kas) TA 2025 Audited: Rp81.036.424.051.631; pagu 89,747 T (90,29%); 2024 Audited 75,817285',LKPP,LKPPU,'audited'),
 (2024,'apbn_electricity_subsidy_realized_lkpp_cash',75.817285,'Rp triliun','Belanja Subsidi Listrik TA 2024 Audited (Rp75.817.285.111.936) = 73,24 + 2,58 kurang bayar 2022 (Menkeu 6 Jan 2025)',LKPP,LKPPU,'audited'),
 (2025,'apbn_electricity_subsidy_budget_ceiling',89.74651,'Rp triliun','pagu Belanja Subsidi Listrik 2025 (Tabel kinerja LKPP, hlm. 142)',LKPP,LKPPU,'audited'),
 (2025,'apbn_electricity_subsidy_expense_accrual',87.460664,'Rp triliun','Beban Subsidi Listrik (LO, akrual) 2025: Rp87.460.663.602.008; 2024 = 77,045335; sama dengan pendapatan subsidi di LK PLN',LKPP,LKPPU,'audited'),
 (2024,'apbn_electricity_subsidy_expense_accrual',77.045335,'Rp triliun','Beban Subsidi Listrik (LO) 2024 (Rp77.045.334.864.270)',LKPP,LKPPU,'audited'),
 (2025,'macro_realized_gdp_growth_pct',5.11,'%','realisasi pertumbuhan ekonomi 2025 (2024: 5,03); asumsi APBN 5,2','BPK, LHR atas Pelaksanaan Transparansi Fiskal TA 2025 (LKPP 2025)','https://www.bpk.go.id/assets/files/lkpp/2025/lkpp_2025_1784027527.pdf','audited'),
 (2025,'macro_realized_inflation_yoy_pct',2.92,'%','inflasi 2025 y/y (2024: 1,57); asumsi APBN 2,5','BPK, LHR atas Pelaksanaan Transparansi Fiskal TA 2025 (LKPP 2025)','https://www.bpk.go.id/assets/files/lkpp/2025/lkpp_2025_1784027527.pdf','audited'),
 (2025,'macro_realized_usdidr_avg',16475,'Rp/USD','rata-rata kurs 2025; asumsi APBN 16.000','BPK, LHR atas Pelaksanaan Transparansi Fiskal TA 2025 (LKPP 2025)','https://www.bpk.go.id/assets/files/lkpp/2025/lkpp_2025_1784027527.pdf','audited'),
 (2025,'macro_realized_sbn10y_pct',6.71,'%','yield SBN 10 tahun 2025 (ytd); asumsi 7,0; 2024: 6,78','BPK, LHR atas Pelaksanaan Transparansi Fiskal TA 2025 (LKPP 2025)','https://www.bpk.go.id/assets/files/lkpp/2025/lkpp_2025_1784027527.pdf','audited'),
 (2025,'macro_realized_icp_usd_bbl',67.38,'USD/barel','realisasi ICP rata-rata 2025 (2024: 78,14); asumsi APBN 82','BPK, LHR atas Pelaksanaan Transparansi Fiskal TA 2025 (LKPP 2025)','https://www.bpk.go.id/assets/files/lkpp/2025/lkpp_2025_1784027527.pdf','audited'),
 (2024,'macro_realized_icp_usd_bbl',78.14,'USD/barel','realisasi ICP rata-rata 2024','BPK, LHR atas Pelaksanaan Transparansi Fiskal TA 2025 (LKPP 2025)','https://www.bpk.go.id/assets/files/lkpp/2025/lkpp_2025_1784027527.pdf','audited'),
 (2025,'macro_realized_oil_lifting_kbpd',605.86,'ribu bph','lifting minyak 2025; target APBN 605','BPK, LHR atas Pelaksanaan Transparansi Fiskal TA 2025 (LKPP 2025)','https://www.bpk.go.id/assets/files/lkpp/2025/lkpp_2025_1784027527.pdf','audited'),
 (2025,'ebt_capacity_total_mw_esdm',15630,'MW','kapasitas pembangkit EBT Des 2025 (definisi Ditjen EBTKE/ESDM: total, bukan seri on-grid Handbook)','Ditjen Gatrik ESDM, berita 22 Jan 2026 (Rapat Kerja Komisi XII DPR)','https://gatrik.esdm.go.id/berita/di-depan-dpr-menteri-esdm-paparkan-capaian-positif-subsektor-ketenagalistrikan','pernyataan resmi'),
 (2025,'ebt_capacity_added_plta_mw',531.2,'MW','tambahan 2025','idem','idem','pernyataan resmi'),
 (2025,'ebt_capacity_added_plts_mw',584.7,'MW','tambahan 2025','idem','idem','pernyataan resmi'),
 (2025,'ebt_capacity_added_pltp_mw',105.2,'MW','tambahan 2025','idem','idem','pernyataan resmi'),
 (2025,'ebt_capacity_added_pltbio_mw',84.5,'MW','tambahan 2025','idem','idem','pernyataan resmi'),
 (2025,'ebt_capacity_added_total_mw',1305.6,'MW','jumlah keempat jenis = 1,3 GW yang disebut Menteri; terbesar 5 tahun terakhir','idem','idem','pernyataan resmi'),
 (2025,'national_installed_capacity_gw',107.51,'GW','kapasitas terpasang nasional 2025, +sekitar 7 GW (mayoritas fosil/batu bara)','idem','idem','pernyataan resmi'),
 (2025,'electricity_consumption_per_capita_kwh',1584,'kWh/kapita','konsumsi listrik per kapita 2025 (2024: 1.411)','idem','idem','pernyataan resmi'),
 (2025,'apbn_electricity_compensation_realized_lkpp_cash',65.3209,'Rp triliun','Kompensasi Tarif Tenaga Listrik 2025 (realisasi kas), pagu 92,411 T (70,69%); pembayaran kompensasi ditunda -> utang kompensasi',LKPP,LKPPU,'audited'),
 (2025,'apbn_electricity_compensation_budget_ceiling',92.41119,'Rp triliun','pagu Kompensasi Tarif Tenaga Listrik 2025',LKPP,LKPPU,'audited'),
 (2025,'apbn_electricity_subsidy_volume_twh_realized',69.66,'TWh','volume keluaran Subsidi Listrik 2025 (teks PDF terbaca "75,55 | 69,66": target 75,55; realisasi 69,66; urutan kolom dari ekstraksi, bukan tabel bersih)',LKPP,LKPPU,'audited; ekstraksi teks'),
 (2025,'apbn_electricity_compensation_volume_twh_realized',222.16,'TWh','volume keluaran Kompensasi Tarif Listrik 2025 (target 195)',LKPP,LKPPU,'audited'),
 (2020,'subsidized_electricity_gwh_realized',59002,'GWh','realisasi energi listrik bersubsidi (Renstra ESDM 2025-2029), target 60.080','Laporan Kinerja Ditjen Ketenagalistrikan 2025, Tabel 7','https://gatrik.artristik.co.id/gatrik-api//storage/migrasi/download_index/files/d35ab-laporan-kinerja-direktorat-jenderal-ketenagalistrikan-tahun-2025-published-tte-_compressed-1-.pdf','resmi'),
 (2021,'subsidized_electricity_gwh_realized',61916,'GWh','target 64.258','idem','idem','resmi'),
 (2022,'subsidized_electricity_gwh_realized',62248,'GWh','target 68.894','idem','idem','resmi'),
 (2023,'subsidized_electricity_gwh_realized',66034,'GWh','target 73.609','idem','idem','resmi'),
 (2024,'subsidized_electricity_gwh_realized',70807,'GWh','target 78.191','idem','idem','resmi'),
 (2025,'subsidized_household_allocation_gwh_q1',19349.53,'GWh','alokasi listrik RT miskin/rentan yang disubsidi, capaian Triwulan I 2025 (target 17.057,75) -- bukan setahun penuh','idem','idem','resmi; parsial'),
 (2026,'subsidized_customers_million_jan_aug',43.3,'juta pelanggan','pelanggan listrik bersubsidi s.d. Agu 2026 (+2,1% dari 42,4 juta)','Kemenkeu, Konferensi Pers APBN KiTa Sep 2026','http://media.kemenkeu.go.id/getmedia/04ced8b6-ddc6-4127-8cda-73e39ef5cbee/Publikasi-Web-Konpers-APBN-KiTa-(Sept-2026).pdf','resmi'),
]
# proksi BPP turunan (BUKAN BPP resmi): biaya usaha (+ beban keuangan) PLN / energi terjual, dari Statistik PLN 2025 Tabel 63 & 46
_R = os.path.join(HERE,'..','Regional-Disparity-Dataset')
_ts = pd.read_csv(os.path.join(_R,'pln_national_timeseries_2016_2025.csv')).set_index('year')
_fin = pd.read_csv(os.path.join(_R,'pln_stat2025_financial_timeseries_long.csv'))
def _f(item,y): return _fin[(_fin.table==63)&_fin.item.str.startswith(item)&(_fin.year==y)].value.iloc[0]
for _y in range(2021,2026):
    _opex=_f('Jumlah Beban Usaha',_y); _fe=-_f('Beban Keuangan',_y); _gwh=_ts.loc[_y,'gwh_sold_total']
    rows.append((_y,'derived_bpp_proxy_opex_per_kwh_sold',round(_opex/_gwh,1),'Rp/kWh',f'TURUNAN: Jumlah Beban Usaha {_opex:,.0f} juta Rp / energi terjual {_gwh:,.2f} GWh; mencakup biaya usaha saja (tanpa beban keuangan); pembagi = energi terjual -> bukan BPP resmi','dihitung dari Statistik PLN 2025 T63 & T46','pln_stat2025_financial_timeseries_long.csv','turunan'))
    rows.append((_y,'derived_bpp_proxy_opex_plus_finance_per_kwh_sold',round((_opex+_fe)/_gwh,1),'Rp/kWh',f'TURUNAN: (Beban Usaha + Beban Keuangan {_fe:,.0f}) / energi terjual; bukan BPP resmi (BPP resmi dihitung PLN/ESDM per Kepmen dan tidak dipublikasikan untuk realisasi 2025 di sumber yang dapat dibaca)','idem','idem','turunan'))
d = pd.DataFrame(rows, columns=['year','item','value','unit','note','source','url','status'])
d.to_csv(f'{HERE}/news_updates_2024_2026.csv', index=False)
fails=[]
def chk(n,ok,det=''):
    print(('PASS ' if ok else 'FAIL ')+n,det)
    if not ok: fails.append(n)
g = pd.read_csv(f'{HERE}/pln_gov_support_2015_2024.csv').set_index('year')
v = d.set_index(['year','item']).value
chk('2024: 73,24 + 2,58 = 75,8 (+-0,05)', abs(73.24+v[(2024,'apbn_electricity_subsidy_arrears_2022_paid')]-v[(2024,'apbn_electricity_subsidy_realized_prelim')])<=0.05)
chk('2024: subsidi LK PLN (Statistik 2024) = LK Audited 2024 di panel (+-0,01 T)', abs(v[(2024,'pln_lk_subsidy_revenue')]-g.loc[2024,'subsidy_trn'])<=0.01, f"{v[(2024,'pln_lk_subsidy_revenue')]:.3f} vs {g.loc[2024,'subsidy_trn']:.3f}")
chk('2024: kompensasi LK PLN (Statistik 2024) = LK Audited 2024 (+-0,01 T)', abs(v[(2024,'pln_lk_compensation_revenue')]-g.loc[2024,'compensation_trn'])<=0.01, f"{v[(2024,'pln_lk_compensation_revenue')]:.3f} vs {g.loc[2024,'compensation_trn']:.3f}")
chk('2026 - 2025 (Jan-Agu) = kenaikan yang dilaporkan (+-1)', abs(v[(2026,'energy_subsidy_compensation_jan_aug')]-v[(2025,'energy_subsidy_compensation_jan_aug')]-v[(2026,'energy_subsidy_compensation_jan_aug_yoy_increase')])<=1)
chk('2025: subsidi+kompensasi listrik Rp210 T mengikuti tren (>= LK PLN 2024, Rp177 T)', v[(2025,'electricity_subsidy_and_compensation_total')]>g.loc[2024,'gov_support_trn'], f"{v[(2025,'electricity_subsidy_and_compensation_total')]} vs {g.loc[2024,'gov_support_trn']:.1f}")
chk('2025: pendapatan usaha 582,68 vs 2024 545,38 naik ~6,8% (+-0,1)', abs((582.68/545.380993-1)*100-6.84)<=0.1)
chk('2025: piutang pemerintah 110,73 / 43,29 -1 = 155,8% (+-0,5)', abs((110.73/g.loc[2024,'govt_receivable_trn']-1)*100-155.8)<=0.5, f"{g.loc[2024,'govt_receivable_trn']:.2f}")
chk('2025: rugi kurs 2024 pembanding 6,78 = panel E (+-0,01)', abs(6.78-6.780398)<=0.01)
chk('2025: laba sebelum pajak 12,99 - pajak 5,73 = laba 7,26 (+-0,02)', abs(12.99-5.73-7.26)<=0.02)
chk('2025: subsidi+kompensasi 200,19 = 87,46+112,73 (+-0,01) dan naik dari 2024', abs(v[(2025,'pln_lk_gov_support_total')]-v[(2025,'pln_lk_subsidy_revenue')]-v[(2025,'pln_lk_compensation_revenue')])<=0.01 and v[(2025,'pln_lk_gov_support_total')]>g.loc[2024,'gov_support_trn'])
chk('2026: 104,6/89 -1 = 17,5% (+-0,2)', abs((104.6/89-1)*100-17.5)<=0.2)
chk('2025 Jan-Agu: subsidi 48,1 + kompensasi 37,5 + kurang bayar 2,0 = 87,6 (+-0,05)', abs(48.1+37.5+2.0-87.6)<=0.05)
chk('2025: penjualan 317,69 TWh / 306,21 = +3,75% (+-0,05)', abs((317.69/306.21-1)*100-3.75)<=0.05)
chk('2025: selisih laba 2024 pembanding media 21,23 vs LK 17,76 = 3,47 T (dicatat)', abs(21.23-17.763024-3.47)<=0.01)
chk('2026: proyeksi subsidi energi 227,26 > rata-rata 2022-25 174,73', 227.26>174.73)
chk('Kemenkeu 2024: subsidi energi 21,6 + 80,2 + 75,8 = 177,6 (+-0,05)', abs(21.6+80.2+75.8-177.6)<=0.05)
chk('Kemenkeu 2024: subsidi 177,6 + kompensasi 209,3 = 386,9 (+-0,05)', abs(177.6+209.3-386.9)<=0.05)
chk('Kemenkeu 2025 alokasi: 26,7 + 87,0 + 89,7 = 203,4; + kompensasi 190,9 = 394,3 (+-0,05)', abs(26.7+87.0+89.7-203.4)<=0.05 and abs(203.4+190.9-394.3)<=0.05)
chk('Kemenkeu subsidi listrik 2024 (75,8) = Menkeu 6 Jan 2025 = LK: (73,24+2,58)', abs(v[(2024,'apbn_electricity_subsidy_realized_kemenkeu')]-v[(2024,'apbn_electricity_subsidy_realized_prelim')])<=0.01)
chk('900VA: 1.800 - 600 = 1.200 dan 1.200/1.800 = 67% (+-0,5)', abs(1800-600-1200)<=0.01 and abs(1200/1800*100-67)<=0.5)
chk('proksi harga seharusnya 900VA (1.800) mendekati proyeksi BPP RUPTL 2025 (1.829) dan pernyataan Dirut (1.600-1.700) dalam 12%', abs(1800/1829-1)<0.12 and 1600*0.9<1800<1700*1.12)
chk('pelanggan bersubsidi 41,7 -> 42,8 = +2,6% (+-0,1)', abs((42.8/41.7-1)*100-2.6)<=0.1)
chk('2025 subsidi+kompensasi 401,6 > total subsidi semua jenis 281,6 (implied kompensasi ~120,0)', 401.6>281.6)
E = pd.read_csv(os.path.join(HERE,'..','PLN-Health-Dataset','pln_financial_panel.csv')).set_index('year')
def near(a,b,t): return abs(a-b)<=t
chk('LK Audited 2025 (panel E): pendapatan 582,68 = media (+-0,01 T)', near(E.loc[2025,'rev_total_reported']/1e6,582.68,0.01))
chk('LK Audited 2025: subsidi 87,46 dan kompensasi 112,73 = media Katadata (+-0,01 T)', near(E.loc[2025,'subsidy']/1e6,87.46,0.01) and near(E.loc[2025,'compensation']/1e6,112.73,0.01))
chk('LK Audited 2025: piutang pemerintah 110,74 (media 110,73) (+-0,02 T)', near(E.loc[2025,'govt_receivable']/1e6,110.73,0.02), f"{E.loc[2025,'govt_receivable']/1e6:.3f}")
chk('LK Audited 2025: laba 7,2607 = CNBC 7,26 dan Katadata ~7,0 tidak tepat (+-0,01 vs CNBC)', near(E.loc[2025,'profit_year']/1e6,7.26,0.01))
chk('LK Audited 2025: rugi kurs 12,462 = media 12,46 (+-0,01)', near(-E.loc[2025,'fx_gain_loss']/1e6,12.46,0.01))
chk('Restatement 2024: 17,763024 + 3,468260 = 21,231284 (+-0,000001) dan = panel E kolom _restated', near(17.763024+3.468260,21.231284,1e-6) and near(E.loc[2024,'profit_year_restated_next_report']/1e6,21.231284,1e-6))
chk('Restatement 2024: laba sebelum pajak tidak berubah 28,269959 dan pajak 10,506935 -> 7,038675 (selisih 3,468260)', near(10.506935-7.038675,3.468260,1e-6))
chk('Restatement 2024: ekuitas naik 7,905235 = penurunan liabilitas (panel E)', near((E.loc[2024,'total_equity_restated_next_report']-E.loc[2024,'total_equity'])/1e6,7.905235,1e-6) and near((E.loc[2024,'total_liab']-E.loc[2024,'total_liab_restated_next_report'])/1e6,7.905235,1e-6))
chk('2025: subsidi+kompensasi (dukungan pemerintah) 200,195 = panel E gov_support', near(E.loc[2025,'gov_support']/1e6,200.195481,0.01), f"{E.loc[2025,'gov_support']/1e6:.3f}")

chk('LKPP 2025: subsidi listrik 81,036424 / pagu 89,74651 = 90,29% (+-0,01)', abs(81.036424/89.74651*100-90.29)<=0.01)
chk('LKPP 2025: kompensasi listrik 65,3209 / pagu 92,41119 = 70,69% (+-0,01)', abs(65.3209/92.41119*100-70.69)<=0.01)
chk('LKPP 2024 kas 75,817285 = Kemenkeu 75,8 (+-0,05) dan 73,24 + 2,58 (+-0,05)', abs(75.817285-75.8)<=0.05 and abs(73.24+2.58-75.817285)<=0.05)
chk('Beban subsidi listrik akrual 2025 (87,460664) = subsidi di LK PLN dan panel E (+-0,001 T)', abs(87.460664-E.loc[2025,'subsidy']/1e6)<=0.001, f"{E.loc[2025,'subsidy']/1e6:.6f}")
chk('Beban subsidi listrik akrual 2024 (77,045335) = LK Audited 2024 di panel (+-0,001 T)', abs(77.045335-g.loc[2024,'subsidy_trn'])<=0.001)
chk('akrual - kas: 2025 = 6,42 T (subsidi terutang, 2024: 1,23 T) dicatat', abs(87.460664-81.036424-6.42424)<=1e-6 and abs(77.045335-75.817285-1.22805)<=1e-6)
chk('kompensasi akrual LK PLN 2025 (112,73) > kompensasi kas (65,32): selisih ~47,4 T = utang kompensasi yang belum dibayar (proksi)', 112.73>65.3209, f"{112.73-65.3209:.2f}")
chk('Gatrik: subsidi listrik 2020-2024 (47,99/49,80/58,83/68,64/77,04) 2021-2024 = pendapatan subsidi LK PLN (+-0,01)', abs(49.80-49.796949)<=0.01 and abs(58.83-58.83196)<=0.01 and abs(68.64-68.636731)<=0.01 and abs(77.04-77.045335)<=0.01)
_p = d[d.item=='derived_bpp_proxy_opex_plus_finance_per_kwh_sold'].set_index('year').value
chk('proksi BPP 2025 (biaya usaha+keuangan / kWh) dalam 1.500-2.000 dan dekat proyeksi RUPTL 1.829 (+-10%)', 1500<_p[2025]<2000 and abs(_p[2025]/1829-1)<=0.10, f"{_p[2025]}")
chk('proksi BPP naik 2021->2025 (bukan nilai resmi)', _p[2025]>_p[2021], f"{_p[2021]} -> {_p[2025]}")
chk('volume kompensasi 222,16 TWh ~ penjualan total 317,69 TWh (70%): masuk akal (<= total)', 222.16<317.69)
chk('kurs realisasi 2025 (16.475, LKPP) = rata-rata panel kurs D 2025 (16.474) dalam 0,1%', abs(16475/pd.read_csv(os.path.join(HERE,'..','FX-Risk-Dataset','fx_annual_panel.csv')).set_index('year').loc[2025,'fx_avg']-1)<0.001)
chk('tambahan EBT 2025 = PLTA+PLTS+PLTP+PLTBio (+-0,1 MW) dan = 1,3 GW yang dinyatakan (+-0,05 GW)', abs(531.2+584.7+105.2+84.5-1305.6)<=0.1 and abs(1305.6/1000-1.3)<=0.05)
chk('ICP 2025 realisasi (67,38) di bawah asumsi APBN (82) dan realisasi 2024 (78,14)', 67.38<82 and 67.38<78.14)
chk('realisasi 2025 vs asumsi APBN tercatat: kurs lebih lemah (+3,0%), inflasi lebih tinggi (2,92>2,5)', 16475>16000 and 2.92>2.5)
chk('bridge 2025: kompensasi 37,450898+112,734817-65,320904=84,864811 (+-0,001)', abs(37.450898+112.734817-65.320904-84.864811)<=0.001)
chk('bridge 2025: subsidi 5,839850+87,460664-81,036424=12,264090 (+-0,001)', abs(5.839850+87.460664-81.036424-12.264090)<=0.001)
chk('bridge 2025: 84,864811+12,264090+13,609498=110,738399 total piutang (+-0,001)', abs(84.864811+12.264090+13.609498-110.738399)<=0.001)
chk('bridge 2025: kenaikan 67,447651 = akrual-kas 53,838153 + diskon 13,609498 (+-0,001)', abs(67.447651-53.838153-13.609498)<=0.001)
print('news updates OK' if not fails else 'FAILED'); 
if fails: raise SystemExit(1)
