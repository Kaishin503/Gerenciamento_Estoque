this project is a CRUD project where the main theme is products.
to run this CRUD, you must first create a .env file then put the following parameters:
DB_SERVER=?
DB_NAME=?
i used Microst SQL Server for this project, but you can use any other like PostGRE or MySQL, only the driver changes.
the DATABASE.txt file contains all commands i used on SQL Server to create the database tables.
run the file APP.py and then you can make requests. 
below are the requests and functionalities the program can execute:

/products: GET and POST requests are allowed, where GET allows you to access LIST PRODUCTS and SEARCH PRODUCT and POST is CREATE PRODUCT 
for the GET request: you can get either a product listing by doing /products or you can put the parameter id_or_name=?
for the POST request: you must send a JSON with the following:
"NAME","CATEGORY","PRICE","STOCK"

/products/<int:id>: PUT and DELETE requests are allowed, where PUT allows you to access UPDATE PRODUCTS and DELETE is DELETE PRODUCT
for the PUT request: you must first put a valid id on the url,, then you can send a JSON with the following (does not require all three to work): 
"NAME","CATEGORY","PRICE"
for the DELETE request, you must put a valid id on the url.

/categories: GET and POST requests are allowed, where GET allows you to access LIST CATEGORIES and POST is CREATE CATEGORY
for the GET request you can just do /categories
for the POST request you must send a JSON with the following:
"NAME"

/categories/<int:id>: DELETE request is allowed, allowing you to access DELETE CATEGORY
for that, you must put a valid category id to delete the category

/products/<int:id>/transactions: POST request is allowed, allowing you to access STOCK IN and STOCK OUT functions.
for the STOCK IN and STOCK OUT you must put either:
{"TRANSACTION":"STOCK_IN","AMOUNT":any}
or
{"TRANSACTION":"STOCK_OUT","AMOUNT":any}

/logs: GET request is allowed, allowing you to access STOCK LOG or SYSTEM LOG.
no action needed. just do GET /logs.


