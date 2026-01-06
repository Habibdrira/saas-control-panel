
@app.route("/api/resolve", methods=["POST"])
def resolve():
    username = request.json["username"]
    conn = sqlite3.connect(USERS_DB)
    cur = conn.execute(
        "SELECT container_port FROM users WHERE username=?",
        (username,)
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "user not found"}), 404

    return jsonify({
        "url": f"http://localhost:{row[0]}"
    })
