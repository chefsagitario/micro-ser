from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# DATABASE_URL environment variable varsa onu kullan, yoksa local fallback
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://alparslan:OYs9KYMfMZkk7EdC9Q6TiHQssPsH8U5J@dpg-d6t8qvvpm1nc739dp4t0-a.oregon-postgres.render.com/hello_cloud2_db_sy3b"
)

def connect_db():
    return psycopg2.connect(DATABASE_URL)

# Bu route hem GET hem POST
@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = connect_db()
    cur = conn.cursor()
    
    # Tablo sadece bir kere yaratılır
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ziyaretciler (
            id SERIAL PRIMARY KEY,
            isim TEXT
        )
    """)
    
    # POST ile isim ekleme
    if request.method == "POST":
        isim = request.json.get("isim")
        if isim:
            cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))
            conn.commit()
    
    # Son 10 ismi getir
    cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")
    isimler = [row[0] for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    return jsonify(isimler)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
