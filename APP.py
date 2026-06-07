
from flask_cors import CORS
from flask import Flask, request, jsonify
import pyodbc
import os
from dotenv import load_dotenv
from CRUDFUNCTIONS import create_product,create_category,list_products,list_categories,search_product,update_product,delete_product,delete_category,stock_in,stock_out,stock_log
load_dotenv()

def get_connection():
    return pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={os.getenv('DB_SERVER')};"
    f"DATABASE={os.getenv('DB_NAME')};"
    "Trusted_Connection=yes;")



app = Flask(__name__)
CORS(app)


@app.route("/products",methods=["GET","POST"])
def product_search_list_and_create():
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        id_or_name = request.args.get("id_or_name")
        if id_or_name:
            try:
                results = search_product(cursor,id_or_name)
            except ValueError as err:
                return jsonify({"ERROR_MESSAGE":str(err)}),404
        else:
            results = list_products(cursor)
        return jsonify(results),200
    if request.method == "POST":
        data = request.get_json()
        try:
            product_creation = create_product(cursor,data["NAME"],data["CATEGORY"],data["PRICE"],data["STOCK"])
            conn.commit()
            return jsonify({"MESSAGE":product_creation}),201
        except ValueError as err:
            return jsonify({"ERROR_MESSAGE":str(err)}),400



@app.route("/products/<int:id>",methods=["PUT","DELETE"])
def product_update_and_delete(id):
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == "PUT":

        data = request.get_json()
        try:
            name = data.get("NAME")
            category = data.get("CATEGORY")
            price = data.get("PRICE")
            product_update = update_product(cursor,id,name=name,category=category,price=price)
            conn.commit()
            return jsonify({"MESSAGE":product_update}),200
        except ValueError as err:
            return jsonify({"ERROR_MESSAGE":str(err)}),400
    if request.method == "DELETE":
        try:
            product_deletion = delete_product(cursor,id)
            conn.commit()
            return jsonify({"MESSAGE":product_deletion}),200
        except ValueError as err:
            return jsonify({"ERROR_MESSAGE":str(err)}),400



@app.route("/categories",methods=["GET","POST"])
def category_creation_and_deletion():
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        category_list = list_categories(cursor)
        return jsonify(category_list)
    if request.methods == "POST":
        try:
            dados = request.get_json()
            category_creation = create_category(cursor,dados["NAME"])
            conn.commit()
            return jsonify({"MESSAGE":category_creation}),201
        except ValueError as err:
            return jsonify({"ERROR_MESSAGE":str(err)}),400



@app.route("/categories/<int:id>",methods=["DELETE"])
def category_deletion(id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        category_deletion = delete_category(cursor,id)
        conn.commit()
        return jsonify({"MESSAGE":category_deletion}),200
    except ValueError as err:
        return jsonify({"ERROR_MESSAGE":str(err)}),400

@app.route("/products/<int:id>/transactions",methods=["PUT"]) 
def transactions(id):
    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()
    type = data.get("TRANSACTION")
    if type == "stock_in":
        amount = data.get("AMOUNT")
        try:
            transaction = stock_in(cursor,id,amount)
            log_transaction = stock_log(cursor,id,amount,type)
            conn.commit()
            return jsonify([{"MESSAGE":transaction},{"MESSAGE":log_transaction}]),200
        except ValueError as err:
            return jsonify({"ERROR_MESSAGE":str(err)}),400
    if type == "stock_out":
        amount = data.get("AMOUNT")
        try:
            transaction = stock_out(cursor,id,amount)
            log_transaction = stock_log(cursor,id,amount,type)
            conn.commit()
            return jsonify([{"MESSAGE":transaction},{"MESSAGE":log_transaction}]),200
        except ValueError as err:
            return jsonify({"ERROR_MESSAGE":str(err)}),400

if __name__ == "__main__":
    app.run(debug=True)