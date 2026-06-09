
from flask_cors import CORS
from flask import Flask, request, jsonify
import pyodbc
import os
from dotenv import load_dotenv
from CRUDFUNCTIONS import create_product,create_category,list_products,list_categories,search_product,update_product,delete_product,delete_category,stock_in,stock_out,stock_log,system_log,view_system_log,view_stock_log
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
                system = system_log(cursor,"PRODUCT",results["NAME"],results["ID"],"SEARCH_PRODUCT")
                conn.commit()
            except ValueError as err:
                return jsonify({"ERROR_MESSAGE":str(err)}),404
        else:
            results = list_products(cursor)
            system = system_log(cursor,"PRODUCT",None,None,"LIST_PRODUCTS")
            conn.commit()
        return jsonify([{"MESSAGE":system},results]),200
    if request.method == "POST":
        data = request.get_json()
        try:
            product_creation = create_product(cursor,data["NAME"],data["CATEGORY"],data["PRICE"],data["STOCK"])
            system = system_log(cursor,"PRODUCT",data["NAME"],product_creation[1]["ID"],"CREATE_PRODUCT")
            conn.commit()
            return jsonify([{"MESSAGE":product_creation[0]["MESSAGE"]},{"SYSTEM_MESSAGE":system}]),201
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
            system = system_log(cursor,"PRODUCT",name,id,"UPDATE_PRODUCT")
            conn.commit()
            return jsonify([{"MESSAGE":product_update},{"SYSTEM_MESSAGE":system}]),200
        except ValueError as err:
            return jsonify({"ERROR_MESSAGE":str(err)}),400
    if request.method == "DELETE":
        try:
            system = system_log(cursor,"PRODUCT",None,id,"DELETE_PRODUCT")
            product_deletion = delete_product(cursor,id)
            conn.commit()
            return jsonify([{"MESSAGE":product_deletion},{"SYSTEM_MESSAGE":system}]),200
        except ValueError as err:
            return jsonify({"ERROR_MESSAGE":str(err)}),400



@app.route("/categories",methods=["GET","POST"])
def category_creation_and_listing():
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        category_list = list_categories(cursor)
        system = system_log(cursor,"CATEGORY",None,None,"LIST_CATEGORIES")
        conn.commit()
        return jsonify({"SYSTEM_MESSAGE":system},{"CATEGORY_LIST":category_list}),200
    if request.method == "POST":
        try:
            data = request.get_json()
            category_creation = create_category(cursor,data["NAME"])
            system = system_log(cursor,"CATEGORY",data["NAME"],category_creation[1]["CATEGORY_ID"],"CREATE_CATEGORY")
            conn.commit()
            return jsonify({"MESSAGE":category_creation[0]["MESSAGE"]},{"SYSTEM_MESSAGE":system}),201
        except ValueError as err:
            return jsonify({"ERROR_MESSAGE":str(err)}),400



@app.route("/categories/<int:id>",methods=["DELETE"])
def category_deletion(id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        system = system_log(cursor,"CATEGORY",None,id,"DELETE_CATEGORY")
        category_deletion = delete_category(cursor,id)
        conn.commit()
        return jsonify({"MESSAGE":category_deletion},{"SYSTEM_MESSAGE":system}),200
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

@app.route("/logs",methods=["GET"])
def logs():
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        stock_log = view_stock_log(cursor)
        system_log = view_system_log(cursor)
        return jsonify([{"STOCK_LOG":stock_log},{"SYSTEM_LOG":system_log}])
if __name__ == "__main__":
    app.run(debug=True)