from flask import Flask, request, jsonify
import hashlib, json, requests, os, base64
from datetime import datetime

app = Flask(__name__)
blockchain = []
BLOCKCHAIN_FILE = "blockchain_data.json"
BLOCKCHAIN_HASH_FILE = "blockchain_data.hash"

# =====================
# TARO LINK APP SCRIPT DIBAWAH INI
# =====================
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxAtYDPZl8TdQ8dyQYGyaa3vKF-PUAO_flQSHPrxmOCho4OC-L58kR8IPrMIvMOIgNeKQ/exec"

# =====================
# HASH
# =====================
def calculate_hash(block):
    temp = block.copy()
    temp.pop("current_hash", None)
    return hashlib.sha256(
        json.dumps(temp, sort_keys=True).encode()
    ).hexdigest()

# =====================
# ENCODE BLOCKCHAIN DATA
# =====================
def encode_blockchain_data(data):
    json_str = json.dumps(data, sort_keys=True)
    encoded = base64.b64encode(json_str.encode()).decode()
    data_hash = hashlib.sha256(json_str.encode()).hexdigest()
    return encoded, data_hash

# =====================
# DECODE BLOCKCHAIN DATA
# =====================
def decode_blockchain_data(encoded_data):
    try:
        json_str = base64.b64decode(encoded_data.encode()).decode()
        return json.loads(json_str), json_str
    except Exception as e:
        print(f"⚠️  Error decoding blockchain: {str(e)}")
        return None, None

# =====================
# VERIFY BLOCKCHAIN FILE INTEGRITY
# =====================
def verify_file_integrity(json_str, stored_hash):
    calculated_hash = hashlib.sha256(json_str.encode()).hexdigest()
    return calculated_hash == stored_hash

# =====================
# SAVE BLOCKCHAIN TO FILE
# =====================
def save_blockchain():
    try:
        encoded_data, data_hash = encode_blockchain_data(blockchain)

        with open(BLOCKCHAIN_FILE, 'w') as f:
            f.write(encoded_data)

        with open(BLOCKCHAIN_HASH_FILE, 'w') as f:
            f.write(data_hash)

        print(f"💾 Blockchain disimpan ke {BLOCKCHAIN_FILE} (encoded & hashed)")
    except Exception as e:
        print(f"⚠️  Error menyimpan blockchain: {str(e)}")

# =====================
# LOAD BLOCKCHAIN FROM FILE
# =====================
def load_blockchain():
    global blockchain
    if os.path.exists(BLOCKCHAIN_FILE) and os.path.exists(BLOCKCHAIN_HASH_FILE):
        try:
            with open(BLOCKCHAIN_FILE, 'r') as f:
                encoded_data = f.read()

            with open(BLOCKCHAIN_HASH_FILE, 'r') as f:
                stored_hash = f.read().strip()

            decoded_data, json_str = decode_blockchain_data(encoded_data)

            if decoded_data is None:
                print(f"⚠️  Gagal decode blockchain file")
                return False

            if not verify_file_integrity(json_str, stored_hash):
                print(f"🚨 PERINGATAN: Blockchain file telah dimodifikasi! Hash tidak cocok!")
                return False

            blockchain = decoded_data
            print(f"✅ Blockchain dimuat dari {BLOCKCHAIN_FILE} ({len(blockchain)} blok) - Integrity verified")
            return True
        except Exception as e:
            print(f"⚠️  Error memuat blockchain: {str(e)}")
            return False
    return False

# =====================
# GENESIS
# =====================
def create_genesis():
    genesis = {
        "block_id": 0,
        "student_id": "-",
        "nama_mahasiswa": "-",
        "mata_kuliah_id": "-",
        "mata_kuliah": "-",
        "jenis_mata_kuliah": "-",
        "nilai": "-",
        "semester": "-",
        "tanggal": str(datetime.now()),
        "dosen_id": "-",
        "dosen_pengampu": "-",
        "prev_hash": "0"
    }
    genesis["current_hash"] = calculate_hash(genesis)
    blockchain.append(genesis)
    save_blockchain()

if not load_blockchain():
    create_genesis()

# =====================
# SAVE TO SHEET
# =====================
def save_to_sheet(block):
    if GOOGLE_SCRIPT_URL == "LINK_APPS_SCRIPT_SPREADSHEET":
        print("⚠️  Google Sheets belum disetup - data hanya tersimpan di blockchain lokal")
        return

    print(f"📤 Mencoba kirim data ke Google Sheets...")

    try:
        response = requests.post(
            GOOGLE_SCRIPT_URL,
            json=block,
            timeout=10,
            allow_redirects=True
        )

        if response.status_code == 200:
            print(f"✅ Data berhasil dikirim ke Google Sheets")
            print(f"   Response: {response.text[:100]}")
        else:
            print(f"⚠️  Google Sheets warning - Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            print(f"   Data tetap tersimpan di blockchain lokal")

    except requests.exceptions.Timeout:
        print(f"⚠️  Timeout - Google Sheets tidak merespons dalam 10 detik")
        print(f"   Data tetap tersimpan di blockchain lokal")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Network error: {str(e)[:100]}")
        print(f"   Data tetap tersimpan di blockchain lokal")
    except Exception as e:
        print(f"⚠️  Error: {str(e)[:100]}")
        print(f"   Data tetap tersimpan di blockchain lokal")

# =====================
# ADD DATA (POST)
# =====================
@app.route("/add_data", methods=["POST"])
def add_data():
    data = request.json

    student_id = data.get("student_id")
    mata_kuliah_id = data.get("mata_kuliah_id")
    semester = data.get("semester")
    jenis_mata_kuliah = data.get("jenis_mata_kuliah")

    if not all([student_id, mata_kuliah_id, semester, jenis_mata_kuliah]):
        return jsonify({"message": "student_id, mata_kuliah_id, semester, dan jenis_mata_kuliah harus diisi"}), 400

    for block in blockchain[1:]:
        if (block["student_id"] == student_id and
            block.get("mata_kuliah_id") == mata_kuliah_id and
            block.get("jenis_mata_kuliah") == jenis_mata_kuliah and
            block["semester"] == semester):
            return jsonify({
                "message": "Data duplikat terdeteksi",
                "keterangan": f"Mahasiswa {student_id} sudah memiliki nilai {jenis_mata_kuliah} untuk mata kuliah {mata_kuliah_id} di semester {semester}"
            }), 409

    prev = blockchain[-1]

    block = {
        "block_id": len(blockchain),
        "student_id": student_id,
        "nama_mahasiswa": data["nama_mahasiswa"],
        "mata_kuliah_id": mata_kuliah_id,
        "mata_kuliah": data["mata_kuliah"],
        "jenis_mata_kuliah": jenis_mata_kuliah,
        "nilai": data["nilai"],
        "semester": semester,
        "tanggal": str(datetime.now()),
        "dosen_id": data["dosen_id"],
        "dosen_pengampu": data["dosen_pengampu"],
        "prev_hash": prev["current_hash"]
    }

    block["current_hash"] = calculate_hash(block)
    blockchain.append(block)
    save_to_sheet(block)
    save_blockchain()

    return jsonify({"message": "Data berhasil masuk blockchain"}), 201

# =====================
# GET CHAIN
# =====================
@app.route("/get_chain", methods=["GET"])
def get_chain():
    return jsonify(blockchain), 200

# =====================
# VERIFY LOCAL
# =====================
@app.route("/verify_chain", methods=["GET"])
def verify_chain():
    # Check local blockchain integrity
    for i in range(1, len(blockchain)):
        if blockchain[i]["prev_hash"] != blockchain[i-1]["current_hash"]:
            return jsonify({
                "status": "DATA TIDAK SAMA",
                "keterangan": f"Blok ke-{i} rusak"
            }), 400

        current_block = blockchain[i]

        normalized_block = {
            "block_id": current_block["block_id"],
            "dosen_id": str(current_block.get("dosen_id", "")),
            "dosen_pengampu": str(current_block.get("dosen_pengampu", "")),
            "jenis_mata_kuliah": str(current_block.get("jenis_mata_kuliah", "")),
            "mata_kuliah": str(current_block.get("mata_kuliah", "")),
            "mata_kuliah_id": str(current_block.get("mata_kuliah_id", "")),
            "nama_mahasiswa": str(current_block.get("nama_mahasiswa", "")),
            "nilai": str(current_block.get("nilai", "")),
            "prev_hash": current_block["prev_hash"],
            "semester": str(current_block.get("semester", "")),
            "student_id": str(current_block.get("student_id", "")),
            "tanggal": current_block["tanggal"]
        }

        recalculated_hash = calculate_hash(normalized_block)

        if current_block["current_hash"] != recalculated_hash:
            return jsonify({
                "status": "DATA TIDAK SAMA",
                "keterangan": f"Blok ke-{i} diubah"
            }), 400

    # Check Google Sheets tampering
    if GOOGLE_SCRIPT_URL != "LINK_APPS_SCRIPT_SPREADSHEET":
        try:
            response = requests.get(GOOGLE_SCRIPT_URL, timeout=15)
            cloud = response.json()

            for c in cloud:
                try:
                    idx = int(c["block_id"])
                except (ValueError, KeyError):
                    continue

                if idx >= len(blockchain):
                    return jsonify({
                        "status": "DATA TIDAK SAMA",
                        "keterangan": f"Blok ke-{idx} ada di Google Sheets tapi tidak ada di blockchain lokal"
                    }), 400

                local = blockchain[idx]

                cloud_block = {
                    "block_id": local["block_id"],
                    "dosen_id": str(c.get("dosen_id", "")),
                    "dosen_pengampu": str(c.get("dosen_pengampu", "")),
                    "jenis_mata_kuliah": str(c.get("jenis_mata_kuliah", "")),
                    "mata_kuliah": str(c.get("mata_kuliah", "")),
                    "mata_kuliah_id": str(c.get("mata_kuliah_id", "")),
                    "nama_mahasiswa": str(c.get("nama_mahasiswa", "")),
                    "nilai": str(c.get("nilai", "")),
                    "prev_hash": local["prev_hash"],
                    "semester": str(c.get("semester", "")),
                    "student_id": str(c.get("student_id", "")),
                    "tanggal": local["tanggal"]
                }

                recalculated_hash = calculate_hash(cloud_block)
                stored_hash = str(c.get("current_hash", ""))

                if recalculated_hash != stored_hash:
                    return jsonify({
                        "status": "DATA TIDAK SAMA",
                        "keterangan": f"Blok ke-{idx} TELAH DIMANIPULASI di Google Sheets",
                        "detail": "Data di sheet telah diubah secara manual",
                        "block_info": {
                            "student_id": cloud_block.get("student_id"),
                            "nama_mahasiswa": cloud_block.get("nama_mahasiswa"),
                            "mata_kuliah": cloud_block.get("mata_kuliah"),
                            "nilai": str(c.get("nilai", ""))
                        },
                        "hash_mismatch": {
                            "stored_hash": stored_hash,
                            "recalculated_hash": recalculated_hash
                        }
                    }), 400

                if stored_hash != local["current_hash"]:
                    return jsonify({
                        "status": "DATA TIDAK SAMA",
                        "keterangan": f"Blok ke-{idx} hash berbeda antara lokal dan cloud",
                        "detail": "Hash di Google Sheets berbeda dengan blockchain lokal",
                        "local_hash": local["current_hash"],
                        "cloud_hash": stored_hash
                    }), 400

        except Exception as e:
            return jsonify({
                "status": "ERROR",
                "keterangan": f"Tidak dapat mengakses Google Sheets: {str(e)}"
            }), 500

    return jsonify({
        "status": "DATA SAMA",
        "keterangan": "Blockchain valid"
    }), 200

# =====================
# DEBUG ENDPOINT - Check data format differences
# =====================
@app.route("/debug_cloud_data", methods=["GET"])
def debug_cloud_data():
    try:
        response = requests.get(GOOGLE_SCRIPT_URL, timeout=15)
        cloud = response.json()

        if len(cloud) > 1 and len(blockchain) > 1:
            cloud_block_1 = cloud[0] if cloud else {}
            local_block_1 = blockchain[1] if len(blockchain) > 1 else {}

            return jsonify({
                "cloud_data": cloud_block_1,
                "local_data": local_block_1,
                "comparison": {
                    "cloud_types": {k: type(v).__name__ for k, v in cloud_block_1.items()},
                    "local_types": {k: type(v).__name__ for k, v in local_block_1.items()}
                }
            }), 200

        return jsonify({"error": "Not enough data"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =====================
# DETECT CLOUD TAMPERING
# =====================
@app.route("/detect_cloud_tampering", methods=["GET"])
def detect_cloud():
    if GOOGLE_SCRIPT_URL == "LINK_APPS_SCRIPT_SPREADSHEET":
        return jsonify({
            "status": "ERROR",
            "keterangan": "Google Sheets belum disetup. Silakan setup Google Apps Script terlebih dahulu."
        }), 400

    try:
        response = requests.get(GOOGLE_SCRIPT_URL, timeout=15)
        cloud = response.json()

        for c in cloud:
            try:
                idx = int(c["block_id"])
            except (ValueError, KeyError):
                continue

            if idx >= len(blockchain):
                return jsonify({
                    "status": "DATA TIDAK SAMA",
                    "keterangan": f"Blok ke-{idx} ada di Google Sheets tapi tidak ada di blockchain lokal"
                }), 400

            local = blockchain[idx]

            cloud_block = {
                "block_id": local["block_id"],
                "dosen_id": str(c.get("dosen_id", "")),
                "dosen_pengampu": str(c.get("dosen_pengampu", "")),
                "jenis_mata_kuliah": str(c.get("jenis_mata_kuliah", "")),
                "mata_kuliah": str(c.get("mata_kuliah", "")),
                "mata_kuliah_id": str(c.get("mata_kuliah_id", "")),
                "nama_mahasiswa": str(c.get("nama_mahasiswa", "")),
                "nilai": str(c.get("nilai", "")),
                "prev_hash": local["prev_hash"],
                "semester": str(c.get("semester", "")),
                "student_id": str(c.get("student_id", "")),
                "tanggal": local["tanggal"]
            }

            recalculated_hash = calculate_hash(cloud_block)
            stored_hash = str(c.get("current_hash", ""))

            if recalculated_hash != stored_hash:
                return jsonify({
                    "status": "DATA TIDAK SAMA",
                    "keterangan": f"Blok ke-{idx} TELAH DIMANIPULASI di Google Sheets",
                    "detail": "Data di sheet telah diubah secara manual",
                    "block_info": {
                        "student_id": cloud_block.get("student_id"),
                        "nama_mahasiswa": cloud_block.get("nama_mahasiswa"),
                        "mata_kuliah": cloud_block.get("mata_kuliah"),
                        "nilai": str(c.get("nilai", ""))
                    },
                    "hash_mismatch": {
                        "stored_hash": stored_hash,
                        "recalculated_hash": recalculated_hash
                    }
                }), 400

            if stored_hash != local["current_hash"]:
                return jsonify({
                    "status": "DATA TIDAK SAMA",
                    "keterangan": f"Blok ke-{idx} hash berbeda antara lokal dan cloud",
                    "detail": "Hash di Google Sheets berbeda dengan blockchain lokal",
                    "local_hash": local["current_hash"],
                    "cloud_hash": stored_hash
                }), 400

        return jsonify({
            "status": "DATA SAMA",
            "keterangan": "Tidak ada manipulasi cloud"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "keterangan": f"Tidak dapat mengakses Google Sheets: {str(e)}"
        }), 500

# =====================
if __name__ == "__main__":
    app.run(debug=True, port=5001)
