from flask import Flask, Response
from webargs import fields
from webargs.flaskparser import use_args

from application.services.create_table import create_table
from application.services.db_connection import DBConnection


app = Flask(__name__)


@app.route("/")
def welcome():
    return "Homework #9 (Kubarev Aleksey)"


@app.route("/users/create")
@use_args({"name": fields.Str(reuired=True), "number": fields.Str(required=True)}, location="query")
def users__create(args):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "INSERT INTO users (contact_name, phone_value) VALUES (:name, :number);",
                {"name": args["name"], "number": args["number"]},
            )

    return "Ok!"


@app.route("/users/read-all")
def users__read_all():
    with DBConnection() as connection:
        with connection:
            users = connection.execute("SELECT * FROM users;").fetchall()

    return "<br>".join([f'{user["phone_id"]}: {user["contact_name"]} - {user["phone_value"]}' for user in users])


@app.route("/users/read/<int:phone_id>")
def user__read(phone_id: int):
    with DBConnection() as connection:
        user = connection.execute(
            "SELECT * FROM users WHERE (phone_id = :phone_id);",
            {
                "phone_id": phone_id,
            },
        ).fetchone()

    return f'{user["phone_id"]}: {user["contact_name"]} - {user["phone_value"]}'


@app.route("/users/update/<int:phone_id>")
@use_args({"name": fields.Str(), "number": fields.Str()}, location="query")
def users__update(
    args,
    phone_id: int,
):
    with DBConnection() as connection:
        with connection:
            name = args.get("name")
            number = args.get("number")
            if name is None and number is None:
                return Response(
                    "Please provide at least one argument",
                    status=400,
                )
            args_for_request = []
            if name is not None:
                args_for_request.append("contact_name=:contact_name")
            if number is not None:
                args_for_request.append("phone_value=:phone_value")
            args_2 = ", ".join(args_for_request)
            connection.execute(
                "UPDATE users " f"SET {args_2}" " WHERE (phone_id = :phone_id);",
                {
                    "phone_id": phone_id,
                    "contact_name": name,
                    "phone_value": number,
                },
            )

    return "Ok!"


@app.route("/users/delete/<int:phone_id>")
def user__delete(phone_id: int):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "DELETE " "FROM users " "WHERE (phone_id = :phone_id);",
                {
                    "phone_id": phone_id,
                },
            )

    return "Ok!"


create_table()
