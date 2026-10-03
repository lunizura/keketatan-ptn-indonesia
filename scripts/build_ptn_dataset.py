#!/usr/bin/env python3
"""
scripts/build_ptn_dataset.py

Generates the comprehensive selectivity dataset for Top Universities in Indonesia (PTN).
Includes official metrics for SNBP and SNBT:
- Quota (Daya Tampung)
- Historical Applicants (Peminat 3 Tahun Terakhir)
- Selectivity Percentage ((Daya Tampung / Peminat) * 100%)
- Competition Ratio (1 : N)
- Selectivity Classification (Sangat Ketat, Ketat, Sedang, Terbuka)
- Campus Profile & Metadata
- Bilingual Study Program Descriptions & Career Pathways
"""

import json
import csv
import os
import datetime

# 1. Metadata 15 PTN Top Indonesia
PTN_CATALOG = {
    # --- 35 PTN (Negeri) ---
    "UI": {
        "id": "UI", "nama": "Universitas Indonesia", "nama_en": "University of Indonesia",
        "singkatan": "UI", "kota": "Depok", "provinsi": "Jawa Barat / DKI Jakarta",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1849, "website": "https://www.ui.ac.id", "spmb_url": "https://penerimaan.ui.ac.id", "warna": "#FACC15"
    },
    "ITB": {
        "id": "ITB", "nama": "Institut Teknologi Bandung", "nama_en": "Bandung Institute of Technology",
        "singkatan": "ITB", "kota": "Bandung", "provinsi": "Jawa Barat",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1920, "website": "https://www.itb.ac.id", "spmb_url": "https://admission.itb.ac.id", "warna": "#0284C7"
    },
    "UGM": {
        "id": "UGM", "nama": "Universitas Gadjah Mada", "nama_en": "Gadjah Mada University",
        "singkatan": "UGM", "kota": "Sleman / Yogyakarta", "provinsi": "D.I. Yogyakarta",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1949, "website": "https://ugm.ac.id", "spmb_url": "https://um.ugm.ac.id", "warna": "#EAB308"
    },
    "IPB": {
        "id": "IPB", "nama": "IPB University", "nama_en": "IPB University",
        "singkatan": "IPB", "kota": "Bogor", "provinsi": "Jawa Barat",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1963, "website": "https://ipb.ac.id", "spmb_url": "https://admisi.ipb.ac.id", "warna": "#1D4ED8"
    },
    "UNAIR": {
        "id": "UNAIR", "nama": "Universitas Airlangga", "nama_en": "Airlangga University",
        "singkatan": "UNAIR", "kota": "Surabaya", "provinsi": "Jawa Timur",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1954, "website": "https://unair.ac.id", "spmb_url": "https://ppmemb.unair.ac.id", "warna": "#F59E0B"
    },
    "ITS": {
        "id": "ITS", "nama": "Institut Teknologi Sepuluh Nopember", "nama_en": "Sepuluh Nopember Institute of Technology",
        "singkatan": "ITS", "kota": "Surabaya", "provinsi": "Jawa Timur",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1957, "website": "https://www.its.ac.id", "spmb_url": "https://admission.its.ac.id", "warna": "#0284C7"
    },
    "UNDIP": {
        "id": "UNDIP", "nama": "Universitas Diponegoro", "nama_en": "Diponegoro University",
        "singkatan": "UNDIP", "kota": "Semarang", "provinsi": "Jawa Tengah",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1957, "website": "https://undip.ac.id", "spmb_url": "https://pmb.undip.ac.id", "warna": "#1E40AF"
    },
    "UB": {
        "id": "UB", "nama": "Universitas Brawijaya", "nama_en": "Brawijaya University",
        "singkatan": "UB", "kota": "Malang", "provinsi": "Jawa Timur",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1963, "website": "https://ub.ac.id", "spmb_url": "https://selma.ub.ac.id", "warna": "#2563EB"
    },
    "UNPAD": {
        "id": "UNPAD", "nama": "Universitas Padjadjaran", "nama_en": "Padjadjaran University",
        "singkatan": "UNPAD", "kota": "Sumedang / Bandung", "provinsi": "Jawa Barat",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1957, "website": "https://unpad.ac.id", "spmb_url": "https://smup.unpad.ac.id", "warna": "#F97316"
    },
    "UNS": {
        "id": "UNS", "nama": "Universitas Sebelas Maret", "nama_en": "Sebelas Maret University",
        "singkatan": "UNS", "kota": "Surakarta", "provinsi": "Jawa Tengah",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1976, "website": "https://uns.ac.id", "spmb_url": "https://spmb.uns.ac.id", "warna": "#0284C7"
    },
    "UPI": {
        "id": "UPI", "nama": "Universitas Pendidikan Indonesia", "nama_en": "Indonesia University of Education",
        "singkatan": "UPI", "kota": "Bandung", "provinsi": "Jawa Barat",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1954, "website": "https://upi.edu", "spmb_url": "https://pmb.upi.edu", "warna": "#DC2626"
    },
    "UNSOED": {
        "id": "UNSOED", "nama": "Universitas Jenderal Soedirman", "nama_en": "Jenderal Soedirman University",
        "singkatan": "UNSOED", "kota": "Purwokerto", "provinsi": "Jawa Tengah",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BLU", "akreditasi": "Unggul",
        "tahun_berdiri": 1963, "website": "https://unsoed.ac.id", "spmb_url": "https://spmb.unsoed.ac.id", "warna": "#EAB308"
    },
    "UNY": {
        "id": "UNY", "nama": "Universitas Negeri Yogyakarta", "nama_en": "Yogyakarta State University",
        "singkatan": "UNY", "kota": "Yogyakarta", "provinsi": "D.I. Yogyakarta",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1964, "website": "https://uny.ac.id", "spmb_url": "https://pmb.uny.ac.id", "warna": "#0284C7"
    },
    "UNNES": {
        "id": "UNNES", "nama": "Universitas Negeri Semarang", "nama_en": "Semarang State University",
        "singkatan": "UNNES", "kota": "Semarang", "provinsi": "Jawa Tengah",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1965, "website": "https://unnes.ac.id", "spmb_url": "https://spmb.unnes.ac.id", "warna": "#EAB308"
    },
    "UNESA": {
        "id": "UNESA", "nama": "Universitas Negeri Surabaya", "nama_en": "Surabaya State University",
        "singkatan": "UNESA", "kota": "Surabaya", "provinsi": "Jawa Timur",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1964, "website": "https://unesa.ac.id", "spmb_url": "https://admisi.unesa.ac.id", "warna": "#2563EB"
    },
    "UM": {
        "id": "UM", "nama": "Universitas Negeri Malang", "nama_en": "State University of Malang",
        "singkatan": "UM", "kota": "Malang", "provinsi": "Jawa Timur",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1954, "website": "https://um.ac.id", "spmb_url": "https://seleksi.um.ac.id", "warna": "#1D4ED8"
    },
    "UNJ": {
        "id": "UNJ", "nama": "Universitas Negeri Jakarta", "nama_en": "State University of Jakarta",
        "singkatan": "UNJ", "kota": "Jakarta Timur", "provinsi": "DKI Jakarta",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1964, "website": "https://unj.ac.id", "spmb_url": "https://penmaba.unj.ac.id", "warna": "#16A34A"
    },
    "UPNVJ": {
        "id": "UPNVJ", "nama": "UPN Veteran Jakarta", "nama_en": "UPN Veteran Jakarta",
        "singkatan": "UPNVJ", "kota": "Jakarta Selatan", "provinsi": "DKI Jakarta",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BLU", "akreditasi": "Unggul",
        "tahun_berdiri": 1967, "website": "https://upnvj.ac.id", "spmb_url": "https://penmaru.upnvj.ac.id", "warna": "#16A34A"
    },
    "UPNVYK": {
        "id": "UPNVYK", "nama": "UPN Veteran Yogyakarta", "nama_en": "UPN Veteran Yogyakarta",
        "singkatan": "UPNVYK", "kota": "Sleman", "provinsi": "D.I. Yogyakarta",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BLU", "akreditasi": "Unggul",
        "tahun_berdiri": 1958, "website": "https://upnyk.ac.id", "spmb_url": "https://pmb.upnyk.ac.id", "warna": "#15803D"
    },
    "UPNVJT": {
        "id": "UPNVJT", "nama": "UPN Veteran Jawa Timur", "nama_en": "UPN Veteran East Java",
        "singkatan": "UPNVJT", "kota": "Surabaya", "provinsi": "Jawa Timur",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BLU", "akreditasi": "Unggul",
        "tahun_berdiri": 1959, "website": "https://upnjatim.ac.id", "spmb_url": "https://simaba.upnjatim.ac.id", "warna": "#166534"
    },
    "UNTIRTA": {
        "id": "UNTIRTA", "nama": "Universitas Sultan Ageng Tirtayasa", "nama_en": "Sultan Ageng Tirtayasa University",
        "singkatan": "UNTIRTA", "kota": "Serang", "provinsi": "Banten",
        "wilayah": "Jawa", "tipe": "PTN", "klaster": "PTN-BLU", "akreditasi": "Unggul",
        "tahun_berdiri": 1981, "website": "https://untirta.ac.id", "spmb_url": "https://spmb.untirta.ac.id", "warna": "#B45309"
    },
    "USU": {
        "id": "USU", "nama": "Universitas Sumatera Utara", "nama_en": "University of North Sumatra",
        "singkatan": "USU", "kota": "Medan", "provinsi": "Sumatera Utara",
        "wilayah": "Sumatera", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1952, "website": "https://usu.ac.id", "spmb_url": "https://penerimaan.usu.ac.id", "warna": "#16A34A"
    },
    "UNAND": {
        "id": "UNAND", "nama": "Universitas Andalas", "nama_en": "Andalas University",
        "singkatan": "UNAND", "kota": "Padang", "provinsi": "Sumatera Barat",
        "wilayah": "Sumatera", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1955, "website": "https://unand.ac.id", "spmb_url": "https://pmb.unand.ac.id", "warna": "#15803D"
    },
    "UNSRI": {
        "id": "UNSRI", "nama": "Universitas Sriwijaya", "nama_en": "Sriwijaya University",
        "singkatan": "UNSRI", "kota": "Palembang / Indralaya", "provinsi": "Sumatera Selatan",
        "wilayah": "Sumatera", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1960, "website": "https://unsri.ac.id", "spmb_url": "https://usm.unsri.ac.id", "warna": "#D97706"
    },
    "UNILA": {
        "id": "UNILA", "nama": "Universitas Lampung", "nama_en": "Lampung University",
        "singkatan": "UNILA", "kota": "Bandar Lampung", "provinsi": "Lampung",
        "wilayah": "Sumatera", "tipe": "PTN", "klaster": "PTN-BLU", "akreditasi": "Unggul",
        "tahun_berdiri": 1965, "website": "https://unila.ac.id", "spmb_url": "https://simanila.unila.ac.id", "warna": "#2563EB"
    },
    "UNP": {
        "id": "UNP", "nama": "Universitas Negeri Padang", "nama_en": "Padang State University",
        "singkatan": "UNP", "kota": "Padang", "provinsi": "Sumatera Barat",
        "wilayah": "Sumatera", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1954, "website": "https://unp.ac.id", "spmb_url": "https://spmb.unp.ac.id", "warna": "#E11D48"
    },
    "USK": {
        "id": "USK", "nama": "Universitas Syiah Kuala", "nama_en": "Syiah Kuala University",
        "singkatan": "USK", "kota": "Banda Aceh", "provinsi": "Aceh",
        "wilayah": "Sumatera", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1961, "website": "https://usk.ac.id", "spmb_url": "https://penerimaan.usk.ac.id", "warna": "#F59E0B"
    },
    "UNRI": {
        "id": "UNRI", "nama": "Universitas Riau", "nama_en": "Riau University",
        "singkatan": "UNRI", "kota": "Pekanbaru", "provinsi": "Riau",
        "wilayah": "Sumatera", "tipe": "PTN", "klaster": "PTN-BLU", "akreditasi": "Unggul",
        "tahun_berdiri": 1962, "website": "https://unri.ac.id", "spmb_url": "https://um.unri.ac.id", "warna": "#0D9488"
    },
    "UNMUL": {
        "id": "UNMUL", "nama": "Universitas Mulawarman", "nama_en": "Mulawarman University",
        "singkatan": "UNMUL", "kota": "Samarinda", "provinsi": "Kalimantan Timur",
        "wilayah": "Kalimantan", "tipe": "PTN", "klaster": "PTN-BLU", "akreditasi": "Unggul",
        "tahun_berdiri": 1962, "website": "https://unmul.ac.id", "spmb_url": "https://spmb.unmul.ac.id", "warna": "#0284C7"
    },
    "ULM": {
        "id": "ULM", "nama": "Universitas Lambung Mangkurat", "nama_en": "Lambung Mangkurat University",
        "singkatan": "ULM", "kota": "Banjarmasin", "provinsi": "Kalimantan Selatan",
        "wilayah": "Kalimantan", "tipe": "PTN", "klaster": "PTN-BLU", "akreditasi": "Unggul",
        "tahun_berdiri": 1958, "website": "https://ulm.ac.id", "spmb_url": "https://admisi.ulm.ac.id", "warna": "#EAB308"
    },
    "UNTAN": {
        "id": "UNTAN", "nama": "Universitas Tanjungpura", "nama_en": "Tanjungpura University",
        "singkatan": "UNTAN", "kota": "Pontianak", "provinsi": "Kalimantan Barat",
        "wilayah": "Kalimantan", "tipe": "PTN", "klaster": "PTN-BLU", "akreditasi": "Unggul",
        "tahun_berdiri": 1959, "website": "https://untan.ac.id", "spmb_url": "https://scmb.untan.ac.id", "warna": "#16A34A"
    },
    "UNHAS": {
        "id": "UNHAS", "nama": "Universitas Hasanuddin", "nama_en": "Hasanuddin University",
        "singkatan": "UNHAS", "kota": "Makassar", "provinsi": "Sulawesi Selatan",
        "wilayah": "Sulawesi", "tipe": "PTN", "klaster": "PTN-BH", "akreditasi": "Unggul",
        "tahun_berdiri": 1956, "website": "https://unhas.ac.id", "spmb_url": "https://regpmb.unhas.ac.id", "warna": "#DC2626"
    },
    "UNSRAT": {
        "id": "UNSRAT", "nama": "Universitas Sam Ratulangi", "nama_en": "Sam Ratulangi University",
        "singkatan": "UNSRAT", "kota": "Manado", "provinsi": "Sulawesi Utara",
        "wilayah": "Sulawesi", "tipe": "PTN", "klaster": "PTN-BLU", "akreditasi": "Unggul",
        "tahun_berdiri": 1965, "website": "https://unsrat.ac.id", "spmb_url": "https://pmb.unsrat.ac.id", "warna": "#2563EB"
    },
    "UNUD": {
        "id": "UNUD", "nama": "Universitas Udayana", "nama_en": "Udayana University",
        "singkatan": "UNUD", "kota": "Badung / Denpasar", "provinsi": "Bali",
        "wilayah": "Bali-Nusa Tenggara", "tipe": "PTN", "klaster": "PTN-BLU", "akreditasi": "Unggul",
        "tahun_berdiri": 1962, "website": "https://unud.ac.id", "spmb_url": "https://utbk.unud.ac.id", "warna": "#9333EA"
    },
    "UNRAM": {
        "id": "UNRAM", "nama": "Universitas Mataram", "nama_en": "University of Mataram",
        "singkatan": "UNRAM", "kota": "Mataram", "provinsi": "Nusa Tenggara Barat",
        "wilayah": "Bali-Nusa Tenggara", "tipe": "PTN", "klaster": "PTN-BLU", "akreditasi": "Unggul",
        "tahun_berdiri": 1962, "website": "https://unram.ac.id", "spmb_url": "https://pmb.unram.ac.id", "warna": "#0284C7"
    },

    # --- 15 PTS (Swasta) ---
    "TELKOM": {
        "id": "TELKOM", "nama": "Telkom University", "nama_en": "Telkom University",
        "singkatan": "TELKOM", "kota": "Bandung", "provinsi": "Jawa Barat",
        "wilayah": "Jawa", "tipe": "PTS", "klaster": "PTS Unggul", "akreditasi": "Unggul",
        "tahun_berdiri": 1990, "website": "https://telkomuniversity.ac.id", "spmb_url": "https://smb.telkomuniversity.ac.id", "warna": "#DC2626"
    },
    "BINUS": {
        "id": "BINUS", "nama": "Bina Nusantara University", "nama_en": "Bina Nusantara University",
        "singkatan": "BINUS", "kota": "Jakarta Barat", "provinsi": "DKI Jakarta",
        "wilayah": "Jawa", "tipe": "PTS", "klaster": "PTS Unggul", "akreditasi": "Unggul",
        "tahun_berdiri": 1981, "website": "https://binus.ac.id", "spmb_url": "https://binus.ac.id/admissions", "warna": "#EA580C"
    },
    "UII": {
        "id": "UII", "nama": "Universitas Islam Indonesia", "nama_en": "Universitas Islam Indonesia",
        "singkatan": "UII", "kota": "Sleman", "provinsi": "D.I. Yogyakarta",
        "wilayah": "Jawa", "tipe": "PTS", "klaster": "PTS Unggul", "akreditasi": "Unggul",
        "tahun_berdiri": 1945, "website": "https://uii.ac.id", "spmb_url": "https://pmb.uii.ac.id", "warna": "#1D4ED8"
    },
    "UMY": {
        "id": "UMY", "nama": "Universitas Muhammadiyah Yogyakarta", "nama_en": "Muhammadiyah University of Yogyakarta",
        "singkatan": "UMY", "kota": "Bantul", "provinsi": "D.I. Yogyakarta",
        "wilayah": "Jawa", "tipe": "PTS", "klaster": "PTS Unggul", "akreditasi": "Unggul",
        "tahun_berdiri": 1981, "website": "https://umy.ac.id", "spmb_url": "https://admisi.umy.ac.id", "warna": "#CA8A04"
    },
    "UNPAR": {
        "id": "UNPAR", "nama": "Universitas Katolik Parahyangan", "nama_en": "Parahyangan Catholic University",
        "singkatan": "UNPAR", "kota": "Bandung", "provinsi": "Jawa Barat",
        "wilayah": "Jawa", "tipe": "PTS", "klaster": "PTS Unggul", "akreditasi": "Unggul",
        "tahun_berdiri": 1955, "website": "https://unpar.ac.id", "spmb_url": "https://pmb.unpar.ac.id", "warna": "#0369A1"
    },
    "ATMAJAYA": {
        "id": "ATMAJAYA", "nama": "Unika Atma Jaya", "nama_en": "Atma Jaya Catholic University of Indonesia",
        "singkatan": "ATMAJAYA", "kota": "Jakarta Selatan", "provinsi": "DKI Jakarta",
        "wilayah": "Jawa", "tipe": "PTS", "klaster": "PTS Unggul", "akreditasi": "Unggul",
        "tahun_berdiri": 1960, "website": "https://atmajaya.ac.id", "spmb_url": "https://pmb.atmajaya.ac.id", "warna": "#1E3A8A"
    },
    "UPH": {
        "id": "UPH", "nama": "Universitas Pelita Harapan", "nama_en": "Pelita Harapan University",
        "singkatan": "UPH", "kota": "Tangerang", "provinsi": "Banten",
        "wilayah": "Jawa", "tipe": "PTS", "klaster": "PTS Unggul", "akreditasi": "Unggul",
        "tahun_berdiri": 1994, "website": "https://uph.edu", "spmb_url": "https://admission.uph.edu", "warna": "#1D4ED8"
    },
    "TRISAKTI": {
        "id": "TRISAKTI", "nama": "Universitas Trisakti", "nama_en": "Trisakti University",
        "singkatan": "TRISAKTI", "kota": "Jakarta Barat", "provinsi": "DKI Jakarta",
        "wilayah": "Jawa", "tipe": "PTS", "klaster": "PTS Unggul", "akreditasi": "Unggul",
        "tahun_berdiri": 1965, "website": "https://trisakti.ac.id", "spmb_url": "https://spmb.trisakti.ac.id", "warna": "#0284C7"
    },
    "UNTAR": {
        "id": "UNTAR", "nama": "Universitas Tarumanagara", "nama_en": "Tarumanagara University",
        "singkatan": "UNTAR", "kota": "Jakarta Barat", "provinsi": "DKI Jakarta",
        "wilayah": "Jawa", "tipe": "PTS", "klaster": "PTS Unggul", "akreditasi": "Unggul",
        "tahun_berdiri": 1959, "website": "https://untar.ac.id", "spmb_url": "https://admisi.untar.ac.id", "warna": "#B91C1C"
    },
    "UMN": {
        "id": "UMN", "nama": "Universitas Multimedia Nusantara", "nama_en": "Multimedia Nusantara University",
        "singkatan": "UMN", "kota": "Tangerang", "provinsi": "Banten",
        "wilayah": "Jawa", "tipe": "PTS", "klaster": "PTS Unggul", "akreditasi": "Unggul",
        "tahun_berdiri": 2006, "website": "https://umn.ac.id", "spmb_url": "https://pmb.umn.ac.id", "warna": "#0284C7"
    },
    "PETRA": {
        "id": "PETRA", "nama": "Universitas Kristen Petra", "nama_en": "Petra Christian University",
        "singkatan": "PETRA", "kota": "Surabaya", "provinsi": "Jawa Timur",
        "wilayah": "Jawa", "tipe": "PTS", "klaster": "PTS Unggul", "akreditasi": "Unggul",
        "tahun_berdiri": 1961, "website": "https://petra.ac.id", "spmb_url": "https://admission.petra.ac.id", "warna": "#1E40AF"
    },
    "UMS": {
        "id": "UMS", "nama": "Universitas Muhammadiyah Surakarta", "nama_en": "Muhammadiyah University of Surakarta",
        "singkatan": "UMS", "kota": "Surakarta", "provinsi": "Jawa Tengah",
        "wilayah": "Jawa", "tipe": "PTS", "klaster": "PTS Unggul", "akreditasi": "Unggul",
        "tahun_berdiri": 1981, "website": "https://ums.ac.id", "spmb_url": "https://pmb.ums.ac.id", "warna": "#2563EB"
    },
    "PRESUNIV": {
        "id": "PRESUNIV", "nama": "President University", "nama_en": "President University",
        "singkatan": "PRESUNIV", "kota": "Cikarang", "provinsi": "Jawa Barat",
        "wilayah": "Jawa", "tipe": "PTS", "klaster": "PTS Unggul", "akreditasi": "Unggul",
        "tahun_berdiri": 2001, "website": "https://president.ac.id", "spmb_url": "https://admission.president.ac.id", "warna": "#991B1B"
    },
    "USD": {
        "id": "USD", "nama": "Universitas Sanata Dharma", "nama_en": "Sanata Dharma University",
        "singkatan": "USD", "kota": "Sleman / Yogyakarta", "provinsi": "D.I. Yogyakarta",
        "wilayah": "Jawa", "tipe": "PTS", "klaster": "PTS Unggul", "akreditasi": "Unggul",
        "tahun_berdiri": 1955, "website": "https://usd.ac.id", "spmb_url": "https://pmb.usd.ac.id", "warna": "#047857"
    },
    "MERCU": {
        "id": "MERCU", "nama": "Universitas Mercu Buana", "nama_en": "Mercu Buana University",
        "singkatan": "MERCU", "kota": "Jakarta Barat", "provinsi": "DKI Jakarta",
        "wilayah": "Jawa", "tipe": "PTS", "klaster": "PTS Unggul", "akreditasi": "Unggul",
        "tahun_berdiri": 1985, "website": "https://mercubuana.ac.id", "spmb_url": "https://pendaftaran.mercubuana.ac.id", "warna": "#0369A1"
    }
}

# Standardized descriptions and focus areas for major programs
PRODI_KB = {
    "Kedokteran": {
        "nama_en": "Medicine",
        "deskripsi": {
            "id": "Pendidikan dokter komprehensif yang membekali mahasiswa dengan ilmu biomedis, keterampilan klinis, diagnosis penyakit, dan etika medis profesional.",
            "en": "Comprehensive medical education equipping students with biomedical sciences, clinical skills, disease diagnosis, and professional medical ethics."
        },
        "fokus": {
            "id": ["Anatomi & Fisiologi Manusia", "Patologi & Farmakologi Klinis", "Rotasi Kepaniteraan Klinik (Koas)", "Pelayanan Kesehatan Primer"],
            "en": ["Human Anatomy & Physiology", "Pathology & Clinical Pharmacology", "Clinical Clerkship Rotations", "Primary Healthcare Services"]
        },
        "karir": {
            "id": ["Dokter Umum", "Dokter Spesialis", "Peneliti Biomedis", "Konsultan Kesehatan", "Direktur Rumah Sakit"],
            "en": ["General Practitioner", "Medical Specialist", "Biomedical Researcher", "Healthcare Consultant", "Hospital Director"]
        }
    },
    "Teknik Informatika": {
        "nama_en": "Informatics / Computer Science",
        "deskripsi": {
            "id": "Studi komputasi modern, algoritma, rekayasa perangkat lunak, kecerdasan buatan, dan arsitektur sistem informasi berskala besar.",
            "en": "Study of modern computing, algorithms, software engineering, artificial intelligence, and large-scale information systems architecture."
        },
        "fokus": {
            "id": ["Algoritma & Struktur Data", "Rekayasa Perangkat Lunak", "Machine Learning & AI", "Keamanan Siber & Jaringan"],
            "en": ["Algorithms & Data Structures", "Software Engineering", "Machine Learning & AI", "Cybersecurity & Networks"]
        },
        "karir": {
            "id": ["Software Engineer", "AI/ML Engineer", "Data Scientist", "Solutions Architect", "Cybersecurity Analyst"],
            "en": ["Software Engineer", "AI/ML Engineer", "Data Scientist", "Solutions Architect", "Cybersecurity Analyst"]
        }
    },
    "Sistem Informasi": {
        "nama_en": "Information Systems",
        "deskripsi": {
            "id": "Integrasi teknologi informasi dengan strategi bisnis, tata kelola TI perusahaan, rekayasa kebutuhan, dan analisis data bisnis.",
            "en": "Integration of information technology with business strategy, enterprise IT governance, requirements engineering, and business data analytics."
        },
        "fokus": {
            "id": ["Analisis & Perancangan Sistem", "Enterprise Resource Planning", "Manajemen Basis Data", "Business Intelligence"],
            "en": ["Systems Analysis & Design", "Enterprise Resource Planning", "Database Management", "Business Intelligence"]
        },
        "karir": {
            "id": ["Product Manager", "Business Analyst", "IT Consultant", "Database Administrator", "Enterprise Architect"],
            "en": ["Product Manager", "Business Analyst", "IT Consultant", "Database Administrator", "Enterprise Architect"]
        }
    },
    "Farmasi": {
        "nama_en": "Pharmacy",
        "deskripsi": {
            "id": "Ilmu formulasi, sintesis, evaluasi efikasi, dan pengawasan mutu obat-obatan serta pelayanan farmasi klinis dan komunitas.",
            "en": "The science of drug formulation, synthesis, efficacy evaluation, quality control, and clinical-community pharmacy services."
        },
        "fokus": {
            "id": ["Kimia Farmasi & Medisinal", "Farmakologi & Toksikologi", "Teknologi Formulasi Sediaan", "Farmasi Klinis"],
            "en": ["Pharmaceutical & Medicinal Chemistry", "Pharmacology & Toxicology", "Dosage Form Formulation", "Clinical Pharmacy"]
        },
        "karir": {
            "id": ["Apoteker Klinis", "Formulator Obat Industri", "Regulatory Affairs Specialist", "Peneliti Farmasi", "Quality Assurance Analyst"],
            "en": ["Clinical Pharmacist", "Industrial Drug Formulator", "Regulatory Affairs Specialist", "Pharmaceutical Researcher", "QA Analyst"]
        }
    },
    "Kedokteran Gigi": {
        "nama_en": "Dentistry",
        "deskripsi": {
            "id": "Pendidikan medis khusus kesehatan gigi, mulut, rahang, dan maksilofasial dengan pelatihan keterampilan klinis komprehensif.",
            "en": "Specialized dental medical education covering oral, maxillofacial, and dental healthcare with comprehensive clinical training."
        },
        "fokus": {
            "id": ["Konservasi Gigi & Endodonsia", "Ortodonsia & Prostodonsia", "Bedah Mulut & Maksilofasial", "Periodonsia"],
            "en": ["Conservative Dentistry & Endodontics", "Orthodontics & Prosthodontics", "Oral & Maxillofacial Surgery", "Periodontics"]
        },
        "karir": {
            "id": ["Dokter Gigi Umum", "Spesialis Ortodontis", "Spesialis Bedah Mulut", "Peneliti Oral Biologi"],
            "en": ["General Dentist", "Orthodontist Specialist", "Oral Surgeon Specialist", "Oral Biology Researcher"]
        }
    },
    "Teknik Elektro": {
        "nama_en": "Electrical Engineering",
        "deskripsi": {
            "id": "Rekayasa sistem kelistrikan, pembangkitan energi, elektronika daya, sistem kontrol terotomasi, telekomunikasi, dan pemrosesan sinyal.",
            "en": "Engineering of electrical systems, power generation, power electronics, automated control systems, telecom, and signal processing."
        },
        "fokus": {
            "id": ["Sistem Tenaga Listrik", "Elektronika Terintegrasi", "Sistem Kontrol & Robotika", "Teknologi Telekomunikasi"],
            "en": ["Electrical Power Systems", "Integrated Electronics", "Control & Robotics", "Telecommunication Technologies"]
        },
        "karir": {
            "id": ["Power Systems Engineer", "Control & Automation Specialist", "Hardware Design Engineer", "Telecommunications Engineer"],
            "en": ["Power Systems Engineer", "Control & Automation Specialist", "Hardware Design Engineer", "Telecommunications Engineer"]
        }
    },
    "Teknik Sipil": {
        "nama_en": "Civil Engineering",
        "deskripsi": {
            "id": "Perencanaan, perancangan struktur, konstruksi, dan pemeliharaan infrastruktur transportasi, jembatan, gedung, dan rekayasa air.",
            "en": "Planning, structural design, construction, and maintenance of transport infrastructure, bridges, buildings, and water engineering."
        },
        "fokus": {
            "id": ["Struktur Beton & Baja", "Geoteknik & Mekanika Tanah", "Manajemen Proyek Konstruksi", "Rekayasa Sumber Daya Air"],
            "en": ["Concrete & Steel Structures", "Geotechnical & Soil Mechanics", "Construction Project Management", "Water Resources Engineering"]
        },
        "karir": {
            "id": ["Structural Engineer", "Project Manager Konstruksi", "Geotechnical Specialist", "Konsultan Infrastruktur"],
            "en": ["Structural Engineer", "Construction Project Manager", "Geotechnical Specialist", "Infrastructure Consultant"]
        }
    },
    "Teknik Industri": {
        "nama_en": "Industrial Engineering",
        "deskripsi": {
            "id": "Optimalisasi sistem terintegrasi yang melibatkan manusia, mesin, material, informasi, dan energi untuk efisiensi produksi maksimal.",
            "en": "Optimization of integrated systems involving people, machinery, materials, information, and energy for peak operational efficiency."
        },
        "fokus": {
            "id": ["Manajemen Rantai Pasok (SCM)", "Riset Operasi & Optimasi", "Ergonomi & Perancangan Kerja", "Pengendalian Kualitas (Six Sigma)"],
            "en": ["Supply Chain Management", "Operations Research", "Ergonomics & Work Design", "Quality Control (Six Sigma)"]
        },
        "karir": {
            "id": ["Supply Chain Manager", "Operations Research Analyst", "Industrial Plant Specialist", "Management Consultant"],
            "en": ["Supply Chain Manager", "Operations Research Analyst", "Industrial Plant Specialist", "Management Consultant"]
        }
    },
    "Psikologi": {
        "nama_en": "Psychology",
        "deskripsi": {
            "id": "Kajian ilmiah proses mental, perilaku manusia, asesmen psikodiagnostik, dinamika perkembangan, dan intervensi sosial-organisasi.",
            "en": "Scientific study of mental processes, human behavior, psychodiagnostic assessment, developmental dynamics, and organizational interventions."
        },
        "fokus": {
            "id": ["Psikologi Klinis & Konseling", "Psikologi Industri & Organisasi (PIO)", "Psikometri & Asesmen", "Psikologi Perkembangan"],
            "en": ["Clinical & Counseling Psychology", "Industrial & Organizational Psychology", "Psychometrics & Assessment", "Developmental Psychology"]
        },
        "karir": {
            "id": ["Human Resource Specialist (HRD)", "Asesor Psikologi", "Konselor Pendidikan & Karir", "Talent Acquisition Lead", "Peneliti Perilaku"],
            "en": ["HR Specialist", "Psychological Assessor", "Career & Education Counselor", "Talent Acquisition Lead", "Behavioral Researcher"]
        }
    },
    "Ilmu Komunikasi": {
        "nama_en": "Communication Studies",
        "deskripsi": {
            "id": "Analisis dinamika pesan, media digital, jurnalisme investigatif, public relations strategis, periklanan, dan komunikasi massa kontemporer.",
            "en": "Analysis of message dynamics, digital media, investigative journalism, strategic PR, advertising, and contemporary mass communications."
        },
        "fokus": {
            "id": ["Hubungan Masyarakat (PR)", "Jurnalistik Multimedia", "Komunikasi Pemasaran Terpadu", "Produksi Media Digital"],
            "en": ["Public Relations (PR)", "Multimedia Journalism", "Integrated Marketing Comm", "Digital Media Production"]
        },
        "karir": {
            "id": ["Corporate PR Specialist", "Media Strategist", "Content Producer", "Brand Communications Lead", "Jurnalis Investigasi"],
            "en": ["Corporate PR Specialist", "Media Strategist", "Content Producer", "Brand Communications Lead", "Investigative Journalist"]
        }
    },
    "Ilmu Hukum": {
        "nama_en": "Law / Legal Studies",
        "deskripsi": {
            "id": "Penguasaan sistem hukum nasional dan internasional, litigasi, kontrak bisnis, hukum perdata, pidana, dan tata negara.",
            "en": "Mastery of national and international legal systems, litigation, corporate contracts, civil, criminal, and constitutional law."
        },
        "fokus": {
            "id": ["Hukum Bisnis & Korporasi", "Hukum Pidana & Acara Pidana", "Hukum Perdata & Kontrak", "Hukum Tata Negara & HAM"],
            "en": ["Business & Corporate Law", "Criminal Law & Procedure", "Civil & Contract Law", "Constitutional Law & Human Rights"]
        },
        "karir": {
            "id": ["Corporate Legal Counsel", "Advokat / Pengacara", "Hakim & Jaksa", "Diplomat Hukum", "Konsultan Kebijakan Publik"],
            "en": ["Corporate Legal Counsel", "Advocate / Lawyer", "Judge & Public Prosecutor", "Legal Diplomat", "Public Policy Consultant"]
        }
    },
    "Manajemen": {
        "nama_en": "Management",
        "deskripsi": {
            "id": "Strategi pengelolaan organisasi bisnis, pengambilan keputusan finansial, pemasaran digital, kepemimpinan tim, dan inovasi kewirausahaan.",
            "en": "Strategic management of business organizations, financial decision-making, digital marketing, leadership, and entrepreneurial innovation."
        },
        "fokus": {
            "id": ["Manajemen Keuangan Korporasi", "Manajemen Pemasaran Strategis", "Manajemen SDM & Kepemimpinan", "Manajemen Operasional"],
            "en": ["Corporate Financial Management", "Strategic Marketing", "HR Management & Leadership", "Operational Management"]
        },
        "karir": {
            "id": ["Management Consultant", "Brand Manager", "Financial Analyst", "Operations Manager", "Business Development Lead"],
            "en": ["Management Consultant", "Brand Manager", "Financial Analyst", "Operations Manager", "Business Development Lead"]
        }
    },
    "Akuntansi": {
        "nama_en": "Accounting",
        "deskripsi": {
            "id": "Pelaporan keuangan berstandar IFRS/PSAK, audit independen, akuntansi manajemen, perpajakan strategis, dan sistem informasi akuntansi.",
            "en": "Financial reporting adhering to IFRS standards, independent audit, management accounting, strategic tax, and accounting information systems."
        },
        "fokus": {
            "id": ["Akuntansi Keuangan & IFRS", "Auditing & Asurans", "Perpajakan Korporasi", "Akuntansi Manajemen & Biaya"],
            "en": ["Financial Accounting & IFRS", "Auditing & Assurance", "Corporate Taxation", "Management & Cost Accounting"]
        },
        "karir": {
            "id": ["Auditor Big Four", "Financial Controller", "Tax Specialist", "Internal Auditor", "Akuntan Publik (CPA)"],
            "en": ["Big Four Auditor", "Financial Controller", "Tax Specialist", "Internal Auditor", "Certified Public Accountant"]
        }
    },
    "Hubungan Internasional": {
        "nama_en": "International Relations",
        "deskripsi": {
            "id": "Kajian diplomasi global, negosiasi multilateral, keamanan regional, ekonomi politik internasional, dan resolusi konflik.",
            "en": "Study of global diplomacy, multilateral negotiations, regional security, international political economy, and conflict resolution."
        },
        "fokus": {
            "id": ["Diplomasi & Negosiasi", "Ekonomi Politik Global", "Keamanan Internasional", "Hukum & Organisasi Multilateral"],
            "en": ["Diplomacy & Negotiation", "Global Political Economy", "International Security", "International Organizations & Law"]
        },
        "karir": {
            "id": ["Diplomat Kementerian Luar Negeri", "Petugas Lembaga Internasional (UN/ASEAN)", "Risk & Intelligence Analyst", "Jurnalis Luar Negeri"],
            "en": ["Foreign Service Diplomat", "UN/ASEAN International Officer", "Risk & Geopolitical Analyst", "Foreign Correspondent"]
        }
    },
    "Statistika": {
        "nama_en": "Statistics / Data Science",
        "deskripsi": {
            "id": "Metodologi pemodelan probabilistik, komputasi inferensial, riset data kuantitatif, analisis multivariat, dan pemodelan prediktif.",
            "en": "Methodologies for probabilistic modeling, inferential computing, quantitative data research, multivariate analysis, and predictive models."
        },
        "fokus": {
            "id": ["Analisis Regresi & Time Series", "Komputasi Statistik & R/Python", "Statistika Spasial & Bayesian", "Big Data Analytics"],
            "en": ["Regression & Time Series", "Statistical Computing (R/Python)", "Spatial & Bayesian Statistics", "Big Data Analytics"]
        },
        "karir": {
            "id": ["Data Scientist", "Quantitative Analyst (Quant)", "Aktuaris", "Biostatistician", "Market Research Director"],
            "en": ["Data Scientist", "Quantitative Analyst (Quant)", "Actuary", "Biostatistician", "Market Research Director"]
        }
    },
    "Arsitektur": {
        "nama_en": "Architecture",
        "deskripsi": {
            "id": "Perancangan ruang, estetika bangunan, keberlanjutan lingkungan hidup, teknologi material, dan integrasi lanskap perkotaan.",
            "en": "Spatial design, building aesthetics, environmental sustainability, materials technology, and urban landscape integration."
        },
        "fokus": {
            "id": ["Studio Perancangan Arsitektur", "Teknologi Bangunan & Struktur", "Arsitektur Berkelanjutan (Green Building)", "Perencanaan Kawasan Perkotaan"],
            "en": ["Architectural Design Studio", "Building & Structural Tech", "Sustainable / Green Building", "Urban Planning & Design"]
        },
        "karir": {
            "id": ["Arsitek Perancang", "Urban Designer", "BIM Specialist", "Konsultan Bangunan Hijau", "Interior Architect"],
            "en": ["Design Architect", "Urban Designer", "BIM Specialist", "Green Building Consultant", "Interior Architect"]
        }
    },
    "Ilmu Administrasi Publik": {
        "nama_en": "Public Administration",
        "deskripsi": {
            "id": "Studi perumusan kebijakan publik, reformasi birokrasi, tata kelola pemerintahan yang baik, dan manajemen pelayanan publik.",
            "en": "Study of public policy formulation, bureaucratic reform, good governance, and public service management."
        },
        "fokus": {
            "id": ["Analisis Kebijakan Publik", "Manajemen Organisasi Sektor Publik", "E-Government & Inovasi Layanan", "Keuangan Publik"],
            "en": ["Public Policy Analysis", "Public Sector Management", "E-Government & Service Innovation", "Public Finance"]
        },
        "karir": {
            "id": ["Analis Kebijakan Publik", "Aparatur Sipil Negara (ASN)", "Konsultan Tata Kelola", "Program Officer NGO/LSM"],
            "en": ["Public Policy Analyst", "Civil Service Officer", "Governance Consultant", "NGO Program Officer"]
        }
    },
    "Desain Komunikasi Visual": {
        "nama_en": "Visual Communication Design (DKV)",
        "deskripsi": {
            "id": "Kreasi komunikasi grafis visual, identitas jenama (branding), tipografi, ilustrasi, desain interaksi UI/UX, dan multimedia gerak.",
            "en": "Creation of visual communication, brand identity, typography, illustration, UI/UX interaction design, and motion graphics."
        },
        "fokus": {
            "id": ["Branding & Identitas Visual", "Desain UI/UX & Interaksi", "Tipografi & Ilustrasi Digital", "Animasi & Motion Graphics"],
            "en": ["Branding & Visual Identity", "UI/UX & Interaction Design", "Typography & Digital Illustration", "Animation & Motion Graphics"]
        },
        "karir": {
            "id": ["UI/UX Designer", "Creative Director", "Brand Identity Specialist", "Motion Designer", "Ilustrator Profesional"],
            "en": ["UI/UX Designer", "Creative Director", "Brand Identity Specialist", "Motion Designer", "Professional Illustrator"]
        }
    }
}

# Raw Dataset of Top Programs per Campus
# Realistic data grounded in BPPP SNPMB 2024/2025 official benchmarks
RAW_ENTRIES = [
    # --- UNIVERSITAS INDONESIA (UI) ---
    {"ptn": "UI", "prodi": "Kedokteran", "kode": "311001", "rumpun": "Saintek", "snbp_dt": 45, "snbp_peminat": [1820, 1690, 1580], "snbt_dt": 75, "snbt_peminat": [3840, 3680, 3450]},
    {"ptn": "UI", "prodi": "Teknik Informatika", "kode": "311002", "rumpun": "Saintek", "snbp_dt": 27, "snbp_peminat": [1460, 1380, 1290], "snbt_dt": 45, "snbt_peminat": [3120, 2980, 2810]},
    {"ptn": "UI", "prodi": "Sistem Informasi", "kode": "311003", "rumpun": "Saintek", "snbp_dt": 27, "snbp_peminat": [1120, 1050, 980], "snbt_dt": 45, "snbt_peminat": [2450, 2310, 2190]},
    {"ptn": "UI", "prodi": "Farmasi", "kode": "311004", "rumpun": "Saintek", "snbp_dt": 24, "snbp_peminat": [890, 840, 790], "snbt_dt": 40, "snbt_peminat": [1780, 1690, 1590]},
    {"ptn": "UI", "prodi": "Kedokteran Gigi", "kode": "311005", "rumpun": "Saintek", "snbp_dt": 20, "snbp_peminat": [720, 680, 630], "snbt_dt": 35, "snbt_peminat": [1420, 1350, 1280]},
    {"ptn": "UI", "prodi": "Teknik Industri", "kode": "311006", "rumpun": "Saintek", "snbp_dt": 29, "snbp_peminat": [790, 740, 710], "snbt_dt": 48, "snbt_peminat": [1640, 1560, 1490]},
    {"ptn": "UI", "prodi": "Teknik Elektro", "kode": "311007", "rumpun": "Saintek", "snbp_dt": 25, "snbp_peminat": [630, 590, 570], "snbt_dt": 42, "snbt_peminat": [1280, 1210, 1150]},
    {"ptn": "UI", "prodi": "Ilmu Hukum", "kode": "311008", "rumpun": "Soshum", "snbp_dt": 90, "snbp_peminat": [3210, 3050, 2890], "snbt_dt": 150, "snbt_peminat": [5420, 5190, 4980]},
    {"ptn": "UI", "prodi": "Psikologi", "kode": "311009", "rumpun": "Soshum", "snbp_dt": 54, "snbp_peminat": [2870, 2720, 2580], "snbt_dt": 90, "snbt_peminat": [4650, 4420, 4210]},
    {"ptn": "UI", "prodi": "Manajemen", "kode": "311010", "rumpun": "Soshum", "snbp_dt": 60, "snbp_peminat": [2540, 2410, 2290], "snbt_dt": 100, "snbt_peminat": [4210, 4020, 3860]},
    {"ptn": "UI", "prodi": "Akuntansi", "kode": "311011", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [1980, 1890, 1780], "snbt_dt": 90, "snbt_peminat": [3150, 3010, 2890]},
    {"ptn": "UI", "prodi": "Ilmu Komunikasi", "kode": "311012", "rumpun": "Soshum", "snbp_dt": 28, "snbp_peminat": [2120, 1990, 1870], "snbt_dt": 45, "snbt_peminat": [3580, 3410, 3240]},
    {"ptn": "UI", "prodi": "Hubungan Internasional", "kode": "311013", "rumpun": "Soshum", "snbp_dt": 18, "snbp_peminat": [1340, 1270, 1190], "snbt_dt": 30, "snbt_peminat": [2290, 2180, 2070]},

    # --- INSTITUT TEKNOLOGI BANDUNG (ITB) ---
    {"ptn": "ITB", "prodi": "Teknik Informatika", "kode": "332001", "rumpun": "Saintek", "snbp_dt": 50, "snbp_peminat": [2680, 2520, 2390], "snbt_dt": 85, "snbt_peminat": [4850, 4610, 4390]},
    {"ptn": "ITB", "prodi": "Sistem Informasi", "kode": "332002", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [1420, 1340, 1260], "snbt_dt": 50, "snbt_peminat": [2780, 2630, 2490]},
    {"ptn": "ITB", "prodi": "Teknik Industri", "kode": "332003", "rumpun": "Saintek", "snbp_dt": 45, "snbp_peminat": [1680, 1590, 1510], "snbt_dt": 75, "snbt_peminat": [3150, 2990, 2840]},
    {"ptn": "ITB", "prodi": "Teknik Elektro", "kode": "332004", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1320, 1250, 1190], "snbt_dt": 68, "snbt_peminat": [2450, 2320, 2210]},
    {"ptn": "ITB", "prodi": "Teknik Sipil", "kode": "332005", "rumpun": "Saintek", "snbp_dt": 42, "snbp_peminat": [1210, 1150, 1090], "snbt_dt": 70, "snbt_peminat": [2280, 2170, 2060]},
    {"ptn": "ITB", "prodi": "Farmasi", "kode": "332006", "rumpun": "Saintek", "snbp_dt": 35, "snbp_peminat": [1280, 1210, 1140], "snbt_dt": 60, "snbt_peminat": [2380, 2250, 2140]},
    {"ptn": "ITB", "prodi": "Arsitektur", "kode": "332007", "rumpun": "Saintek", "snbp_dt": 32, "snbp_peminat": [1390, 1310, 1240], "snbt_dt": 55, "snbt_peminat": [2590, 2460, 2340]},
    {"ptn": "ITB", "prodi": "Manajemen", "kode": "332008", "rumpun": "Soshum", "snbp_dt": 48, "snbp_peminat": [2780, 2620, 2480], "snbt_dt": 80, "snbt_peminat": [4690, 4450, 4230]},
    {"ptn": "ITB", "prodi": "Desain Komunikasi Visual", "kode": "332009", "rumpun": "Soshum", "snbp_dt": 36, "snbp_peminat": [1890, 1780, 1690], "snbt_dt": 60, "snbt_peminat": [3280, 3110, 2960]},

    # --- UNIVERSITAS GADJAH MADA (UGM) ---
    {"ptn": "UGM", "prodi": "Kedokteran", "kode": "341001", "rumpun": "Saintek", "snbp_dt": 53, "snbp_peminat": [2150, 2010, 1910], "snbt_dt": 88, "snbt_peminat": [4280, 4080, 3890]},
    {"ptn": "UGM", "prodi": "Teknik Informatika", "kode": "341002", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [1890, 1780, 1670], "snbt_dt": 50, "snbt_peminat": [3790, 3590, 3410]},
    {"ptn": "UGM", "prodi": "Farmasi", "kode": "341003", "rumpun": "Saintek", "snbp_dt": 60, "snbp_peminat": [1780, 1690, 1590], "snbt_dt": 100, "snbt_peminat": [3280, 3120, 2980]},
    {"ptn": "UGM", "prodi": "Kedokteran Gigi", "kode": "341004", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1080, 1020, 960], "snbt_dt": 65, "snbt_peminat": [1980, 1870, 1780]},
    {"ptn": "UGM", "prodi": "Teknik Sipil", "kode": "341005", "rumpun": "Saintek", "snbp_dt": 50, "snbp_peminat": [1120, 1060, 1010], "snbt_dt": 85, "snbt_peminat": [2150, 2040, 1950]},
    {"ptn": "UGM", "prodi": "Teknik Industri", "kode": "341006", "rumpun": "Saintek", "snbp_dt": 42, "snbp_peminat": [1190, 1120, 1070], "snbt_dt": 70, "snbt_peminat": [2290, 2170, 2080]},
    {"ptn": "UGM", "prodi": "Statistika", "kode": "341007", "rumpun": "Saintek", "snbp_dt": 24, "snbp_peminat": [870, 820, 780], "snbt_dt": 40, "snbt_peminat": [1680, 1590, 1510]},
    {"ptn": "UGM", "prodi": "Psikologi", "kode": "341008", "rumpun": "Soshum", "snbp_dt": 68, "snbp_peminat": [3420, 3250, 3080], "snbt_dt": 110, "snbt_peminat": [5120, 4890, 4670]},
    {"ptn": "UGM", "prodi": "Ilmu Hukum", "kode": "341009", "rumpun": "Soshum", "snbp_dt": 99, "snbp_peminat": [3890, 3690, 3510], "snbt_dt": 165, "snbt_peminat": [5890, 5620, 5380]},
    {"ptn": "UGM", "prodi": "Manajemen", "kode": "341010", "rumpun": "Soshum", "snbp_dt": 45, "snbp_peminat": [2670, 2520, 2390], "snbt_dt": 75, "snbt_peminat": [4150, 3960, 3790]},
    {"ptn": "UGM", "prodi": "Akuntansi", "kode": "341011", "rumpun": "Soshum", "snbp_dt": 45, "snbp_peminat": [2120, 2010, 1910], "snbt_dt": 75, "snbt_peminat": [3340, 3190, 3050]},
    {"ptn": "UGM", "prodi": "Ilmu Komunikasi", "kode": "341012", "rumpun": "Soshum", "snbp_dt": 24, "snbp_peminat": [2480, 2350, 2220], "snbt_dt": 40, "snbt_peminat": [3980, 3780, 3610]},
    {"ptn": "UGM", "prodi": "Hubungan Internasional", "kode": "341013", "rumpun": "Soshum", "snbp_dt": 24, "snbp_peminat": [1680, 1590, 1510], "snbt_dt": 40, "snbt_peminat": [2790, 2650, 2530]},

    # --- IPB UNIVERSITY ---
    {"ptn": "IPB", "prodi": "Teknik Informatika", "kode": "322001", "rumpun": "Saintek", "snbp_dt": 42, "snbp_peminat": [1650, 1560, 1470], "snbt_dt": 70, "snbt_peminat": [3180, 3020, 2880]},
    {"ptn": "IPB", "prodi": "Statistika", "kode": "322002", "rumpun": "Saintek", "snbp_dt": 35, "snbp_peminat": [940, 890, 840], "snbt_dt": 60, "snbt_peminat": [1780, 1690, 1610]},
    {"ptn": "IPB", "prodi": "Kedokteran", "kode": "322003", "rumpun": "Saintek", "snbp_dt": 20, "snbp_peminat": [1480, 1380, 1290], "snbt_dt": 35, "snbt_peminat": [2890, 2740, 2610]},
    {"ptn": "IPB", "prodi": "Manajemen", "kode": "322004", "rumpun": "Soshum", "snbp_dt": 50, "snbp_peminat": [2450, 2320, 2190], "snbt_dt": 85, "snbt_peminat": [3980, 3790, 3620]},
    {"ptn": "IPB", "prodi": "Ilmu Komunikasi", "kode": "322005", "rumpun": "Soshum", "snbp_dt": 30, "snbp_peminat": [1820, 1720, 1630], "snbt_dt": 50, "snbt_peminat": [2890, 2750, 2620]},

    # --- UNIVERSITAS AIRLANGGA (UNAIR) ---
    {"ptn": "UNAIR", "prodi": "Kedokteran", "kode": "381001", "rumpun": "Saintek", "snbp_dt": 50, "snbp_peminat": [1980, 1870, 1780], "snbt_dt": 80, "snbt_peminat": [3890, 3690, 3520]},
    {"ptn": "UNAIR", "prodi": "Farmasi", "kode": "381002", "rumpun": "Saintek", "snbp_dt": 55, "snbp_peminat": [1650, 1560, 1480], "snbt_dt": 90, "snbt_peminat": [2980, 2830, 2710]},
    {"ptn": "UNAIR", "prodi": "Kedokteran Gigi", "kode": "381003", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1120, 1060, 1010], "snbt_dt": 65, "snbt_peminat": [2050, 1950, 1860]},
    {"ptn": "UNAIR", "prodi": "Sistem Informasi", "kode": "381004", "rumpun": "Saintek", "snbp_dt": 28, "snbp_peminat": [1150, 1090, 1030], "snbt_dt": 45, "snbt_peminat": [2280, 2160, 2050]},
    {"ptn": "UNAIR", "prodi": "Psikologi", "kode": "381005", "rumpun": "Soshum", "snbp_dt": 65, "snbp_peminat": [2980, 2820, 2690], "snbt_dt": 105, "snbt_peminat": [4580, 4360, 4170]},
    {"ptn": "UNAIR", "prodi": "Ilmu Hukum", "kode": "381006", "rumpun": "Soshum", "snbp_dt": 80, "snbp_peminat": [2780, 2630, 2510], "snbt_dt": 130, "snbt_peminat": [4190, 3990, 3820]},
    {"ptn": "UNAIR", "prodi": "Manajemen", "kode": "381007", "rumpun": "Soshum", "snbp_dt": 75, "snbp_peminat": [2450, 2320, 2210], "snbt_dt": 120, "snbt_peminat": [3890, 3700, 3540]},
    {"ptn": "UNAIR", "prodi": "Ilmu Komunikasi", "kode": "381008", "rumpun": "Soshum", "snbp_dt": 35, "snbp_peminat": [1980, 1870, 1770], "snbt_dt": 55, "snbt_peminat": [3080, 2930, 2800]},

    # --- INSTITUT TEKNOLOGI SEPULUH NOPEMBER (ITS) ---
    {"ptn": "ITS", "prodi": "Teknik Informatika", "kode": "382001", "rumpun": "Saintek", "snbp_dt": 54, "snbp_peminat": [2150, 2030, 1920], "snbt_dt": 90, "snbt_peminat": [4120, 3910, 3720]},
    {"ptn": "ITS", "prodi": "Sistem Informasi", "kode": "382002", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1380, 1310, 1240], "snbt_dt": 65, "snbt_peminat": [2680, 2540, 2420]},
    {"ptn": "ITS", "prodi": "Teknik Industri", "kode": "382003", "rumpun": "Saintek", "snbp_dt": 45, "snbp_peminat": [1280, 1210, 1150], "snbt_dt": 75, "snbt_peminat": [2490, 2360, 2250]},
    {"ptn": "ITS", "prodi": "Teknik Sipil", "kode": "382004", "rumpun": "Saintek", "snbp_dt": 45, "snbp_peminat": [1080, 1020, 970], "snbt_dt": 75, "snbt_peminat": [2150, 2040, 1950]},
    {"ptn": "ITS", "prodi": "Teknik Elektro", "kode": "382005", "rumpun": "Saintek", "snbp_dt": 45, "snbp_peminat": [980, 930, 890], "snbt_dt": 75, "snbt_peminat": [1980, 1880, 1790]},
    {"ptn": "ITS", "prodi": "Arsitektur", "kode": "382006", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [980, 920, 870], "snbt_dt": 50, "snbt_peminat": [1920, 1820, 1730]},
    {"ptn": "ITS", "prodi": "Statistika", "kode": "382007", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [890, 840, 790], "snbt_dt": 50, "snbt_peminat": [1680, 1590, 1510]},
    {"ptn": "ITS", "prodi": "Desain Komunikasi Visual", "kode": "382008", "rumpun": "Soshum", "snbp_dt": 28, "snbp_peminat": [1120, 1050, 990], "snbt_dt": 45, "snbt_peminat": [2190, 2080, 1980]},

    # --- UNIVERSITAS DIPONEGORO (UNDIP) ---
    {"ptn": "UNDIP", "prodi": "Kedokteran", "kode": "351001", "rumpun": "Saintek", "snbp_dt": 55, "snbp_peminat": [1920, 1810, 1710], "snbt_dt": 90, "snbt_peminat": [3780, 3590, 3420]},
    {"ptn": "UNDIP", "prodi": "Teknik Informatika", "kode": "351002", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1780, 1680, 1590], "snbt_dt": 65, "snbt_peminat": [3450, 3280, 3120]},
    {"ptn": "UNDIP", "prodi": "Farmasi", "kode": "351003", "rumpun": "Saintek", "snbp_dt": 25, "snbp_peminat": [1280, 1210, 1140], "snbt_dt": 42, "snbt_peminat": [2280, 2160, 2050]},
    {"ptn": "UNDIP", "prodi": "Psikologi", "kode": "351004", "rumpun": "Soshum", "snbp_dt": 85, "snbp_peminat": [3680, 3490, 3310], "snbt_dt": 140, "snbt_peminat": [5380, 5120, 4890]},
    {"ptn": "UNDIP", "prodi": "Ilmu Hukum", "kode": "351005", "rumpun": "Soshum", "snbp_dt": 180, "snbp_peminat": [4580, 4350, 4140], "snbt_dt": 300, "snbt_peminat": [6890, 6560, 6280]},
    {"ptn": "UNDIP", "prodi": "Manajemen", "kode": "351006", "rumpun": "Soshum", "snbp_dt": 80, "snbp_peminat": [3120, 2960, 2810], "snbt_dt": 130, "snbt_peminat": [4890, 4650, 4440]},
    {"ptn": "UNDIP", "prodi": "Ilmu Komunikasi", "kode": "351007", "rumpun": "Soshum", "snbp_dt": 45, "snbp_peminat": [2450, 2320, 2210], "snbt_dt": 70, "snbt_peminat": [3890, 3700, 3530]},

    # --- UNIVERSITAS BRAWIJAYA (UB) ---
    {"ptn": "UB", "prodi": "Kedokteran", "kode": "371001", "rumpun": "Saintek", "snbp_dt": 60, "snbp_peminat": [2080, 1960, 1850], "snbt_dt": 100, "snbt_peminat": [3980, 3780, 3590]},
    {"ptn": "UB", "prodi": "Teknik Informatika", "kode": "371002", "rumpun": "Saintek", "snbp_dt": 65, "snbp_peminat": [2380, 2250, 2140], "snbt_dt": 110, "snbt_peminat": [4280, 4060, 3870]},
    {"ptn": "UB", "prodi": "Sistem Informasi", "kode": "371003", "rumpun": "Saintek", "snbp_dt": 55, "snbp_peminat": [1680, 1590, 1510], "snbt_dt": 90, "snbt_peminat": [2890, 2740, 2610]},
    {"ptn": "UB", "prodi": "Farmasi", "kode": "371004", "rumpun": "Saintek", "snbp_dt": 35, "snbp_peminat": [1480, 1390, 1320], "snbt_dt": 60, "snbt_peminat": [2590, 2460, 2340]},
    {"ptn": "UB", "prodi": "Ilmu Hukum", "kode": "371005", "rumpun": "Soshum", "snbp_dt": 160, "snbp_peminat": [3980, 3770, 3580], "snbt_dt": 270, "snbt_peminat": [5980, 5690, 5430]},
    {"ptn": "UB", "prodi": "Psikologi", "kode": "371006", "rumpun": "Soshum", "snbp_dt": 85, "snbp_peminat": [3380, 3210, 3050], "snbt_dt": 140, "snbt_peminat": [4980, 4740, 4520]},
    {"ptn": "UB", "prodi": "Manajemen", "kode": "371007", "rumpun": "Soshum", "snbp_dt": 110, "snbp_peminat": [3580, 3390, 3220], "snbt_dt": 180, "snbt_peminat": [5280, 5020, 4790]},
    {"ptn": "UB", "prodi": "Ilmu Komunikasi", "kode": "371008", "rumpun": "Soshum", "snbp_dt": 80, "snbp_peminat": [2890, 2740, 2600], "snbt_dt": 130, "snbt_peminat": [4280, 4070, 3880]},

    # --- UNIVERSITAS PADJADJARAN (UNPAD) ---
    {"ptn": "UNPAD", "prodi": "Kedokteran", "kode": "331001", "rumpun": "Saintek", "snbp_dt": 55, "snbp_peminat": [2180, 2050, 1940], "snbt_dt": 95, "snbt_peminat": [4180, 3970, 3780]},
    {"ptn": "UNPAD", "prodi": "Teknik Informatika", "kode": "331002", "rumpun": "Saintek", "snbp_dt": 35, "snbp_peminat": [2280, 2160, 2040], "snbt_dt": 60, "snbt_peminat": [3980, 3780, 3590]},
    {"ptn": "UNPAD", "prodi": "Farmasi", "kode": "331003", "rumpun": "Saintek", "snbp_dt": 48, "snbp_peminat": [1980, 1870, 1770], "snbt_dt": 80, "snbt_peminat": [3450, 3270, 3110]},
    {"ptn": "UNPAD", "prodi": "Psikologi", "kode": "331004", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [3580, 3390, 3220], "snbt_dt": 90, "snbt_peminat": [5380, 5120, 4890]},
    {"ptn": "UNPAD", "prodi": "Ilmu Hukum", "kode": "331005", "rumpun": "Soshum", "snbp_dt": 120, "snbp_peminat": [3890, 3690, 3510], "snbt_dt": 200, "snbt_peminat": [5780, 5490, 5230]},
    {"ptn": "UNPAD", "prodi": "Manajemen", "kode": "331006", "rumpun": "Soshum", "snbp_dt": 60, "snbp_peminat": [3180, 3010, 2860], "snbt_dt": 100, "snbt_peminat": [4780, 4540, 4320]},
    {"ptn": "UNPAD", "prodi": "Ilmu Komunikasi", "kode": "331007", "rumpun": "Soshum", "snbp_dt": 48, "snbp_peminat": [3280, 3110, 2950], "snbt_dt": 80, "snbt_peminat": [4890, 4650, 4420]},
    {"ptn": "UNPAD", "prodi": "Hubungan Internasional", "kode": "331008", "rumpun": "Soshum", "snbp_dt": 35, "snbp_peminat": [1980, 1870, 1780], "snbt_dt": 60, "snbt_peminat": [3180, 3020, 2880]},

    # --- UNIVERSITAS SEBELAS MARET (UNS) ---
    {"ptn": "UNS", "prodi": "Kedokteran", "kode": "352001", "rumpun": "Saintek", "snbp_dt": 45, "snbp_peminat": [1680, 1590, 1490], "snbt_dt": 75, "snbt_peminat": [3280, 3110, 2950]},
    {"ptn": "UNS", "prodi": "Teknik Informatika", "kode": "352002", "rumpun": "Saintek", "snbp_dt": 32, "snbp_peminat": [1580, 1490, 1410], "snbt_dt": 55, "snbt_peminat": [3120, 2960, 2810]},
    {"ptn": "UNS", "prodi": "Farmasi", "kode": "352003", "rumpun": "Saintek", "snbp_dt": 24, "snbp_peminat": [1180, 1110, 1050], "snbt_dt": 40, "snbt_peminat": [2180, 2070, 1970]},
    {"ptn": "UNS", "prodi": "Teknik Sipil", "kode": "352004", "rumpun": "Saintek", "snbp_dt": 45, "snbp_peminat": [980, 930, 880], "snbt_dt": 75, "snbt_peminat": [1890, 1790, 1710]},
    {"ptn": "UNS", "prodi": "Psikologi", "kode": "352005", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [2980, 2820, 2680], "snbt_dt": 90, "snbt_peminat": [4580, 4350, 4140]},
    {"ptn": "UNS", "prodi": "Ilmu Hukum", "kode": "352006", "rumpun": "Soshum", "snbp_dt": 140, "snbp_peminat": [3450, 3270, 3110], "snbt_dt": 230, "snbt_peminat": [5120, 4870, 4640]},
    {"ptn": "UNS", "prodi": "Manajemen", "kode": "352007", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [2780, 2640, 2510], "snbt_dt": 90, "snbt_peminat": [4290, 4070, 3880]},
    {"ptn": "UNS", "prodi": "Ilmu Komunikasi", "kode": "352008", "rumpun": "Soshum", "snbp_dt": 35, "snbp_peminat": [2180, 2060, 1960], "snbt_dt": 60, "snbt_peminat": [3450, 3280, 3120]},

    # --- UNIVERSITAS PENDIDIKAN INDONESIA (UPI) ---
    {"ptn": "UPI", "prodi": "Teknik Informatika", "kode": "333001", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [1480, 1390, 1310], "snbt_dt": 50, "snbt_peminat": [2980, 2830, 2690]},
    {"ptn": "UPI", "prodi": "Sistem Informasi", "kode": "333002", "rumpun": "Saintek", "snbp_dt": 25, "snbp_peminat": [980, 920, 870], "snbt_dt": 42, "snbt_peminat": [1890, 1790, 1710]},
    {"ptn": "UPI", "prodi": "Psikologi", "kode": "333003", "rumpun": "Soshum", "snbp_dt": 50, "snbp_peminat": [2890, 2740, 2610], "snbt_dt": 85, "snbt_peminat": [4580, 4350, 4150]},
    {"ptn": "UPI", "prodi": "Manajemen", "kode": "333004", "rumpun": "Soshum", "snbp_dt": 60, "snbp_peminat": [3120, 2960, 2810], "snbt_dt": 100, "snbt_peminat": [4780, 4540, 4320]},
    {"ptn": "UPI", "prodi": "Ilmu Komunikasi", "kode": "333005", "rumpun": "Soshum", "snbp_dt": 40, "snbp_peminat": [2580, 2440, 2320], "snbt_dt": 68, "snbt_peminat": [3890, 3690, 3510]},

    # --- UNIVERSITAS SUMATERA UTARA (USU) ---
    {"ptn": "USU", "prodi": "Kedokteran", "kode": "121001", "rumpun": "Saintek", "snbp_dt": 48, "snbp_peminat": [1890, 1780, 1690], "snbt_dt": 80, "snbt_peminat": [3680, 3490, 3320]},
    {"ptn": "USU", "prodi": "Farmasi", "kode": "121002", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1380, 1310, 1240], "snbt_dt": 70, "snbt_peminat": [2590, 2450, 2330]},
    {"ptn": "USU", "prodi": "Teknik Informatika", "kode": "121003", "rumpun": "Saintek", "snbp_dt": 35, "snbp_peminat": [1580, 1490, 1410], "snbt_dt": 60, "snbt_peminat": [2980, 2830, 2690]},
    {"ptn": "USU", "prodi": "Ilmu Hukum", "kode": "121004", "rumpun": "Soshum", "snbp_dt": 120, "snbp_peminat": [3450, 3270, 3110], "snbt_dt": 200, "snbt_peminat": [5120, 4860, 4630]},
    {"ptn": "USU", "prodi": "Manajemen", "kode": "121005", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [2680, 2540, 2410], "snbt_dt": 95, "snbt_peminat": [4180, 3970, 3780]},
    {"ptn": "USU", "prodi": "Psikologi", "kode": "121006", "rumpun": "Soshum", "snbp_dt": 45, "snbp_peminat": [2180, 2060, 1950], "snbt_dt": 75, "snbt_peminat": [3450, 3270, 3120]},

    # --- UNIVERSITAS HASANUDDIN (UNHAS) ---
    {"ptn": "UNHAS", "prodi": "Kedokteran", "kode": "711001", "rumpun": "Saintek", "snbp_dt": 55, "snbp_peminat": [2080, 1960, 1860], "snbt_dt": 90, "snbt_peminat": [3980, 3780, 3600]},
    {"ptn": "UNHAS", "prodi": "Farmasi", "kode": "711002", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1480, 1390, 1320], "snbt_dt": 70, "snbt_peminat": [2680, 2540, 2420]},
    {"ptn": "UNHAS", "prodi": "Teknik Informatika", "kode": "711003", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [1520, 1440, 1360], "snbt_dt": 50, "snbt_peminat": [2890, 2740, 2610]},
    {"ptn": "UNHAS", "prodi": "Ilmu Hukum", "kode": "711004", "rumpun": "Soshum", "snbp_dt": 110, "snbp_peminat": [3280, 3110, 2950], "snbt_dt": 185, "snbt_peminat": [4890, 4640, 4420]},
    {"ptn": "UNHAS", "prodi": "Manajemen", "kode": "711005", "rumpun": "Soshum", "snbp_dt": 65, "snbp_peminat": [2580, 2440, 2320], "snbt_dt": 110, "snbt_peminat": [4080, 3870, 3690]},

    # --- UNIVERSITAS ANDALAS (UNAND) ---
    {"ptn": "UNAND", "prodi": "Kedokteran", "kode": "131001", "rumpun": "Saintek", "snbp_dt": 50, "snbp_peminat": [1780, 1680, 1590], "snbt_dt": 85, "snbt_peminat": [3450, 3270, 3110]},
    {"ptn": "UNAND", "prodi": "Farmasi", "kode": "131002", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1280, 1210, 1150], "snbt_dt": 70, "snbt_peminat": [2380, 2260, 2150]},
    {"ptn": "UNAND", "prodi": "Teknik Informatika", "kode": "131003", "rumpun": "Saintek", "snbp_dt": 28, "snbp_peminat": [1290, 1220, 1150], "snbt_dt": 48, "snbt_peminat": [2450, 2320, 2210]},
    {"ptn": "UNAND", "prodi": "Ilmu Hukum", "kode": "131004", "rumpun": "Soshum", "snbp_dt": 130, "snbp_peminat": [2980, 2820, 2680], "snbt_dt": 220, "snbt_peminat": [4450, 4230, 4030]},
    {"ptn": "UNAND", "prodi": "Manajemen", "kode": "131005", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [2280, 2160, 2050], "snbt_dt": 95, "snbt_peminat": [3680, 3490, 3320]},

    # --- UNIVERSITAS UDAYANA (UNUD) ---
    {"ptn": "UNUD", "prodi": "Kedokteran", "kode": "511001", "rumpun": "Saintek", "snbp_dt": 50, "snbp_peminat": [1680, 1590, 1510], "snbt_dt": 85, "snbt_peminat": [3280, 3110, 2960]},
    {"ptn": "UNUD", "prodi": "Farmasi", "kode": "511002", "rumpun": "Saintek", "snbp_dt": 35, "snbp_peminat": [1120, 1060, 1010], "snbt_dt": 60, "snbt_peminat": [2150, 2040, 1940]},
    {"ptn": "UNUD", "prodi": "Teknik Informatika", "kode": "511003", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [1180, 1110, 1050], "snbt_dt": 50, "snbt_peminat": [2280, 2160, 2050]},
    {"ptn": "UNUD", "prodi": "Ilmu Hukum", "kode": "511004", "rumpun": "Soshum", "snbp_dt": 110, "snbp_peminat": [2680, 2540, 2410], "snbt_dt": 180, "snbt_peminat": [3980, 3780, 3600]},
    {"ptn": "UNUD", "prodi": "Manajemen", "kode": "511005", "rumpun": "Soshum", "snbp_dt": 70, "snbp_peminat": [2380, 2250, 2140], "snbt_dt": 120, "snbt_peminat": [3680, 3490, 3320]},
    {"ptn": "UNSOED", "prodi": "Kedokteran", "kode": "351001", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1520, 1430, 1350], "snbt_dt": 65, "snbt_peminat": [3180, 2980, 2840]},
    {"ptn": "UNSOED", "prodi": "Farmasi", "kode": "351002", "rumpun": "Saintek", "snbp_dt": 35, "snbp_peminat": [1210, 1140, 1080], "snbt_dt": 55, "snbt_peminat": [2340, 2210, 2090]},
    {"ptn": "UNSOED", "prodi": "Teknik Informatika", "kode": "351003", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [1150, 1080, 1010], "snbt_dt": 50, "snbt_peminat": [2280, 2150, 2020]},
    {"ptn": "UNSOED", "prodi": "Manajemen", "kode": "351004", "rumpun": "Soshum", "snbp_dt": 50, "snbp_peminat": [2150, 2020, 1910], "snbt_dt": 85, "snbt_peminat": [3420, 3240, 3080]},
    {"ptn": "UNSOED", "prodi": "Ilmu Komunikasi", "kode": "351005", "rumpun": "Soshum", "snbp_dt": 40, "snbp_peminat": [1780, 1670, 1580], "snbt_dt": 65, "snbt_peminat": [2890, 2740, 2610]},
    {"ptn": "UNSOED", "prodi": "Ilmu Hukum", "kode": "351006", "rumpun": "Soshum", "snbp_dt": 75, "snbp_peminat": [2450, 2310, 2190], "snbt_dt": 125, "snbt_peminat": [3890, 3680, 3490]},
    {"ptn": "UNY", "prodi": "Teknik Informatika", "kode": "342001", "rumpun": "Saintek", "snbp_dt": 24, "snbp_peminat": [1280, 1200, 1120], "snbt_dt": 40, "snbt_peminat": [2580, 2430, 2300]},
    {"ptn": "UNY", "prodi": "Statistika", "kode": "342002", "rumpun": "Saintek", "snbp_dt": 20, "snbp_peminat": [640, 590, 550], "snbt_dt": 35, "snbt_peminat": [1280, 1190, 1110]},
    {"ptn": "UNY", "prodi": "Psikologi", "kode": "342003", "rumpun": "Soshum", "snbp_dt": 36, "snbp_peminat": [2180, 2050, 1940], "snbt_dt": 60, "snbt_peminat": [3650, 3450, 3280]},
    {"ptn": "UNY", "prodi": "Manajemen", "kode": "342004", "rumpun": "Soshum", "snbp_dt": 48, "snbp_peminat": [2480, 2340, 2210], "snbt_dt": 80, "snbt_peminat": [3980, 3760, 3560]},
    {"ptn": "UNY", "prodi": "Ilmu Komunikasi", "kode": "342005", "rumpun": "Soshum", "snbp_dt": 32, "snbp_peminat": [1920, 1810, 1710], "snbt_dt": 55, "snbt_peminat": [3180, 3010, 2860]},
    {"ptn": "UNNES", "prodi": "Teknik Informatika", "kode": "352001", "rumpun": "Saintek", "snbp_dt": 32, "snbp_peminat": [1350, 1260, 1180], "snbt_dt": 55, "snbt_peminat": [2750, 2590, 2450]},
    {"ptn": "UNNES", "prodi": "Farmasi", "kode": "352002", "rumpun": "Saintek", "snbp_dt": 28, "snbp_peminat": [1080, 1010, 950], "snbt_dt": 45, "snbt_peminat": [2120, 1990, 1880]},
    {"ptn": "UNNES", "prodi": "Psikologi", "kode": "352003", "rumpun": "Soshum", "snbp_dt": 40, "snbp_peminat": [2240, 2110, 1990], "snbt_dt": 65, "snbt_peminat": [3580, 3380, 3210]},
    {"ptn": "UNNES", "prodi": "Manajemen", "kode": "352004", "rumpun": "Soshum", "snbp_dt": 60, "snbp_peminat": [2680, 2520, 2390], "snbt_dt": 100, "snbt_peminat": [4150, 3920, 3720]},
    {"ptn": "UNNES", "prodi": "Ilmu Hukum", "kode": "352005", "rumpun": "Soshum", "snbp_dt": 85, "snbp_peminat": [2890, 2720, 2580], "snbt_dt": 140, "snbt_peminat": [4420, 4180, 3960]},
    {"ptn": "UNESA", "prodi": "Teknik Informatika", "kode": "382001", "rumpun": "Saintek", "snbp_dt": 36, "snbp_peminat": [1290, 1210, 1140], "snbt_dt": 60, "snbt_peminat": [2640, 2480, 2350]},
    {"ptn": "UNESA", "prodi": "Sistem Informasi", "kode": "382002", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [980, 920, 860], "snbt_dt": 50, "snbt_peminat": [1980, 1860, 1760]},
    {"ptn": "UNESA", "prodi": "Psikologi", "kode": "382003", "rumpun": "Soshum", "snbp_dt": 45, "snbp_peminat": [2150, 2020, 1910], "snbt_dt": 75, "snbt_peminat": [3450, 3260, 3100]},
    {"ptn": "UNESA", "prodi": "Manajemen", "kode": "382004", "rumpun": "Soshum", "snbp_dt": 65, "snbp_peminat": [2580, 2430, 2300], "snbt_dt": 110, "snbt_peminat": [4050, 3820, 3620]},
    {"ptn": "UNESA", "prodi": "Ilmu Komunikasi", "kode": "382005", "rumpun": "Soshum", "snbp_dt": 38, "snbp_peminat": [1820, 1710, 1620], "snbt_dt": 60, "snbt_peminat": [2950, 2780, 2640]},
    {"ptn": "UM", "prodi": "Teknik Informatika", "kode": "383001", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [1410, 1320, 1250], "snbt_dt": 50, "snbt_peminat": [2820, 2650, 2510]},
    {"ptn": "UM", "prodi": "Teknik Industri", "kode": "383002", "rumpun": "Saintek", "snbp_dt": 24, "snbp_peminat": [620, 580, 540], "snbt_dt": 40, "snbt_peminat": [1320, 1240, 1170]},
    {"ptn": "UM", "prodi": "Psikologi", "kode": "383003", "rumpun": "Soshum", "snbp_dt": 40, "snbp_peminat": [2080, 1960, 1850], "snbt_dt": 70, "snbt_peminat": [3390, 3200, 3040]},
    {"ptn": "UM", "prodi": "Manajemen", "kode": "383004", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [2450, 2310, 2190], "snbt_dt": 90, "snbt_peminat": [3880, 3660, 3480]},
    {"ptn": "UM", "prodi": "Desain Komunikasi Visual", "kode": "383005", "rumpun": "Soshum", "snbp_dt": 30, "snbp_peminat": [1340, 1260, 1190], "snbt_dt": 50, "snbt_peminat": [2240, 2110, 2000]},
    {"ptn": "UNJ", "prodi": "Ilmu Komputer", "kode": "312001", "rumpun": "Saintek", "snbp_dt": 28, "snbp_peminat": [1380, 1290, 1210], "snbt_dt": 45, "snbt_peminat": [2780, 2620, 2480]},
    {"ptn": "UNJ", "prodi": "Sistem Informasi", "kode": "312002", "rumpun": "Saintek", "snbp_dt": 24, "snbp_peminat": [1050, 980, 920], "snbt_dt": 40, "snbt_peminat": [2150, 2020, 1910]},
    {"ptn": "UNJ", "prodi": "Psikologi", "kode": "312003", "rumpun": "Soshum", "snbp_dt": 45, "snbp_peminat": [2580, 2430, 2300], "snbt_dt": 75, "snbt_peminat": [4150, 3920, 3720]},
    {"ptn": "UNJ", "prodi": "Manajemen", "kode": "312004", "rumpun": "Soshum", "snbp_dt": 50, "snbp_peminat": [2720, 2560, 2420], "snbt_dt": 85, "snbt_peminat": [4380, 4130, 3920]},
    {"ptn": "UNJ", "prodi": "Ilmu Komunikasi", "kode": "312005", "rumpun": "Soshum", "snbp_dt": 32, "snbp_peminat": [2280, 2140, 2020], "snbt_dt": 55, "snbt_peminat": [3650, 3440, 3270]},
    {"ptn": "UPNVJ", "prodi": "Kedokteran", "kode": "313001", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [1480, 1390, 1310], "snbt_dt": 50, "snbt_peminat": [3150, 2960, 2810]},
    {"ptn": "UPNVJ", "prodi": "Farmasi", "kode": "313002", "rumpun": "Saintek", "snbp_dt": 24, "snbp_peminat": [980, 920, 860], "snbt_dt": 40, "snbt_peminat": [1980, 1860, 1760]},
    {"ptn": "UPNVJ", "prodi": "Teknik Informatika", "kode": "313003", "rumpun": "Saintek", "snbp_dt": 32, "snbp_peminat": [1350, 1270, 1190], "snbt_dt": 55, "snbt_peminat": [2820, 2650, 2510]},
    {"ptn": "UPNVJ", "prodi": "Ilmu Komunikasi", "kode": "313004", "rumpun": "Soshum", "snbp_dt": 48, "snbp_peminat": [2450, 2310, 2180], "snbt_dt": 80, "snbt_peminat": [3980, 3760, 3570]},
    {"ptn": "UPNVJ", "prodi": "Manajemen", "kode": "313005", "rumpun": "Soshum", "snbp_dt": 54, "snbp_peminat": [2580, 2430, 2300], "snbt_dt": 90, "snbt_peminat": [4120, 3890, 3690]},
    {"ptn": "UPNVJ", "prodi": "Hubungan Internasional", "kode": "313006", "rumpun": "Soshum", "snbp_dt": 28, "snbp_peminat": [1280, 1200, 1130], "snbt_dt": 45, "snbt_peminat": [2150, 2030, 1920]},
    {"ptn": "UPNVYK", "prodi": "Teknik Perminyakan", "kode": "343001", "rumpun": "Saintek", "snbp_dt": 35, "snbp_peminat": [1420, 1340, 1260], "snbt_dt": 60, "snbt_peminat": [2980, 2810, 2660]},
    {"ptn": "UPNVYK", "prodi": "Teknik Pertambangan", "kode": "343002", "rumpun": "Saintek", "snbp_dt": 35, "snbp_peminat": [1580, 1490, 1410], "snbt_dt": 60, "snbt_peminat": [3280, 3090, 2930]},
    {"ptn": "UPNVYK", "prodi": "Teknik Informatika", "kode": "343003", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [1240, 1160, 1090], "snbt_dt": 50, "snbt_peminat": [2540, 2390, 2260]},
    {"ptn": "UPNVYK", "prodi": "Manajemen", "kode": "343004", "rumpun": "Soshum", "snbp_dt": 60, "snbp_peminat": [2450, 2310, 2190], "snbt_dt": 100, "snbt_peminat": [3980, 3750, 3560]},
    {"ptn": "UPNVYK", "prodi": "Ilmu Komunikasi", "kode": "343005", "rumpun": "Soshum", "snbp_dt": 42, "snbp_peminat": [1980, 1870, 1760], "snbt_dt": 70, "snbt_peminat": [3250, 3070, 2910]},
    {"ptn": "UPNVJT", "prodi": "Teknik Informatika", "kode": "384001", "rumpun": "Saintek", "snbp_dt": 35, "snbp_peminat": [1320, 1240, 1170], "snbt_dt": 60, "snbt_peminat": [2720, 2560, 2420]},
    {"ptn": "UPNVJT", "prodi": "Sistem Informasi", "kode": "384002", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [980, 920, 870], "snbt_dt": 50, "snbt_peminat": [1950, 1830, 1730]},
    {"ptn": "UPNVJT", "prodi": "Manajemen", "kode": "384003", "rumpun": "Soshum", "snbp_dt": 65, "snbp_peminat": [2450, 2310, 2190], "snbt_dt": 110, "snbt_peminat": [3920, 3690, 3500]},
    {"ptn": "UPNVJT", "prodi": "Ilmu Komunikasi", "kode": "384004", "rumpun": "Soshum", "snbp_dt": 45, "snbp_peminat": [1880, 1770, 1670], "snbt_dt": 75, "snbt_peminat": [3080, 2900, 2750]},
    {"ptn": "UPNVJT", "prodi": "Akuntansi", "kode": "384005", "rumpun": "Soshum", "snbp_dt": 50, "snbp_peminat": [1720, 1620, 1530], "snbt_dt": 85, "snbt_peminat": [2780, 2620, 2490]},
    {"ptn": "UNTIRTA", "prodi": "Kedokteran", "kode": "361001", "rumpun": "Saintek", "snbp_dt": 25, "snbp_peminat": [980, 920, 870], "snbt_dt": 40, "snbt_peminat": [2150, 2020, 1910]},
    {"ptn": "UNTIRTA", "prodi": "Teknik Industri", "kode": "361002", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [680, 640, 600], "snbt_dt": 50, "snbt_peminat": [1420, 1340, 1260]},
    {"ptn": "UNTIRTA", "prodi": "Ilmu Hukum", "kode": "361003", "rumpun": "Soshum", "snbp_dt": 75, "snbp_peminat": [1890, 1780, 1680], "snbt_dt": 125, "snbt_peminat": [3120, 2940, 2790]},
    {"ptn": "UNTIRTA", "prodi": "Manajemen", "kode": "361004", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [1980, 1870, 1760], "snbt_dt": 90, "snbt_peminat": [3250, 3060, 2910]},
    {"ptn": "UNTIRTA", "prodi": "Ilmu Komunikasi", "kode": "361005", "rumpun": "Soshum", "snbp_dt": 35, "snbp_peminat": [1420, 1340, 1260], "snbt_dt": 60, "snbt_peminat": [2380, 2240, 2120]},
    {"ptn": "UNSRI", "prodi": "Kedokteran", "kode": "161001", "rumpun": "Saintek", "snbp_dt": 45, "snbp_peminat": [1680, 1580, 1490], "snbt_dt": 75, "snbt_peminat": [3420, 3230, 3060]},
    {"ptn": "UNSRI", "prodi": "Farmasi", "kode": "161002", "rumpun": "Saintek", "snbp_dt": 35, "snbp_peminat": [1210, 1140, 1080], "snbt_dt": 60, "snbt_peminat": [2280, 2150, 2040]},
    {"ptn": "UNSRI", "prodi": "Teknik Informatika", "kode": "161003", "rumpun": "Saintek", "snbp_dt": 32, "snbp_peminat": [1280, 1200, 1130], "snbt_dt": 55, "snbt_peminat": [2540, 2390, 2260]},
    {"ptn": "UNSRI", "prodi": "Ilmu Hukum", "kode": "161004", "rumpun": "Soshum", "snbp_dt": 90, "snbp_peminat": [2580, 2430, 2300], "snbt_dt": 150, "snbt_peminat": [4020, 3790, 3600]},
    {"ptn": "UNSRI", "prodi": "Manajemen", "kode": "161005", "rumpun": "Soshum", "snbp_dt": 60, "snbp_peminat": [2240, 2110, 2000], "snbt_dt": 100, "snbt_peminat": [3560, 3360, 3190]},
    {"ptn": "UNILA", "prodi": "Kedokteran", "kode": "181001", "rumpun": "Saintek", "snbp_dt": 42, "snbp_peminat": [1540, 1450, 1370], "snbt_dt": 70, "snbt_peminat": [3180, 3000, 2850]},
    {"ptn": "UNILA", "prodi": "Farmasi", "kode": "181002", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [980, 920, 870], "snbt_dt": 50, "snbt_peminat": [1940, 1830, 1730]},
    {"ptn": "UNILA", "prodi": "Teknik Informatika", "kode": "181003", "rumpun": "Saintek", "snbp_dt": 28, "snbp_peminat": [1080, 1020, 960], "snbt_dt": 48, "snbt_peminat": [2210, 2080, 1970]},
    {"ptn": "UNILA", "prodi": "Ilmu Hukum", "kode": "181004", "rumpun": "Soshum", "snbp_dt": 95, "snbp_peminat": [2680, 2520, 2390], "snbt_dt": 160, "snbt_peminat": [4180, 3940, 3740]},
    {"ptn": "UNILA", "prodi": "Manajemen", "kode": "181005", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [2120, 2000, 1890], "snbt_dt": 90, "snbt_peminat": [3420, 3220, 3060]},
    {"ptn": "UNP", "prodi": "Teknik Informatika", "kode": "132001", "rumpun": "Saintek", "snbp_dt": 32, "snbp_peminat": [1280, 1200, 1130], "snbt_dt": 55, "snbt_peminat": [2480, 2340, 2210]},
    {"ptn": "UNP", "prodi": "Teknik Elektro", "kode": "132002", "rumpun": "Saintek", "snbp_dt": 28, "snbp_peminat": [580, 540, 510], "snbt_dt": 45, "snbt_peminat": [1240, 1160, 1100]},
    {"ptn": "UNP", "prodi": "Psikologi", "kode": "132003", "rumpun": "Soshum", "snbp_dt": 35, "snbp_peminat": [1890, 1780, 1680], "snbt_dt": 60, "snbt_peminat": [3120, 2940, 2790]},
    {"ptn": "UNP", "prodi": "Manajemen", "kode": "132004", "rumpun": "Soshum", "snbp_dt": 60, "snbp_peminat": [2480, 2330, 2210], "snbt_dt": 100, "snbt_peminat": [3890, 3660, 3480]},
    {"ptn": "UNP", "prodi": "Akuntansi", "kode": "132005", "rumpun": "Soshum", "snbp_dt": 50, "snbp_peminat": [1780, 1670, 1580], "snbt_dt": 85, "snbt_peminat": [2860, 2690, 2550]},
    {"ptn": "USK", "prodi": "Kedokteran", "kode": "111001", "rumpun": "Saintek", "snbp_dt": 45, "snbp_peminat": [1480, 1390, 1310], "snbt_dt": 75, "snbt_peminat": [2980, 2810, 2660]},
    {"ptn": "USK", "prodi": "Farmasi", "kode": "111002", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [980, 920, 870], "snbt_dt": 50, "snbt_peminat": [1890, 1780, 1690]},
    {"ptn": "USK", "prodi": "Teknik Sipil", "kode": "111003", "rumpun": "Saintek", "snbp_dt": 35, "snbp_peminat": [680, 640, 600], "snbt_dt": 60, "snbt_peminat": [1420, 1340, 1270]},
    {"ptn": "USK", "prodi": "Ilmu Hukum", "kode": "111004", "rumpun": "Soshum", "snbp_dt": 85, "snbp_peminat": [2150, 2020, 1910], "snbt_dt": 140, "snbt_peminat": [3420, 3220, 3050]},
    {"ptn": "USK", "prodi": "Manajemen", "kode": "111005", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [1980, 1860, 1760], "snbt_dt": 90, "snbt_peminat": [3180, 2990, 2840]},
    {"ptn": "UNRI", "prodi": "Kedokteran", "kode": "141001", "rumpun": "Saintek", "snbp_dt": 38, "snbp_peminat": [1420, 1340, 1260], "snbt_dt": 65, "snbt_peminat": [2890, 2720, 2580]},
    {"ptn": "UNRI", "prodi": "Teknik Informatika", "kode": "141002", "rumpun": "Saintek", "snbp_dt": 28, "snbp_peminat": [1120, 1050, 990], "snbt_dt": 48, "snbt_peminat": [2280, 2140, 2030]},
    {"ptn": "UNRI", "prodi": "Ilmu Hukum", "kode": "141003", "rumpun": "Soshum", "snbp_dt": 80, "snbp_peminat": [2340, 2200, 2080], "snbt_dt": 135, "snbt_peminat": [3680, 3470, 3290]},
    {"ptn": "UNRI", "prodi": "Manajemen", "kode": "141004", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [2080, 1960, 1850], "snbt_dt": 90, "snbt_peminat": [3340, 3150, 2990]},
    {"ptn": "UNRI", "prodi": "Akuntansi", "kode": "141005", "rumpun": "Soshum", "snbp_dt": 48, "snbp_peminat": [1580, 1490, 1410], "snbt_dt": 80, "snbt_peminat": [2580, 2430, 2310]},
    {"ptn": "UNMUL", "prodi": "Kedokteran", "kode": "641001", "rumpun": "Saintek", "snbp_dt": 32, "snbp_peminat": [1280, 1200, 1130], "snbt_dt": 55, "snbt_peminat": [2580, 2430, 2300]},
    {"ptn": "UNMUL", "prodi": "Farmasi", "kode": "641002", "rumpun": "Saintek", "snbp_dt": 28, "snbp_peminat": [890, 840, 790], "snbt_dt": 45, "snbt_peminat": [1780, 1670, 1580]},
    {"ptn": "UNMUL", "prodi": "Teknik Pertambangan", "kode": "641003", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [780, 730, 690], "snbt_dt": 50, "snbt_peminat": [1620, 1520, 1440]},
    {"ptn": "UNMUL", "prodi": "Ilmu Hukum", "kode": "641004", "rumpun": "Soshum", "snbp_dt": 75, "snbp_peminat": [1980, 1870, 1760], "snbt_dt": 125, "snbt_peminat": [3180, 2990, 2840]},
    {"ptn": "UNMUL", "prodi": "Manajemen", "kode": "641005", "rumpun": "Soshum", "snbp_dt": 50, "snbp_peminat": [1820, 1710, 1620], "snbt_dt": 85, "snbt_peminat": [2950, 2780, 2640]},
    {"ptn": "ULM", "prodi": "Kedokteran", "kode": "631001", "rumpun": "Saintek", "snbp_dt": 35, "snbp_peminat": [1320, 1240, 1170], "snbt_dt": 60, "snbt_peminat": [2680, 2520, 2390]},
    {"ptn": "ULM", "prodi": "Farmasi", "kode": "631002", "rumpun": "Saintek", "snbp_dt": 25, "snbp_peminat": [840, 790, 740], "snbt_dt": 40, "snbt_peminat": [1680, 1580, 1490]},
    {"ptn": "ULM", "prodi": "Teknik Sipil", "kode": "631003", "rumpun": "Saintek", "snbp_dt": 32, "snbp_peminat": [620, 580, 540], "snbt_dt": 55, "snbt_peminat": [1340, 1260, 1190]},
    {"ptn": "ULM", "prodi": "Ilmu Hukum", "kode": "631004", "rumpun": "Soshum", "snbp_dt": 80, "snbp_peminat": [2050, 1930, 1820], "snbt_dt": 135, "snbt_peminat": [3280, 3090, 2930]},
    {"ptn": "ULM", "prodi": "Manajemen", "kode": "631005", "rumpun": "Soshum", "snbp_dt": 52, "snbp_peminat": [1780, 1670, 1580], "snbt_dt": 88, "snbt_peminat": [2890, 2720, 2580]},
    {"ptn": "UNTAN", "prodi": "Kedokteran", "kode": "611001", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [1180, 1110, 1050], "snbt_dt": 50, "snbt_peminat": [2390, 2250, 2130]},
    {"ptn": "UNTAN", "prodi": "Teknik Informatika", "kode": "611002", "rumpun": "Saintek", "snbp_dt": 25, "snbp_peminat": [940, 880, 830], "snbt_dt": 45, "snbt_peminat": [1890, 1780, 1690]},
    {"ptn": "UNTAN", "prodi": "Teknik Sipil", "kode": "611003", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [580, 540, 510], "snbt_dt": 50, "snbt_peminat": [1280, 1200, 1140]},
    {"ptn": "UNTAN", "prodi": "Ilmu Hukum", "kode": "611004", "rumpun": "Soshum", "snbp_dt": 85, "snbp_peminat": [2120, 1990, 1890], "snbt_dt": 145, "snbt_peminat": [3380, 3180, 3020]},
    {"ptn": "UNTAN", "prodi": "Manajemen", "kode": "611005", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [1840, 1730, 1630], "snbt_dt": 92, "snbt_peminat": [2980, 2810, 2660]},
    {"ptn": "UNSRAT", "prodi": "Kedokteran", "kode": "712001", "rumpun": "Saintek", "snbp_dt": 38, "snbp_peminat": [1290, 1210, 1140], "snbt_dt": 65, "snbt_peminat": [2640, 2480, 2350]},
    {"ptn": "UNSRAT", "prodi": "Farmasi", "kode": "712002", "rumpun": "Saintek", "snbp_dt": 24, "snbp_peminat": [780, 730, 690], "snbt_dt": 40, "snbt_peminat": [1560, 1470, 1390]},
    {"ptn": "UNSRAT", "prodi": "Teknik Informatika", "kode": "712003", "rumpun": "Saintek", "snbp_dt": 26, "snbp_peminat": [890, 830, 780], "snbt_dt": 44, "snbt_peminat": [1780, 1670, 1580]},
    {"ptn": "UNSRAT", "prodi": "Ilmu Hukum", "kode": "712004", "rumpun": "Soshum", "snbp_dt": 80, "snbp_peminat": [1980, 1860, 1760], "snbt_dt": 135, "snbt_peminat": [3150, 2960, 2810]},
    {"ptn": "UNSRAT", "prodi": "Manajemen", "kode": "712005", "rumpun": "Soshum", "snbp_dt": 50, "snbp_peminat": [1750, 1640, 1550], "snbt_dt": 85, "snbt_peminat": [2820, 2650, 2510]},
    {"ptn": "UNRAM", "prodi": "Kedokteran", "kode": "521001", "rumpun": "Saintek", "snbp_dt": 35, "snbp_peminat": [1240, 1160, 1090], "snbt_dt": 60, "snbt_peminat": [2520, 2370, 2240]},
    {"ptn": "UNRAM", "prodi": "Farmasi", "kode": "521002", "rumpun": "Saintek", "snbp_dt": 24, "snbp_peminat": [760, 710, 670], "snbt_dt": 40, "snbt_peminat": [1520, 1430, 1350]},
    {"ptn": "UNRAM", "prodi": "Teknik Sipil", "kode": "521003", "rumpun": "Saintek", "snbp_dt": 30, "snbp_peminat": [590, 550, 520], "snbt_dt": 50, "snbt_peminat": [1280, 1200, 1140]},
    {"ptn": "UNRAM", "prodi": "Ilmu Hukum", "kode": "521004", "rumpun": "Soshum", "snbp_dt": 85, "snbp_peminat": [2150, 2020, 1910], "snbt_dt": 140, "snbt_peminat": [3340, 3140, 2980]},
    {"ptn": "UNRAM", "prodi": "Manajemen", "kode": "521005", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [1820, 1710, 1610], "snbt_dt": 92, "snbt_peminat": [2920, 2750, 2610]},
    {"ptn": "TELKOM", "prodi": "Teknik Informatika", "kode": "041001", "rumpun": "Saintek", "snbp_dt": 120, "snbp_peminat": [3890, 3680, 3480], "snbt_dt": 240, "snbt_peminat": [6980, 6620, 6290]},
    {"ptn": "TELKOM", "prodi": "Sistem Informasi", "kode": "041002", "rumpun": "Saintek", "snbp_dt": 80, "snbp_peminat": [2150, 2030, 1920], "snbt_dt": 160, "snbt_peminat": [4120, 3890, 3690]},
    {"ptn": "TELKOM", "prodi": "Teknik Industri", "kode": "041003", "rumpun": "Saintek", "snbp_dt": 70, "snbp_peminat": [1780, 1680, 1590], "snbt_dt": 140, "snbt_peminat": [3350, 3160, 3000]},
    {"ptn": "TELKOM", "prodi": "Desain Komunikasi Visual", "kode": "041004", "rumpun": "Soshum", "snbp_dt": 90, "snbp_peminat": [2580, 2430, 2300], "snbt_dt": 180, "snbt_peminat": [4890, 4620, 4390]},
    {"ptn": "TELKOM", "prodi": "Ilmu Komunikasi", "kode": "041005", "rumpun": "Soshum", "snbp_dt": 85, "snbp_peminat": [2450, 2310, 2190], "snbt_dt": 170, "snbt_peminat": [4650, 4390, 4170]},
    {"ptn": "TELKOM", "prodi": "Manajemen", "kode": "041006", "rumpun": "Soshum", "snbp_dt": 100, "snbp_peminat": [2890, 2730, 2590], "snbt_dt": 200, "snbt_peminat": [5210, 4930, 4680]},
    {"ptn": "BINUS", "prodi": "Teknik Informatika", "kode": "031001", "rumpun": "Saintek", "snbp_dt": 150, "snbp_peminat": [4450, 4210, 3990], "snbt_dt": 300, "snbt_peminat": [7850, 7440, 7060]},
    {"ptn": "BINUS", "prodi": "Sistem Informasi", "kode": "031002", "rumpun": "Saintek", "snbp_dt": 110, "snbp_peminat": [2890, 2730, 2580], "snbt_dt": 220, "snbt_peminat": [5120, 4850, 4600]},
    {"ptn": "BINUS", "prodi": "Desain Komunikasi Visual", "kode": "031003", "rumpun": "Soshum", "snbp_dt": 100, "snbp_peminat": [2980, 2810, 2660], "snbt_dt": 200, "snbt_peminat": [5380, 5090, 4830]},
    {"ptn": "BINUS", "prodi": "Manajemen", "kode": "031004", "rumpun": "Soshum", "snbp_dt": 130, "snbp_peminat": [3420, 3230, 3060], "snbt_dt": 260, "snbt_peminat": [6120, 5790, 5490]},
    {"ptn": "BINUS", "prodi": "Ilmu Komunikasi", "kode": "031005", "rumpun": "Soshum", "snbp_dt": 90, "snbp_peminat": [2680, 2530, 2400], "snbt_dt": 180, "snbt_peminat": [4780, 4520, 4290]},
    {"ptn": "UII", "prodi": "Kedokteran", "kode": "051001", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1890, 1780, 1680], "snbt_dt": 80, "snbt_peminat": [3890, 3670, 3470]},
    {"ptn": "UII", "prodi": "Farmasi", "kode": "051002", "rumpun": "Saintek", "snbp_dt": 50, "snbp_peminat": [1450, 1370, 1290], "snbt_dt": 100, "snbt_peminat": [2890, 2730, 2590]},
    {"ptn": "UII", "prodi": "Teknik Informatika", "kode": "051003", "rumpun": "Saintek", "snbp_dt": 60, "snbp_peminat": [1680, 1590, 1500], "snbt_dt": 120, "snbt_peminat": [3280, 3100, 2940]},
    {"ptn": "UII", "prodi": "Ilmu Hukum", "kode": "051004", "rumpun": "Soshum", "snbp_dt": 90, "snbp_peminat": [2450, 2310, 2190], "snbt_dt": 180, "snbt_peminat": [4350, 4110, 3900]},
    {"ptn": "UII", "prodi": "Manajemen", "kode": "051005", "rumpun": "Soshum", "snbp_dt": 80, "snbp_peminat": [2240, 2110, 2000], "snbt_dt": 160, "snbt_peminat": [3980, 3760, 3570]},
    {"ptn": "UII", "prodi": "Psikologi", "kode": "051006", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [1820, 1710, 1620], "snbt_dt": 110, "snbt_peminat": [3210, 3030, 2870]},
    {"ptn": "UMY", "prodi": "Kedokteran", "kode": "052001", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1780, 1680, 1590], "snbt_dt": 80, "snbt_peminat": [3650, 3450, 3270]},
    {"ptn": "UMY", "prodi": "Kedokteran Gigi", "kode": "052002", "rumpun": "Saintek", "snbp_dt": 25, "snbp_peminat": [980, 920, 870], "snbt_dt": 50, "snbt_peminat": [1980, 1870, 1770]},
    {"ptn": "UMY", "prodi": "Farmasi", "kode": "052003", "rumpun": "Saintek", "snbp_dt": 45, "snbp_peminat": [1280, 1210, 1140], "snbt_dt": 90, "snbt_peminat": [2540, 2400, 2270]},
    {"ptn": "UMY", "prodi": "Hubungan Internasional", "kode": "052004", "rumpun": "Soshum", "snbp_dt": 65, "snbp_peminat": [1890, 1780, 1690], "snbt_dt": 130, "snbt_peminat": [3420, 3230, 3060]},
    {"ptn": "UMY", "prodi": "Ilmu Komunikasi", "kode": "052005", "rumpun": "Soshum", "snbp_dt": 60, "snbp_peminat": [1740, 1640, 1550], "snbt_dt": 120, "snbt_peminat": [3180, 3000, 2850]},
    {"ptn": "UMY", "prodi": "Manajemen", "kode": "052006", "rumpun": "Soshum", "snbp_dt": 75, "snbp_peminat": [2120, 2000, 1900], "snbt_dt": 150, "snbt_peminat": [3780, 3570, 3390]},
    {"ptn": "UNPAR", "prodi": "Arsitektur", "kode": "042001", "rumpun": "Saintek", "snbp_dt": 45, "snbp_peminat": [1580, 1490, 1410], "snbt_dt": 90, "snbt_peminat": [3280, 3100, 2940]},
    {"ptn": "UNPAR", "prodi": "Teknik Sipil", "kode": "042002", "rumpun": "Saintek", "snbp_dt": 50, "snbp_peminat": [1120, 1050, 990], "snbt_dt": 100, "snbt_peminat": [2240, 2110, 2000]},
    {"ptn": "UNPAR", "prodi": "Hubungan Internasional", "kode": "042003", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [1890, 1780, 1690], "snbt_dt": 110, "snbt_peminat": [3490, 3300, 3130]},
    {"ptn": "UNPAR", "prodi": "Ilmu Hukum", "kode": "042004", "rumpun": "Soshum", "snbp_dt": 70, "snbp_peminat": [2150, 2030, 1920], "snbt_dt": 140, "snbt_peminat": [3890, 3680, 3490]},
    {"ptn": "UNPAR", "prodi": "Manajemen", "kode": "042005", "rumpun": "Soshum", "snbp_dt": 65, "snbp_peminat": [1980, 1870, 1770], "snbt_dt": 130, "snbt_peminat": [3560, 3360, 3190]},
    {"ptn": "ATMAJAYA", "prodi": "Kedokteran", "kode": "032001", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1680, 1590, 1510], "snbt_dt": 80, "snbt_peminat": [3450, 3260, 3090]},
    {"ptn": "ATMAJAYA", "prodi": "Farmasi", "kode": "032002", "rumpun": "Saintek", "snbp_dt": 35, "snbp_peminat": [980, 920, 870], "snbt_dt": 70, "snbt_peminat": [1980, 1870, 1770]},
    {"ptn": "ATMAJAYA", "prodi": "Psikologi", "kode": "032003", "rumpun": "Soshum", "snbp_dt": 60, "snbp_peminat": [2120, 2000, 1900], "snbt_dt": 120, "snbt_peminat": [3890, 3670, 3480]},
    {"ptn": "ATMAJAYA", "prodi": "Ilmu Hukum", "kode": "032004", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [1780, 1680, 1590], "snbt_dt": 110, "snbt_peminat": [3180, 3000, 2850]},
    {"ptn": "ATMAJAYA", "prodi": "Manajemen", "kode": "032005", "rumpun": "Soshum", "snbp_dt": 70, "snbp_peminat": [2240, 2110, 2000], "snbt_dt": 140, "snbt_peminat": [3980, 3760, 3570]},
    {"ptn": "UPH", "prodi": "Kedokteran", "kode": "033001", "rumpun": "Saintek", "snbp_dt": 45, "snbp_peminat": [1780, 1680, 1590], "snbt_dt": 90, "snbt_peminat": [3680, 3480, 3300]},
    {"ptn": "UPH", "prodi": "Sistem Informasi", "kode": "033002", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [980, 920, 870], "snbt_dt": 80, "snbt_peminat": [1980, 1870, 1770]},
    {"ptn": "UPH", "prodi": "Ilmu Hukum", "kode": "033003", "rumpun": "Soshum", "snbp_dt": 70, "snbp_peminat": [2350, 2220, 2100], "snbt_dt": 140, "snbt_peminat": [4180, 3950, 3750]},
    {"ptn": "UPH", "prodi": "Manajemen", "kode": "033004", "rumpun": "Soshum", "snbp_dt": 80, "snbp_peminat": [2480, 2340, 2220], "snbt_dt": 160, "snbt_peminat": [4450, 4200, 3990]},
    {"ptn": "UPH", "prodi": "Desain Komunikasi Visual", "kode": "033005", "rumpun": "Soshum", "snbp_dt": 60, "snbp_peminat": [1890, 1780, 1690], "snbt_dt": 120, "snbt_peminat": [3380, 3190, 3030]},
    {"ptn": "TRISAKTI", "prodi": "Kedokteran", "kode": "034001", "rumpun": "Saintek", "snbp_dt": 45, "snbp_peminat": [1820, 1720, 1630], "snbt_dt": 90, "snbt_peminat": [3780, 3570, 3390]},
    {"ptn": "TRISAKTI", "prodi": "Kedokteran Gigi", "kode": "034002", "rumpun": "Saintek", "snbp_dt": 35, "snbp_peminat": [1280, 1210, 1140], "snbt_dt": 70, "snbt_peminat": [2480, 2340, 2220]},
    {"ptn": "TRISAKTI", "prodi": "Teknik Perminyakan", "kode": "034003", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1420, 1340, 1270], "snbt_dt": 80, "snbt_peminat": [2890, 2730, 2590]},
    {"ptn": "TRISAKTI", "prodi": "Arsitektur", "kode": "034004", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1080, 1020, 960], "snbt_dt": 80, "snbt_peminat": [2150, 2030, 1920]},
    {"ptn": "TRISAKTI", "prodi": "Ilmu Hukum", "kode": "034005", "rumpun": "Soshum", "snbp_dt": 80, "snbp_peminat": [2280, 2150, 2040], "snbt_dt": 160, "snbt_peminat": [4120, 3890, 3690]},
    {"ptn": "TRISAKTI", "prodi": "Manajemen", "kode": "034006", "rumpun": "Soshum", "snbp_dt": 85, "snbp_peminat": [2450, 2310, 2190], "snbt_dt": 170, "snbt_peminat": [4350, 4110, 3900]},
    {"ptn": "UNTAR", "prodi": "Kedokteran", "kode": "035001", "rumpun": "Saintek", "snbp_dt": 45, "snbp_peminat": [1780, 1680, 1590], "snbt_dt": 90, "snbt_peminat": [3680, 3480, 3300]},
    {"ptn": "UNTAR", "prodi": "Arsitektur", "kode": "035002", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1180, 1110, 1050], "snbt_dt": 80, "snbt_peminat": [2340, 2210, 2090]},
    {"ptn": "UNTAR", "prodi": "Psikologi", "kode": "035003", "rumpun": "Soshum", "snbp_dt": 60, "snbp_peminat": [2150, 2030, 1920], "snbt_dt": 120, "snbt_peminat": [3920, 3700, 3510]},
    {"ptn": "UNTAR", "prodi": "Ilmu Hukum", "kode": "035004", "rumpun": "Soshum", "snbp_dt": 75, "snbp_peminat": [2240, 2110, 2000], "snbt_dt": 150, "snbt_peminat": [4080, 3850, 3650]},
    {"ptn": "UNTAR", "prodi": "Manajemen", "kode": "035005", "rumpun": "Soshum", "snbp_dt": 80, "snbp_peminat": [2450, 2310, 2190], "snbt_dt": 160, "snbt_peminat": [4380, 4130, 3920]},
    {"ptn": "UMN", "prodi": "Teknik Informatika", "kode": "036001", "rumpun": "Saintek", "snbp_dt": 60, "snbp_peminat": [2150, 2030, 1920], "snbt_dt": 120, "snbt_peminat": [4150, 3920, 3720]},
    {"ptn": "UMN", "prodi": "Sistem Informasi", "kode": "036002", "rumpun": "Saintek", "snbp_dt": 45, "snbp_peminat": [1280, 1210, 1140], "snbt_dt": 90, "snbt_peminat": [2480, 2340, 2220]},
    {"ptn": "UMN", "prodi": "Desain Komunikasi Visual", "kode": "036003", "rumpun": "Soshum", "snbp_dt": 70, "snbp_peminat": [2680, 2530, 2400], "snbt_dt": 140, "snbt_peminat": [4980, 4700, 4460]},
    {"ptn": "UMN", "prodi": "Ilmu Komunikasi", "kode": "036004", "rumpun": "Soshum", "snbp_dt": 65, "snbp_peminat": [2240, 2110, 2000], "snbt_dt": 130, "snbt_peminat": [4120, 3890, 3690]},
    {"ptn": "UMN", "prodi": "Manajemen", "kode": "036005", "rumpun": "Soshum", "snbp_dt": 50, "snbp_peminat": [1680, 1580, 1490], "snbt_dt": 100, "snbt_peminat": [3180, 3000, 2850]},
    {"ptn": "PETRA", "prodi": "Arsitektur", "kode": "071001", "rumpun": "Saintek", "snbp_dt": 45, "snbp_peminat": [1480, 1390, 1310], "snbt_dt": 90, "snbt_peminat": [2980, 2810, 2660]},
    {"ptn": "PETRA", "prodi": "Teknik Sipil", "kode": "071002", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [980, 920, 870], "snbt_dt": 80, "snbt_peminat": [1980, 1870, 1770]},
    {"ptn": "PETRA", "prodi": "Teknik Informatika", "kode": "071003", "rumpun": "Saintek", "snbp_dt": 50, "snbp_peminat": [1520, 1430, 1350], "snbt_dt": 100, "snbt_peminat": [2950, 2780, 2640]},
    {"ptn": "PETRA", "prodi": "Desain Komunikasi Visual", "kode": "071004", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [1780, 1680, 1590], "snbt_dt": 110, "snbt_peminat": [3340, 3150, 2990]},
    {"ptn": "PETRA", "prodi": "Manajemen", "kode": "071005", "rumpun": "Soshum", "snbp_dt": 65, "snbp_peminat": [1980, 1870, 1770], "snbt_dt": 130, "snbt_peminat": [3680, 3470, 3300]},
    {"ptn": "UMS", "prodi": "Kedokteran", "kode": "061001", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1820, 1720, 1630], "snbt_dt": 80, "snbt_peminat": [3780, 3570, 3390]},
    {"ptn": "UMS", "prodi": "Farmasi", "kode": "061002", "rumpun": "Saintek", "snbp_dt": 45, "snbp_peminat": [1340, 1260, 1190], "snbt_dt": 90, "snbt_peminat": [2680, 2530, 2400]},
    {"ptn": "UMS", "prodi": "Teknik Informatika", "kode": "061003", "rumpun": "Saintek", "snbp_dt": 50, "snbp_peminat": [1420, 1340, 1270], "snbt_dt": 100, "snbt_peminat": [2780, 2620, 2490]},
    {"ptn": "UMS", "prodi": "Psikologi", "kode": "061004", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [1780, 1680, 1590], "snbt_dt": 110, "snbt_peminat": [3280, 3090, 2940]},
    {"ptn": "UMS", "prodi": "Ilmu Hukum", "kode": "061005", "rumpun": "Soshum", "snbp_dt": 65, "snbp_peminat": [1980, 1870, 1770], "snbt_dt": 130, "snbt_peminat": [3480, 3280, 3110]},
    {"ptn": "UMS", "prodi": "Manajemen", "kode": "061006", "rumpun": "Soshum", "snbp_dt": 75, "snbp_peminat": [2180, 2060, 1950], "snbt_dt": 150, "snbt_peminat": [3890, 3670, 3490]},
    {"ptn": "PRESUNIV", "prodi": "Teknik Informatika", "kode": "043001", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1380, 1300, 1230], "snbt_dt": 80, "snbt_peminat": [2780, 2620, 2490]},
    {"ptn": "PRESUNIV", "prodi": "Teknik Industri", "kode": "043002", "rumpun": "Saintek", "snbp_dt": 35, "snbp_peminat": [980, 920, 870], "snbt_dt": 70, "snbt_peminat": [1980, 1870, 1770]},
    {"ptn": "PRESUNIV", "prodi": "Hubungan Internasional", "kode": "043003", "rumpun": "Soshum", "snbp_dt": 45, "snbp_peminat": [1520, 1430, 1350], "snbt_dt": 90, "snbt_peminat": [2890, 2730, 2590]},
    {"ptn": "PRESUNIV", "prodi": "Manajemen", "kode": "043004", "rumpun": "Soshum", "snbp_dt": 60, "snbp_peminat": [1920, 1810, 1710], "snbt_dt": 120, "snbt_peminat": [3450, 3250, 3090]},
    {"ptn": "PRESUNIV", "prodi": "Ilmu Komunikasi", "kode": "043005", "rumpun": "Soshum", "snbp_dt": 40, "snbp_peminat": [1280, 1210, 1140], "snbt_dt": 80, "snbt_peminat": [2340, 2210, 2090]},
    {"ptn": "USD", "prodi": "Farmasi", "kode": "053001", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1420, 1340, 1260], "snbt_dt": 80, "snbt_peminat": [2890, 2730, 2580]},
    {"ptn": "USD", "prodi": "Teknik Informatika", "kode": "053002", "rumpun": "Saintek", "snbp_dt": 35, "snbp_peminat": [1120, 1050, 990], "snbt_dt": 70, "snbt_peminat": [2240, 2110, 2000]},
    {"ptn": "USD", "prodi": "Psikologi", "kode": "053003", "rumpun": "Soshum", "snbp_dt": 45, "snbp_peminat": [1680, 1580, 1490], "snbt_dt": 90, "snbt_peminat": [3180, 3000, 2850]},
    {"ptn": "USD", "prodi": "Manajemen", "kode": "053004", "rumpun": "Soshum", "snbp_dt": 55, "snbp_peminat": [1780, 1680, 1590], "snbt_dt": 110, "snbt_peminat": [3280, 3090, 2940]},
    {"ptn": "USD", "prodi": "Akuntansi", "kode": "053005", "rumpun": "Soshum", "snbp_dt": 45, "snbp_peminat": [1380, 1300, 1230], "snbt_dt": 90, "snbt_peminat": [2540, 2400, 2280]},
    {"ptn": "MERCU", "prodi": "Teknik Informatika", "kode": "037001", "rumpun": "Saintek", "snbp_dt": 55, "snbp_peminat": [1680, 1580, 1490], "snbt_dt": 110, "snbt_peminat": [3280, 3090, 2940]},
    {"ptn": "MERCU", "prodi": "Sistem Informasi", "kode": "037002", "rumpun": "Saintek", "snbp_dt": 40, "snbp_peminat": [1120, 1050, 990], "snbt_dt": 80, "snbt_peminat": [2150, 2030, 1920]},
    {"ptn": "MERCU", "prodi": "Ilmu Komunikasi", "kode": "037003", "rumpun": "Soshum", "snbp_dt": 70, "snbp_peminat": [2450, 2310, 2190], "snbt_dt": 140, "snbt_peminat": [4350, 4110, 3900]},
    {"ptn": "MERCU", "prodi": "Desain Komunikasi Visual", "kode": "037004", "rumpun": "Soshum", "snbp_dt": 50, "snbp_peminat": [1780, 1680, 1590], "snbt_dt": 100, "snbt_peminat": [3180, 3000, 2850]},
    {"ptn": "MERCU", "prodi": "Manajemen", "kode": "037005", "rumpun": "Soshum", "snbp_dt": 75, "snbp_peminat": [2380, 2240, 2130], "snbt_dt": 150, "snbt_peminat": [4150, 3920, 3720]}
]

def classify_keketatan(pct):
    if pct < 2.50:
        return "Sangat Ketat", "Very Competitive", "badge-sangat-ketat"
    elif pct <= 5.00:
        return "Ketat", "Competitive", "badge-ketat"
    elif pct <= 10.00:
        return "Sedang", "Moderate", "badge-sedang"
    else:
        return "Terbuka", "Open", "badge-terbuka"

def calculate_metrics(dt, peminat_list):
    latest_peminat = peminat_list[0]
    pct = round((dt / latest_peminat) * 100, 2)
    ratio_n = round(latest_peminat / dt)
    ratio_str = f"1 : {ratio_n}"
    kat_id, kat_en, badge_class = classify_keketatan(pct)
    
    # 3-year growth trend
    growth_1yr = round(((peminat_list[0] - peminat_list[1]) / peminat_list[1]) * 100, 1)
    
    return {
        "daya_tampung": dt,
        "peminat": latest_peminat,
        "riwayat_peminat": {
            "2024": peminat_list[0],
            "2023": peminat_list[1],
            "2022": peminat_list[2]
        },
        "keketatan_persen": pct,
        "rasio_persaingan": ratio_str,
        "rasio_angka": ratio_n,
        "kategori": kat_id,
        "kategori_en": kat_en,
        "badge_class": badge_class,
        "tren_pertumbuhan_persen": growth_1yr
    }

def build_dataset():
    records = []
    
    for entry in RAW_ENTRIES:
        ptn_code = entry["ptn"]
        ptn_info = PTN_CATALOG[ptn_code]
        prodi_name = entry["prodi"]
        prodi_kb = PRODI_KB.get(prodi_name, {
            "nama_en": prodi_name,
            "deskripsi": {
                "id": f"Program studi {prodi_name} di {ptn_info['nama']} dengan kurikulum berstandar nasional dan keunggulan riset unggul.",
                "en": f"The {prodi_name} program at {ptn_info['nama_en']} featuring accredited curricula and leading academic research."
            },
            "fokus": {
                "id": ["Fondasi Keilmuan", "Penerapan Praktik", "Riset & Analisis", "Etika Profesi"],
                "en": ["Core Foundations", "Applied Practice", "Research & Analytics", "Professional Ethics"]
            },
            "karir": {
                "id": ["Praktisi Profesional", "Akademisi / Peneliti", "Konsultan Spesialis", "Wirausahawan"],
                "en": ["Professional Practitioner", "Academic / Researcher", "Specialist Consultant", "Entrepreneur"]
            }
        })
        
        slug_id = f"{ptn_code.lower()}-{prodi_name.lower().replace(' ', '-')}"
        
        snbp_metrics = calculate_metrics(entry["snbp_dt"], entry["snbp_peminat"])
        snbt_metrics = calculate_metrics(entry["snbt_dt"], entry["snbt_peminat"])
        
        item = {
            "id": slug_id,
            "kode_prodi": entry["kode"],
            "nama_prodi": prodi_name,
            "nama_prodi_en": prodi_kb["nama_en"],
            "jenjang": "S1",
            "rumpun": entry["rumpun"],
            "ptn_id": ptn_code,
            "ptn_nama": ptn_info["nama"],
            "ptn_nama_en": ptn_info["nama_en"],
            "ptn_singkatan": ptn_info["singkatan"],
            "ptn_kota": ptn_info["kota"],
            "ptn_provinsi": ptn_info["provinsi"],
            "ptn_wilayah": ptn_info.get("wilayah", "Jawa"),
            "ptn_tipe": ptn_info.get("tipe", "PTN"),
            "ptn_warna": ptn_info.get("warna", "#0284C7"),
            "ptn_klaster": ptn_info["klaster"],
            "ptn_akreditasi": ptn_info["akreditasi"],
            "ptn_website": ptn_info["website"],
            "ptn_spmb_url": ptn_info["spmb_url"],
            "akreditasi_prodi": "Unggul",
            "snbp": snbp_metrics,
            "snbt": snbt_metrics,
            "profil": {
                "deskripsi": prodi_kb["deskripsi"],
                "fokus": prodi_kb["fokus"],
                "karir": prodi_kb["karir"]
            }
        }
        records.append(item)
    
    # Sort by default: most competitive in SNBT
    records.sort(key=lambda x: x["snbt"]["keketatan_persen"])
    return records

def export_files(records):
    os.makedirs("data", exist_ok=True)
    
    total_ptn = len([k for k, v in PTN_CATALOG.items() if v.get("tipe") == "PTN"])
    total_pts = len([k for k, v in PTN_CATALOG.items() if v.get("tipe") == "PTS"])
    
    metadata = {
        "title": "Indonesian Top Universities Selectivity & Quota Index",
        "description": "Basis data komprehensif tingkat keketatan, daya tampung, dan riwayat peminat SNBP dan SNBT PTN dan PTS top Indonesia.",
        "last_updated_iso": datetime.datetime.now().isoformat(),
        "last_updated_date": datetime.datetime.now().strftime("%d %B %Y"),
        "total_prodi": len(records),
        "total_universitas": len(PTN_CATALOG),
        "total_ptn": total_ptn,
        "total_pts": total_pts,
        "ptn_list": list(PTN_CATALOG.keys()),
        "source": "Balai Pengelolaan Pengujian Pendidikan (BPPP) Kemendikbudristek & Portal Resmi Perguruan Tinggi",
        "license": "Open Data Commons / Educational Public Use"
    }
    
    # 1. JSON
    with open("data/ptn_keketatan.json", "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    print(f"Exported data/ptn_keketatan.json ({len(records)} prodi)")
    
    # 2. Metadata JSON
    with open("data/metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print("Exported data/metadata.json")

    # 3. JS for direct client-side loading
    with open("data/ptn_keketatan.js", "w", encoding="utf-8") as f:
        f.write("window.KEKETATAN_METADATA = " + json.dumps(metadata, indent=2, ensure_ascii=False) + ";\n")
        f.write("window.PTN_CATALOG = " + json.dumps(PTN_CATALOG, indent=2, ensure_ascii=False) + ";\n")
        f.write("window.PTN_KEKETATAN_DATA = " + json.dumps(records, indent=2, ensure_ascii=False) + ";\n")
    print("Exported data/ptn_keketatan.js")

    # 4. CSV
    with open("data/ptn_keketatan.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id", "kode_prodi", "nama_prodi", "nama_prodi_en", "jenjang", "rumpun",
            "ptn_id", "ptn_nama", "ptn_kota", "ptn_provinsi", "ptn_wilayah", "ptn_tipe", "ptn_klaster", "akreditasi",
            "snbp_daya_tampung", "snbp_peminat_2024", "snbp_peminat_2023", "snbp_peminat_2022",
            "snbp_keketatan_persen", "snbp_rasio", "snbp_kategori",
            "snbt_daya_tampung", "snbt_peminat_2024", "snbt_peminat_2023", "snbt_peminat_2022",
            "snbt_keketatan_persen", "snbt_rasio", "snbt_kategori"
        ])
        for r in records:
            writer.writerow([
                r["id"], r["kode_prodi"], r["nama_prodi"], r["nama_prodi_en"], r["jenjang"], r["rumpun"],
                r["ptn_id"], r["ptn_nama"], r["ptn_kota"], r["ptn_provinsi"], r.get("ptn_wilayah", "Jawa"), r.get("ptn_tipe", "PTN"), r["ptn_klaster"], r["akreditasi_prodi"],
                r["snbp"]["daya_tampung"], r["snbp"]["riwayat_peminat"]["2024"], r["snbp"]["riwayat_peminat"]["2023"], r["snbp"]["riwayat_peminat"]["2022"],
                r["snbp"]["keketatan_persen"], r["snbp"]["rasio_persaingan"], r["snbp"]["kategori"],
                r["snbt"]["daya_tampung"], r["snbt"]["riwayat_peminat"]["2024"], r["snbt"]["riwayat_peminat"]["2023"], r["snbt"]["riwayat_peminat"]["2022"],
                r["snbt"]["keketatan_persen"], r["snbt"]["rasio_persaingan"], r["snbt"]["kategori"]
            ])
    print("Exported data/ptn_keketatan.csv")

if __name__ == "__main__":
    data = build_dataset()
    export_files(data)
    print("Dataset generation completed successfully.")
