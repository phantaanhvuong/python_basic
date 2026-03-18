import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_NAME = "products.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template("index.html", products=products)


@app.route("/create", methods=["GET", "POST"])
def create_product():
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        quantity = int(request.form["quantity"])

        conn = get_connection()
        conn.execute(
            "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)",
            (name, price, quantity)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("create.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):
    conn = get_connection()
    product = conn.execute("SELECT * FROM products WHERE id = ?", (id,)).fetchone()

    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        quantity = int(request.form["quantity"])

        conn.execute(
            "UPDATE products SET name = ?, price = ?, quantity = ? WHERE id = ?",
            (name, price, quantity, id)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    conn.close()
    return render_template("edit.html", product=product)


@app.route("/delete/<int:id>")
def delete_product(id):
    conn = get_connection()
    conn.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    create_table()
    app.run(debug=True)