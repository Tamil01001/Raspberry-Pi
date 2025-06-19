from flask import Flask, render_template, send_from_directory, request
import sqlite3
import os

app = Flask(__name__)

# Get base directory where app.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Point to the logs/ directory outside flask_admin/
DB_PATH = os.path.join(BASE_DIR, "..", "logs", "plates.db")
SNAP_DIR = os.path.join(BASE_DIR, "..", "logs", "snaps")

@app.route("/", methods=["GET", "POST"])
def index():
    search_query = request.form.get("search") if request.method == "POST" else None

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if search_query:
        cur.execute("SELECT plate, timestamp, confidence, image_path FROM plate_logs WHERE plate LIKE ? ORDER BY id DESC",
                    ('%' + search_query + '%',))
    else:
        cur.execute("SELECT plate, timestamp, confidence, image_path FROM plate_logs ORDER BY id DESC")

    records = cur.fetchall()
    conn.close()

    no_results = search_query and len(records) == 0

    return render_template("dashboard.html", records=records, search_query=search_query, no_results=no_results)

@app.route("/logs/snaps/<filename>")
def send_snapshot(filename):
    return send_from_directory(SNAP_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
