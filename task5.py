from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

def connect():
    return sqlite3.connect("team.db")

con = connect()
con.execute("""
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    status TEXT
)
""")
con.commit()
con.close()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Team Availability</title>
    <style>
        body {
            font-family: Arial;
            background: #eef2f3;
            text-align: center;
            padding: 20px;
        }
        .box {
            background: white;
            padding: 20px;
            margin: auto;
            width: 80%;
            max-width: 500px;
            border-radius: 10px;
        }
        input, select, button {
            padding: 10px;
            margin: 8px;
        }
        button {
            background: blue;
            color: white;
            border: none;
            cursor: pointer;
        }
        table {
            margin: auto;
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid gray;
            padding: 10px;
        }
    </style>
</head>
<body>

<div class="box">
    <h1>Team Availability Check</h1>

    <h3>Add Team Member</h3>

    <form action="/add" method="POST">
        <input type="text" name="name"
        placeholder="Enter Member Name" required>

        <br>

        <select name="status">
            <option value="Available">Available</option>
            <option value="Not Available">Not Available</option>
        </select>

        <br>

        <button type="submit">Add Team Member</button>
    </form>

    <hr>

    <h3>Check Team Availability</h3>
    <p>Total Members: {{ total }}</p>
    <p>Available: {{ available }}</p>
    <p>Not Available: {{ unavailable }}</p>

    <hr>

    <h3>Display All Team Members</h3>

    <table>
        <tr>
            <th>Name</th>
            <th>Status</th>
            <th>Update Status</th>
        </tr>

        {% for member in members %}
        <tr>
            <td>{{ member[1] }}</td>
            <td>{{ member[2] }}</td>
            <td>
                <form action="/update/{{ member[0] }}" method="POST">
                    <select name="status">
                        <option value="Available">Available</option>
                        <option value="Not Available">Not Available</option>
                    </select>
                    <button type="submit">Update</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </table>

</div>
</body>
</html>
"""

@app.route("/")
def home():
    con = connect()

    members = con.execute(
        "SELECT * FROM members"
    ).fetchall()

    total = len(members)

    available = con.execute(
        "SELECT COUNT(*) FROM members WHERE status='Available'"
    ).fetchone()[0]

    unavailable = con.execute(
        "SELECT COUNT(*) FROM members WHERE status='Not Available'"
    ).fetchone()[0]

    con.close()

    return render_template_string(
        html,
        members=members,
        total=total,
        available=available,
        unavailable=unavailable
    )

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    status = request.form["status"]

    con = connect()
    con.execute(
        "INSERT INTO members (name, status) VALUES (?, ?)",
        (name, status)
    )
    con.commit()
    con.close()

    return redirect("/")

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    status = request.form["status"]

    con = connect()
    con.execute(
        "UPDATE members SET status=? WHERE id=?",
        (status, id)
    )
    con.commit()
    con.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5002)