from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route("/users")
def index():
    mysql = connectToMySQL("user_db")
    users = mysql.query_db("SELECT * FROM users;")
    print(users)
    return render_template("index.html", all_users = users)

@app.route("/users/new/process", methods=["POST"])
def new_user():
    mysql = connectToMySQL("user_db")
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, NOW(), NOW());"
    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "em": request.form["email"]
    }
    id = mysql.query_db(query, data)
    return redirect("/users/" + str(id))

@app.route("/users/new")
def display():
    return render_template("adduser.html")

@app.route("/users/<id>")
def display_user(id):
    mysql = connectToMySQL("user_db")
    id = int(id)
    query = mysql.query_db(f"SELECT * FROM users WHERE users.id = {id};")
    return render_template("displayuser.html", user=query)

@app.route("/users/<id>/edit")
def show_edit_user(id):
    mysql = connectToMySQL("user_db")
    id = int(id)
    query = mysql.query_db(f"SELECT * FROM users WHERE users.id = {id};")
    return render_template("edituser.html", user=query)

@app.route("/users/<id>/update", methods=["POST"])
def edit_user(id):
    mysql = connectToMySQL("user_db")
    query = "UPDATE users SET first_name = %(fn)s, last_name = %(ln)s, email=%(em)s, updated_at = NOW() WHERE id=%(id)s;"
    data = {
        "fn": request.form['fname'],
        "ln": request.form['lname'],
        "em": request.form['email'],
        "id": id
    }
    mysql.query_db(query, data)
    return redirect("/users/"+id)

@app.route("/users/<id>/destroy")
def destroy(id):
    mysql = connectToMySQL("user_db")
    id = int(id)
    mysql.query_db(f"DELETE FROM users WHERE users.id = {id};")
    return redirect("/users")


if __name__ == "__main__":
    app.run(debug=True)