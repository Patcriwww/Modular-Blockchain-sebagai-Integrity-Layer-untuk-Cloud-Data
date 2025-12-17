from flask import Flask, request, jsonify
import hashlib, json, requests
from datetime import datetime

app = Flask(__name__)
blockchain = []

# =====================
# TARO LINK APP SCRIPT DIBAWAH INI
# =====================
GOOGLE_SCRIPT_URL = "LINK_APPS_SCRIPT_SPREADSHEET"

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
# GENESIS
# =====================
def create_genesis():
    genesis = {
        "block_id": 0,
        "student_id": "-",
        "nama_mahasiswa": "-",
        "mata_kuliah": "-",
        "nilai": "-",
        "semester": "-",
        "tanggal": str(datetime.now()),
        "dosen_pengampu": "-",
        "prev_hash": "0"
    }
    genesis["current_hash"] = calculate_hash(genesis)
    blockchain.append(genesis)

create_genesis()

# =====================
# SAVE TO SHEET
# =====================
def save_to_sheet(block):
    requests.post(GOOGLE_SCRIPT_URL, json=block)

# =====================
# ADD DATA (POST)
# =====================
@app.route("/add_data", methods=["POST"])
def add_data():
    data = request.json
    prev = blockchain[-1]

    block = {
        "block_id": len(blockchain),
        "student_id": data["student_id"],
        "nama_mahasiswa": data["nama_mahasiswa"],
        "mata_kuliah": data["mata_kuliah"],
        "nilai": data["nilai"],
        "semester": data["semester"],
        "tanggal": str(datetime.now()),
        "dosen_pengampu": data["dosen_pengampu"],
        "prev_hash": prev["current_hash"]
    }

    block["current_hash"] = calculate_hash(block)
    blockchain.append(block)
    save_to_sheet(block)

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
    for i in range(1, len(blockchain)):
        if blockchain[i]["prev_hash"] != blockchain[i-1]["current_hash"]:
            return jsonify({
                "status": "DATA TIDAK SAMA",
                "keterangan": f"Blok ke-{i} rusak"
            }), 400

        if blockchain[i]["current_hash"] != calculate_hash(blockchain[i]):
            return jsonify({
                "status": "DATA TIDAK SAMA",
                "keterangan": f"Blok ke-{i} diubah"
            }), 400

    return jsonify({
        "status": "DATA SAMA",
        "keterangan": "Blockchain valid"
    }), 200

# =====================
# DETECT CLOUD TAMPERING
# =====================
@app.route("/detect_cloud_tampering", methods=["GET"])
def detect_cloud():
    cloud = requests.get(GOOGLE_SCRIPT_URL).json()

    for c in cloud:
        idx = int(c["block_id"])
        local = blockchain[idx]

        recalculated = calculate_hash(c)

        if recalculated != local["current_hash"]:
            return jsonify({
                "status": "DATA TIDAK SAMA",
                "keterangan": f"Blok ke-{idx} TELAH DIMANIPULASI di Google Sheets"
            }), 400

    return jsonify({
        "status": "DATA SAMA",
        "keterangan": "Tidak ada manipulasi cloud"
    }), 200

# =====================
if __name__ == "__main__":
    app.run(debug=True)

