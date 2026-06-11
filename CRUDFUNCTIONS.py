import pyodbc
def create_product(cursor,name,category,price,stock):
    product_name_validation = cursor.execute("SELECT ProductName FROM Products WHERE ProductName = ?",(name,))
    results = product_name_validation.fetchone()
    if results is not None:
        raise ValueError(f"PRODUCT {results[0]} ALREADY EXISTS")
    category_validation = cursor.execute("SELECT CategoryPK FROM ProductCategory WHERE CategoryName = ?",(category,))
    results = category_validation.fetchone()
    if results is None:
        raise ValueError("CATEGORY NOT FOUND")
    else:
        categoryFK = results[0]
    if price <= 0:
        raise ValueError("PRICE CANNOT BE LESS THAN/EQUAL TO 0")
    if stock <= 0:
        raise ValueError("STOCK CANNOT BE LESS THAN/EQUAL TO 0")
    name = name.upper()
    cursor.execute("INSERT INTO Products (ProductName,CategoryFK,ProductPrice,ProductStock) VALUES (?,?,?,?)",(name,categoryFK,price,stock))
    search = cursor.execute("SELECT ProductPK FROM Products WHERE ProductName = ?",(name,))
    fetch = search.fetchone()
    return [{"MESSAGE":"PRODUCT SUCCESSFULLY CREATED "},{"ID":fetch[0]}]
    
    

def create_category(cursor,category_name):
    category_validation = cursor.execute("SELECT CategoryPK FROM ProductCategory WHERE CategoryName = ?",(category_name,))
    fetch = category_validation.fetchone()
    if fetch is not None:
        raise ValueError("CATEGORY ALREADY EXISTS")
    else:
        category_name = category_name.upper()
        cursor.execute("INSERT INTO ProductCategory (CategoryName) VALUES (?)",(category_name,))
        search = cursor.execute("SELECT CategoryPK FROM ProductCategory WHERE CategoryName = ?",(category_name,))
        fetch = search.fetchone()
        category_id = fetch[0]
        return ([{"MESSAGE":f"CREATED CATEGORY {category_name}"},{"CATEGORY_ID":category_id}])


         
def list_products(cursor):
    products = cursor.execute("SELECT * FROM Products")
    fetch = products.fetchall()
    product_list = []
    for item in fetch:
        id,name,categoryFK,price,stock = item
        category = cursor.execute("SELECT CategoryName FROM ProductCategory WHERE CategoryPK = ?",(categoryFK,))
        fetch2 = category.fetchone()
        category_name = fetch2[0]
        product_list.append({"ID":id,"NAME":name,"CATEGORY_NAME":category_name,"CATEGORY_ID":categoryFK,"PRICE":price,"STOCK":stock})
    if len(product_list) == 0:
        raise ValueError("NO PRODUCT FOUND")
    return product_list



def list_categories(cursor):
    products = cursor.execute("SELECT * FROM ProductCategory")
    fetch = products.fetchall()
    product_list = []
    for item in fetch:
        id,category_name = item
        product_list.append({"ID":id,"CATEGORY_NAME":category_name})
    if len(product_list) == 0:
        raise ValueError("NO CATEGORY FOUND")
    return product_list



def search_product(cursor,id_or_name):
    try:
        product_id_search = cursor.execute("""
        SELECT ProductCategory.CategoryName,Products.*
        FROM Products
        INNER JOIN ProductCategory
        ON ProductCategory.CategoryPK = Products.CategoryFK
        WHERE ProductPK = ?
        """,(id_or_name,))
    except pyodbc.DataError:
        product_id_search = cursor.execute("""
        SELECT ProductCategory.CategoryName,Products.*
        FROM Products
        INNER JOIN ProductCategory
        ON ProductCategory.CategoryPK = Products.CategoryFK
        WHERE ProductName = ?
        """,(id_or_name,))
    results = product_id_search.fetchone()
    if results is not None:
        category_name,id,name,category_fk,price,stock = results
        return({"ID":id,"NAME":name,"CATEGORY_NAME":category_name,"CATEGORY_ID":category_fk,"PRICE":price,"STOCK":stock})
    else:
        raise ValueError("PRODUCT NOT FOUND")
       
        

def update_product(cursor,id,name=None,category=None,price=None):
    info_list = {}
    try:
        id = int(id)
    except ValueError:
        raise ValueError("ERROR: ID Must Be A Number!")
    if id is None:
        raise ValueError("ERROR: You Must Insert An ID!")
    product = cursor.execute("SELECT * FROM Products WHERE ProductPK = ?",(id,))
    if product.fetchone() is None:
        raise ValueError("ERROR: Product Does Not Exist!")
    if name is not None:
        name_verification = cursor.execute("SELECT ProductName FROM Products WHERE ProductName = ?",(name,))
        results = name_verification.fetchone()
        if results is not None:
            raise ValueError(f"PRODUCT {results[0]} ALREADY EXISTS")
        name = name.lower()
        info_list.update({"NAME":name})
    if category is not None:
        category_verification = cursor.execute("SELECT CategoryPK FROM ProductCategory WHERE CategoryName = ?",(category.lower(),))
        fetch = category_verification.fetchone()
        if fetch == None:
            raise ValueError("CATEGORY DOES NOT EXIST")
        else:
            info_list.update({"CATEGORY":fetch[0]})
    if price is not None:
        if price <= 0:
            raise ValueError("PRICE CANNNOT BE LOWER THAN/EQUAL TO 0")
        else:
            info_list.update({"PRICE":price})
    if name == None and category == None and price == None:
        raise ValueError("YOU MUST GIVE AT LEAST ONE ARGUMENT TO UPDATE")
    if info_list.get("NAME"):
        info_list["NAME"] = info_list["NAME"].upper()
        cursor.execute("UPDATE Products SET ProductName = ? WHERE ProductPK = ?",(info_list["NAME"],id))
    if info_list.get("CATEGORY"):
        category = info_list.get("CATEGORY")
        cursor.execute("UPDATE Products SET CategoryFK = ? WHERE ProductPK = ?",(category,id))
    if info_list.get("PRICE"):
        cursor.execute("UPDATE Products SET ProductPrice = ? WHERE ProductPK = ?",(info_list["PRICE"],id))
    return "PRODUCT UPDATED SUCCESSFULLY"



def delete_product(cursor,id):
    search = cursor.execute("SELECT * FROM Products WHERE ProductPK = ?", (id,))
    product = search.fetchone()
    if product is None:
        raise ValueError("PRODUCT DOES NOT EXIST")
    cursor.execute("DELETE FROM Products WHERE ProductPK = ?", (id,))
    return "PRODUCT SUCCESSFULLY DELETED"



def delete_category(cursor,id):
    search = cursor.execute("SELECT * FROM ProductCategory WHERE CategoryPK = ?",(id,))
    product = search.fetchone()
    if product is None:
        raise ValueError("CATEGORY DOES NOT EXIST")
    cursor.execute("DELETE FROM ProductCategory WHERE CategoryPK = ?",(id,))
    return "CATEGORY SUCCESSFULLY DELETED"

def stock_in(cursor,id,amount):
    search = cursor.execute("SELECT ProductStock FROM Products WHERE ProductPK = ?",(id,))
    fetch = search.fetchone()
    if fetch is None:
        raise ValueError("PRODUCT DOES NOT EXIST")
    if amount <= 0:
        raise ValueError("STOCK-IN CANNOT BE LOWER THAN/EQUAL TO 0")
    current_stock = fetch[0]
    new_stock = current_stock + amount
    cursor.execute("UPDATE Products SET ProductStock = ? WHERE ProductPK = ?",(new_stock,id))
    return "STOCK-IN REGISTERED"



def stock_out(cursor,id,amount):
    search = cursor.execute("SELECT ProductStock FROM Products WHERE ProductPK = ?",(id,))
    fetch = search.fetchone()
    if fetch == None:
        raise ValueError("PRODUCT DOES NOT EXIST")
    if amount == 0: 
        raise ValueError("QUANTITY ADDED CANNOT BE 0")
    if amount > 0:
        current_stock = fetch[0]
        new_stock = current_stock - amount
        if new_stock < 0:
            raise ValueError("INSUFFICIENT STOCK")
        cursor.execute("UPDATE Products SET ProductStock = ? WHERE ProductPK = ?",(new_stock,id))
        return "STOCK-OUT REGISTERED"
    if amount < 0:
        raise ValueError("STOCK-OUT CANNOT BE LOWER THAN/EQUAL TO 0")
        
    
def stock_log(cursor,id,amount,type):
    search = cursor.execute("SELECT ProductName FROM Products WHERE ProductPK = ?",(id,))
    fetch = search.fetchone()
    if fetch is None:
        raise ValueError("PRODUCT DOES NOT EXIST")
    product_name = fetch[0]
    cursor.execute("INSERT INTO StockLog (ProductName,ProductFK,Amount,MovimentationType) VALUES (?,?,?,?)",(product_name,id,amount,type))
    return ("STOCK LOG SUCCESSFULLY UPDATED")
        
def system_log(cursor,entity,entity_name,id,operation_type):
    if entity is None:
        raise ValueError("ENTITY MUST BE SPECIFIED")
    cursor.execute("INSERT INTO SystemLog (Entity,EntityName,EntityID,OperationType) VALUES (?,?,?,?)",(entity,entity_name,id,operation_type))
    return ("SYSTEM LOG SUCCESSFULLY UPDATED")

def view_system_log(cursor):
    system_log = cursor.execute("SELECT * FROM SystemLog")
    fetch = system_log.fetchall()
    system_list = []
    for item in fetch:
        id,entity,entity_name,entity_id,operation_type,date = item
        system_list.append({"ID":id,"ENTITY":entity,"ENTITY_NAME":entity_name,"ENTITY_ID":entity_id,"OPERATION_TYPE":operation_type,"DATE":date})
    if len(system_list) == 0:
        raise ValueError("LOG IS EMPTY")
    return system_list

def view_stock_log(cursor):
    stock_log = cursor.execute("SELECT * FROM StockLog")
    fetch = stock_log.fetchall()
    product_list = []
    for item in fetch:
        id,name,productFK,amount,movimentation_type,date = item
        product_list.append({"ID":id,"NAME":name,"PRODUCT_ID":productFK,"AMOUNT":amount,"MOVIMENTATION_TYPE":movimentation_type,"OPERATION_DATE":str(date)})
    if len(product_list) == 0:
        raise ValueError("LOG IS EMPTY")
    return product_list