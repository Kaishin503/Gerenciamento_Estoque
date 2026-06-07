import pyodbc
def create_product(cursor,name,category,price,stock):
    product_name_validation = cursor.execute("SELECT ProductName FROM Products WHERE ProductName = ?",(name,))
    results = product_name_validation.fetchone()
    if results is not None:
        raise ValueError(f"ERROR: Product {results[0]} Already Exists!")
    category_validation = cursor.execute("SELECT CategoryPK FROM ProductCategory WHERE CategoryName = ?",(category,))
    results = category_validation.fetchone()
    if results is None:
        raise ValueError("ERROR: Category Not Found!")
    else:
        categoryFK = results[0]
    if price <= 0:
        raise ValueError("ERROR: Price Cannot Be Less Than/Equal to 0!")
    if stock <= 0:
        raise ValueError("ERROR: Stock Cannot Be Less Than/Equal to 0!")
    cursor.execute("INSERT INTO Products (ProductName,CategoryFK,ProductPrice,ProductStock) VALUES (?,?,?,?)",(name,categoryFK,price,stock))
    return "Product Successfully Created."
    
    

def create_category(cursor,category_name):
    category_validation = cursor.execute("SELECT CategoryPK FROM ProductCategory WHERE CategoryName = ?",(category_name,))
    fetch = category_validation.fetchone()
    if fetch is not None:
        raise ValueError("ERROR: Category Already Exists!")
    else:
        cursor.execute("INSERT INTO ProductCategory (CategoryName) VALUES (?)",(category_name,))
        return (f"Created Category {category_name}!")


         
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
    return product_list



def list_categories(cursor):
    products = cursor.execute("SELECT * FROM ProductCategory")
    fetch = products.fetchall()
    product_list = []
    for item in fetch:
        id,category_name = item
        product_list.append({"ID":id,"CATEGORY_NAME":category_name})
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
        raise ValueError("ERROR: Product Not Found!")
       
        

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
            raise ValueError(f"ERROR: Product {results[0]} Already Exists!")
        name = name.lower()
        info_list.update({"NAME":name})
    if category is not None:
        category_verification = cursor.execute("SELECT CategoryPK FROM ProductCategory WHERE CategoryName = ?",(category.lower(),))
        if category_verification.fetchone() == None:
            raise ValueError("ERROR: Category Does Not Exist!")
        else:
            info_list.update({"CATEGORY":category_verification.fetchone()})
    if price is not None:
        if price <= 0:
            raise ValueError("ERROR: Price Cannot Be Lower Than/Equal To 0")
        else:
            info_list.update({"PRICE":price})
    if name == None and category == None and price == None:
        raise ValueError("ERROR: You Must Give At Least One Argument To Update!")
    if info_list.get("NAME"):
        cursor.execute("UPDATE Products SET ProductName = ? WHERE ProductPK = ?",(info_list["NAME"],id))
    if info_list.get("CATEGORY"):
        cursor.execute("UPDATE Products SET CategoryFK = ? WHERE ProductPK = ?",(category,id))
    if info_list.get("PRICE"):
        cursor.execute("UPDATE Products SET ProductPrice = ? WHERE ProductPK = ?",(info_list["PRICE"],id))
    return "Product Updated Successfully."



def delete_product(cursor,id):
    search = cursor.execute("SELECT * FROM Products WHERE ProductPK = ?",(id,))
    product = search.fetchone()
    if product is None:
        raise ValueError("ERROR: Product Does Not Exist!")
    cursor.execute("DELETE FROM Products WHERE ProductPK = ?",(id,))
    return "Product Successfully Deleted."



def delete_category(cursor,id):
    search = cursor.execute("SELECT * FROM ProductCategory WHERE CategoryPK = ?",(id,))
    product = search.fetchone()
    if product is None:
        raise ValueError("ERROR: Category Does Not Exist!")
    cursor.execute("DELETE FROM ProductCategory WHERE CategoryPK = ?",(id,))
    return "Category Successfully Deleted."

def stock_in(cursor,id,amount):
    search = cursor.execute("SELECT ProductStock FROM Products WHERE ProductPK = ?",(id,))
    fetch = search.fetchone()
    if fetch is None:
        raise ValueError("ERROR: Product Does Not Exist!")
    if amount <= 0:
        raise ValueError("ERROR: Stock-in Cannot Be Lower Than/Equal To 0!")
    current_stock = fetch[0]
    new_stock = current_stock + amount
    cursor.execute("UPDATE Products SET ProductStock = ? WHERE ProductPK = ?",(new_stock,id))
    return "Stock-In Registered."



def stock_out(cursor,id,amount):
    search = cursor.execute("SELECT ProductStock FROM Products WHERE ProductPK = ?",(id,))
    fetch = search.fetchone()
    if fetch == None:
        raise ValueError("ERROR: Product Does Not Exist!")
    if amount == 0: 
        raise ValueError("ERROR: Quantity Added Cannot Be 0!")
    if amount > 0:
        current_stock = fetch[0]
        new_stock = current_stock - amount
        cursor.execute("UPDATE Products SET ProductStock = ? WHERE ProductPK = ?",(new_stock,id))
        return "Stock-Out Registered."
    if amount < 0:
        current_stock = fetch[0]
        new_stock = current_stock + amount
        cursor.execute("UPDATE Products SET ProductStock = ? WHERE ProductPK = ?",(new_stock,id))
        return "Stock-Out Registered."
    