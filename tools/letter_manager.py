import os
import sys
import json
import csv
import math
import argparse
import urllib.request
import urllib.error
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
REGISTRY_JSON_PATH = os.path.join(SCRIPT_DIR, "surat_registry.json")
REGISTRY_CSV_PATH = os.path.join(BASE_DIR, "00_STANDAR_DAN_REGULASI", "REGISTER_NOMOR_SURAT.csv")

EMBEDDING_URL = "http://127.0.0.1:1234/v1/embeddings"
RERANK_URL = "http://127.0.0.1:8080/v1/rerank"

ROMAN_MONTHS = {
    1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI",
    7: "VII", 8: "VIII", 9: "IX", 10: "X", 11: "XI", 12: "XII"
}

PRODUCT_CONFIG = {
    "GREN": {
        "nama": "GREN Propertykost Jatinangor",
        "entitas": "KAB",
        "folder": "01_GREN_PROPERTYKOST",
        "deskripsi": "Rukost tapak kost eksklusif mahasiswa Jatinangor Unpad ITB investasi yield passive income Kenzo Anatha Bumi surat open table sewa kamar promo survey",
        "subfolders": {
            "01_Surat_Keluar": "surat keluar permohonan open table penawaran kerjasama tenant",
            "02_Surat_Masuk": "surat masuk balasan dari dinas instansi pengelola gedung",
            "03_Internal_Office_Memo_IOM": "internal memo promo survey voucher kebijakan marketing tim sales",
            "04_Perizinan_Dan_Legalitas": "dokumen PBG SHM izin lingkungan sertifikat",
            "05_Administrasi_Konsumen": "surat konfirmasi unit pesanan SKUP surat pemesanan form konsumen kwitansi",
            "06_SPK_Dan_Kontrak": "surat perjanjian kerja kontraktor arsitek interior vendor"
        }
    },
    "HJA": {
        "nama": "Hunian Asri Jatihandap",
        "entitas": "SAB",
        "folder": "02_HUNIAN_ASRI_JATIHANDAP",
        "deskripsi": "Perumahan tapak rumah subsidi komersial kavling siap bangun Jatihandap Cimenyan Bandung Siliwangi Anatha Bumi Yanproland ukur tanah siteplan",
        "subfolders": {
            "01_Surat_Keluar": "surat keluar koordinasi BPN desa perbankan mitra sales",
            "02_Surat_Masuk": "surat masuk warga instansi pemerintah daerah kontraktor",
            "03_Internal_Office_Memo_IOM": "internal memo operasional lapangan promo sales kavling",
            "04_Pertanahan_Dan_Perizinan": "berita acara ukur tanah izin kavling SHM perumahan",
            "05_Administrasi_Konsumen": "surat pesanan kavling SKUP pembayaran kwitansi konsumen",
            "06_SPK_Dan_Kontrak": "SPK pembangunan unit cut and fill infrastruktur jalan"
        }
    },
    "EK": {
        "nama": "Emeralda Kertajati",
        "entitas": "SAB",
        "folder": "03_EMERALDA_KERTAJATI",
        "deskripsi": "Aset tanah lahan kavling aerocity BIJB bandara internasional Jawa Barat Kertajati Majalengka 20 AJB akta jual beli investasi tanah",
        "subfolders": {
            "01_Surat_Keluar": "surat penawaran investor permohonan ke dinas pemkab Majalengka",
            "02_Surat_Masuk": "surat masuk calon investor BPN Majalengka desa Kertajati",
            "03_Internal_Office_Memo_IOM": "memo appraisal nilai aset tanah evaluasi kerjasama",
            "04_Pertanahan_Dan_AJB": "akta jual beli warkah tanah surat riwayat tanah 20 AJB",
            "05_Penawaran_Investor": "proposal penawaran lahan aerocity letter of intent MOU",
            "06_SPK_Dan_Legalitas": "SPK notaris PPAT appraisal jasa hukum perizinan"
        }
    },
    "TER": {
        "nama": "The Emeralda Resort & Kingston Park",
        "entitas": "SAB",
        "folder": "04_THE_EMERALDA_RESORT_KINGSTON_PARK",
        "deskripsi": "Resort villa hillside Padalarang Bandung Barat klaster Kingston Park Beryl Janet Royal Park masterplan mediasi sengketa lahan luxury",
        "subfolders": {
            "01_Surat_Keluar": "surat koordinasi masterplan perizinan korespondensi holding",
            "02_Surat_Masuk": "surat masuk konsultan arsitektur investor dinas",
            "03_Internal_Office_Memo_IOM": "memo perkembangan klaster kebijakan teknis arahan direksi",
            "04_Mediasi_Dan_Legalitas": "dokumen mediasi formal sengketa lahan akta perdamaian legal",
            "05_Klaster_Kingston_Park": "surat brand strategy materi arsitektur Kingston Park",
            "06_SPK_Perencanaan_Dan_Masterplan": "SPK konsultan masterplan lansekap perencana kawasan"
        }
    },
    "FNA": {
        "nama": "Freelance Nugi AI Studio",
        "entitas": "NAI",
        "folder": "05_FREELANCE_NUGI_AI_STUDIO",
        "deskripsi": "Jasa software engineer fullstack AI automation agent serverless RAG bot development rate card proposal retainer invoice NDA konsultasi tech",
        "subfolders": {
            "01_Surat_Keluar": "surat pengantar invoice rilis software serah terima sistem",
            "02_Surat_Masuk": "purchase order dari klien feedback teknis brief proyek",
            "03_Proposal_Dan_Penawaran": "proposal jasa software AI RAG automation rate card quote",
            "04_SPK_Dan_Service_Agreement": "kontrak kerja freelance retainer agreement SLA",
            "05_NDA_Dan_Kerahasiaan": "non disclosure agreement perlindungan kerahasiaan data",
            "06_Invoice_Dan_Kwitansi": "invoice termin down payment tagihan pembayaran bukti transfer"
        }
    },
    "WIFI": {
        "nama": "Mora Republic WIFI / Uswah Cell",
        "entitas": "MR",
        "folder": "06_MORA_REPUBLIC_WIFI_USWAH",
        "deskripsi": "Penyedia internet RT RW net voucher wifi router kuota bandwidth izin kabel tiang instalasi formulir pendaftaran pelanggan teknisi Uswah",
        "subfolders": {
            "01_Surat_Keluar": "surat izin tarik kabel fiber optik pasang tiang ke RT RW lurah",
            "02_Surat_Masuk": "surat balasan warga izin penarikan kabel tagihan upstream",
            "03_Formulir_Berlangganan_Instalasi": "form pasang baru internet survei lokasi berita acara pasang",
            "04_Kerjasama_Vendor_ISP": "kontrak kerjasama bandwidth sewa tiang ISP upstream",
            "05_Tanda_Terima_Perangkat": "tanda terima modem router ONT mutasi perangkat retur"
        }
    },
    "CORP": {
        "nama": "Yanproland Holding & Corporate",
        "entitas": "YPL",
        "folder": "07_CORPORATE_YANPROLAND_HOLDING",
        "deskripsi": "Tata kelola holding surat keputusan SK direksi surat tugas surat kuasa pengajuan anggaran markom sales legalitas akta perusahaan",
        "subfolders": {
            "01_Surat_Keputusan_Direksi_SK": "surat keputusan SK pengangkatan jabatan struktur organisasi SOP",
            "02_Surat_Tugas_Dan_Kuasa": "surat tugas perjalanan dinas surat kuasa penunjukan",
            "03_Internal_Office_Memo_Holding": "pengajuan anggaran holding markom sales lintas unit bisnis",
            "04_Legalitas_Holding": "akta pendirian holding NIB NPWP perizinan berusaha OSS"
        }
    }
}

def get_embedding(text, model="text-embedding-nomic-embed-text-v1.5"):
    try:
        req = urllib.request.Request(
            EMBEDDING_URL,
            data=json.dumps({"input": text, "model": model}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
            return data['data'][0]['embedding']
    except Exception as e:
        # Try fallback model if first fails
        if model != "text-embedding-qwen3-embedding-4b":
            try:
                return get_embedding(text, model="text-embedding-qwen3-embedding-4b")
            except Exception:
                pass
        raise RuntimeError(f"Gagal memanggil endpoint embedding di {EMBEDDING_URL}: {e}")

def cosine_similarity(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)

def try_rerank(query, documents):
    try:
        req = urllib.request.Request(
            RERANK_URL,
            data=json.dumps({"query": query, "documents": documents}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            return data
    except Exception:
        return None

def load_registry():
    if os.path.exists(REGISTRY_JSON_PATH):
        with open(REGISTRY_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": "1.0.0", "updated_at": "", "counters": {}, "letters": []}

def save_registry(data):
    data["updated_at"] = datetime.now().isoformat()
    with open(REGISTRY_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def append_csv(record):
    file_exists = os.path.exists(REGISTRY_CSV_PATH)
    fieldnames = [
        "no_registrasi", "nomor_surat", "tanggal", "entitas", "produk", "divisi",
        "jenis_surat", "perihal", "tujuan_penerima", "pembuat", "status", "lokasi_arsip"
    ]
    with open(REGISTRY_CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(record)

def classify_text(text):
    print(f"\n[*] Menganalisis teks menggunakan model embedding: {EMBEDDING_URL}...")
    doc_emb = get_embedding(text)
    
    # 1. Product scoring
    prod_scores = []
    for code, cfg in PRODUCT_CONFIG.items():
        p_emb = get_embedding(cfg["deskripsi"])
        sim = cosine_similarity(doc_emb, p_emb)
        prod_scores.append((code, sim, cfg))
    prod_scores.sort(key=lambda x: x[1], reverse=True)
    
    best_prod_code, best_prod_sim, best_prod_cfg = prod_scores[0]
    
    # 2. Subfolder scoring within best product
    sub_scores = []
    for sub, desc in best_prod_cfg["subfolders"].items():
        s_emb = get_embedding(desc)
        sim = cosine_similarity(doc_emb, s_emb)
        sub_scores.append((sub, sim))
    sub_scores.sort(key=lambda x: x[1], reverse=True)
    best_subfolder, best_sub_sim = sub_scores[0]
    
    # 3. Check reranker if available
    candidates = [f"{cfg['nama']} ({code}) - {cfg['folder']}" for code, _, cfg in prod_scores[:3]]
    rerank_res = try_rerank(text, candidates)
    rerank_status = "Aktif (Port 8080)" if rerank_res else "Fallback (Cosine Similarity Embedding)"

    print("\n" + "=" * 65)
    print("           HASIL KLASIFIKASI SEMANTIK SURAT (AI)           ")
    print("=" * 65)
    print(f"Reranker Engine      : {rerank_status}")
    print(f"Teks Input           : \"{text}\"")
    print(f"Produk Terdeteksi    : {best_prod_cfg['nama']} [{best_prod_code}]")
    print(f"Entitas Legal        : {best_prod_cfg['entitas']}")
    print(f"Confidence Score     : {best_prod_sim:.4f}")
    print(f"Rekomendasi Folder   : {best_prod_cfg['folder']}/{best_subfolder}/")
    print("-" * 65)
    print("Alternatif Terdekat:")
    for code, score, cfg in prod_scores[1:3]:
        print(f" - {cfg['nama']} [{code}]: {score:.4f}")
    print("=" * 65 + "\n")
    
    return {
        "produk": best_prod_code,
        "entitas": best_prod_cfg['entitas'],
        "folder": os.path.join(best_prod_cfg['folder'], best_subfolder)
    }

def issue_letter_number(prod, div, title, recipient, maker=None, date_str=None, jenis="SURAT"):
    prod = prod.upper()
    div = div.upper()
    
    if prod not in PRODUCT_CONFIG:
        print(f"[!] Error: Kode produk '{prod}' tidak valid. Pilihan: {list(PRODUCT_CONFIG.keys())}")
        return
        
    cfg = PRODUCT_CONFIG[prod]
    entitas = cfg["entitas"]
    
    dt = datetime.strptime(date_str, "%Y-%m-%d") if date_str else datetime.now()
    year_str = str(dt.year)
    month_roman = ROMAN_MONTHS[dt.month]
    date_formatted = dt.strftime("%Y-%m-%d")
    
    reg_data = load_registry()
    if "counters" not in reg_data:
        reg_data["counters"] = {}
    if year_str not in reg_data["counters"]:
        reg_data["counters"][year_str] = {}
    if prod not in reg_data["counters"][year_str]:
        reg_data["counters"][year_str][prod] = {}
    if div not in reg_data["counters"][year_str][prod]:
        reg_data["counters"][year_str][prod][div] = 0
        
    next_seq = reg_data["counters"][year_str][prod][div] + 1
    seq_str = f"{next_seq:03d}"
    
    # Standard format: [No]/[DIV]/[ENTITAS]/[PRODUK]/[ROMAWI]/[TAHUN]
    letter_no = f"{seq_str}/{div}/{entitas}/{prod}/{month_roman}/{year_str}"
    reg_id = f"REG-{year_str}-{len(reg_data.get('letters', [])) + 1:04d}"
    
    # Expected file path hint
    clean_title = "".join(c if c.isalnum() else "_" for c in title).strip("_")
    suggested_filename = f"{seq_str}_{div}_{entitas}_{prod}_{month_roman}_{year_str}_{clean_title[:40]}.docx"
    suggested_folder = os.path.join(cfg["folder"], "01_Surat_Keluar")
    full_path_hint = f"{suggested_folder}/{suggested_filename}"
    
    new_record = {
        "no_registrasi": reg_id,
        "nomor_surat": letter_no,
        "tanggal": date_formatted,
        "entitas": entitas,
        "produk": prod,
        "divisi": div,
        "jenis_surat": jenis.upper(),
        "perihal": title,
        "tujuan_penerima": recipient,
        "pembuat": maker or f"Divisi {div}",
        "status": "DITERBITKAN",
        "lokasi_arsip": full_path_hint
    }
    
    # Commit changes
    reg_data["counters"][year_str][prod][div] = next_seq
    reg_data["letters"].append(new_record)
    save_registry(reg_data)
    append_csv(new_record)
    
    print("\n" + "=" * 65)
    print("         NOMOR SURAT RESMI BERHASIL DITERBITKAN!           ")
    print("=" * 65)
    print(f"Nomor Surat Resmi    :  {letter_no}")
    print(f"No. Registrasi       :  {reg_id}")
    print(f"Tanggal Penerbitan   :  {date_formatted}")
    print(f"Entitas / Perusahaan :  {entitas} ({cfg['nama']})")
    print(f"Divisi               :  {div}")
    print(f"Perihal              :  {title}")
    print(f"Kepada Yth           :  {recipient}")
    print("-" * 65)
    print(f"Saran Nama File      :  {suggested_filename}")
    print(f"Folder Penyimpanan   :  {suggested_folder}/")
    print("=" * 65 + "\n")
    return letter_no

def list_letters(limit=15):
    reg_data = load_registry()
    letters = reg_data.get("letters", [])
    if not letters:
        print("[i] Belum ada surat yang terdaftar.")
        return
        
    print("\n" + "=" * 110)
    print(f"                      DAFTAR ARSIP SURAT TERDAFTAR (Total: {len(letters)} Dokumen)                       ")
    print("=" * 110)
    print(f"{'No':<4} | {'Nomor Surat':<28} | {'Tanggal':<10} | {'Produk':<6} | {'Penerima':<25} | {'Perihal':<30}")
    print("-" * 110)
    for i, item in enumerate(letters[-limit:], 1):
        penerima = (item.get('tujuan_penerima') or '')[:24]
        perihal = (item.get('perihal') or '')[:29]
        print(f"{i:<4} | {item['nomor_surat']:<28} | {item['tanggal']:<10} | {item['produk']:<6} | {penerima:<25} | {perihal:<30}")
    print("=" * 110 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Letter Manager AI Assistant untuk Kumpulan-surat")
    subparsers = parser.add_subparsers(dest="command", help="Perintah yang tersedia")
    
    # Classify
    p_classify = subparsers.add_parser("classify", help="Klasifikasikan teks/surat ke produk & subfolder yang tepat")
    p_classify.add_argument("text", type=str, help="Perihal atau ringkasan isi surat")
    
    # Issue
    p_issue = subparsers.add_parser("issue", help="Terbitkan nomor surat baru (anti-duplikat)")
    p_issue.add_argument("--product", required=True, choices=list(PRODUCT_CONFIG.keys()), help="Kode produk")
    p_issue.add_argument("--div", required=True, help="Kode divisi (MKT, SLS, DIR, LEG, FIN, OPS, ENG, GA)")
    p_issue.add_argument("--title", required=True, help="Perihal surat")
    p_issue.add_argument("--recipient", required=True, help="Nama pihak tujuan / penerima surat")
    p_issue.add_argument("--maker", default=None, help="Nama pembuat surat / pengirim")
    p_issue.add_argument("--date", default=None, help="Tanggal surat YYYY-MM-DD (default hari ini)")
    p_issue.add_argument("--type", default="SURAT", help="Jenis surat (SURAT, IOM, SPK, SKUP, SK)")
    
    # List
    subparsers.add_parser("list", help="Tampilkan daftar surat yang terdaftar di sistem")
    
    args = parser.parse_args()
    
    if args.command == "classify":
        classify_text(args.text)
    elif args.command == "issue":
        issue_letter_number(
            prod=args.product,
            div=args.div,
            title=args.title,
            recipient=args.recipient,
            maker=args.maker,
            date_str=args.date,
            jenis=args.type
        )
    elif args.command == "list":
        list_letters()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
