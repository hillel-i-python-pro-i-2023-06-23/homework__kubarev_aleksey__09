from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

from application.services.generate_message import generate_message
from application.services.generate_users import generate_users

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/hi/<name>/<int:age>")
@app.route("/hi/<name>")
@app.route("/hi")
def hi(name: str = "Lucy", age: int = 42):
    return generate_message(name=name, age=age)


@app.route("/hello")
@use_args({"name": fields.Str(missing="Bob"), "age": fields.Int(missing=20)}, location="query")
def hello(args):
    name = args["name"]
    age = args["age"]

    return generate_message(name=name, age=age)


@app.route("/users/generate")
@use_args({"amount": fields.Int(missing=10)}, location="query")
def users_generate(args):
    # [handle_input]-[BEGIN]
    amount = args["amount"]
    # [handle_input]-[END]

    # [handle_logic]-[BEGIN]
    users = generate_users(amount=amount)
    # [handle_logic]-[END]

    # [handle_output]-[BEGIN]
    users_formatted = []
    for user in users:
        user_formatted = f"<li><b>{user.username}</b> - <span>{user.email}</span> - <span>{user.age}</span></li>"
        users_formatted.append(user_formatted)
    _temp = "\n".join(users_formatted)
    return f"<ol>{_temp}</ol>"
    # [handle_output]-[END]


# HTML tags

# div
# p
# span

# ul
# ol
# li

# hr

# br

# a

# form
# input
# button

# h1, h2, h3, h4, h5, h6


if __name__ == "__main__":
    app.run()
