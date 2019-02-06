import sqlite3 as sql

def insert_product(bcode, ptype):
	con = sql.connect("database.db")
	# print(con)
	# con.execute(".tables")
	con.execute("INSERT INTO products VALUES (?,?);", (bcode, ptype))
	con.commit()
	con.close()

def insert_product_ingredient(bcode, iname):
	con = sql.connect("database.db")
	con.execute("INSERT INTO product_ingredients VALUES (?,?)", (bcode, iname))
	con.commit()
	con.close()

def insert_safety_rating(ptype, iname, sr):
	con = sql.connect("database.db")
	con.execute("INSERT INTO safety_ratings VALUES (?,?,?)", (ptype, iname, sr))
	con.commit()
	con.close()

def select_safety_rating(ptype, iname):
	con = sql.connect("database.db")
	cur = con.cursor()
	string = "SELECT safety_ratings.ingredient_name, safety_ratings.safety from safety_ratings where product_type='"+ptype+"' AND ingredient_name ='{0}'".format(iname.strip()) 
	print(string)
	result = cur.execute(string)
	return result.fetchall()

def select_ingredients(bcode):
	print(bcode)
	con = sql.connect("database.db")
	cur = con.cursor()
	result = cur.execute("SELECT safety_ratings.ingredient_name, safety from safety_ratings,product_ingredients where barcode="+bcode+" AND safety_ratings.ingredient_name=product_ingredients.ingredient_name" )
	return result.fetchall()

def insert_demo_data():
	insert_product('3948063023901','BISCUIT')
	insert_product('8906009070902','BISCUIT')
	insert_product_ingredient('8906009070902', 'ROLLED_OATS')
	insert_product_ingredient('8906009070902', 'HONEY')
	insert_product_ingredient('3948063023901', 'CALCIUM_SALT')
	insert_product_ingredient('3948063023901', 'SUGAR')
	insert_safety_rating('BISCUIT','ROLLED_OATS',7)
	insert_safety_rating('BISCUIT','HONEY',8)
	insert_safety_rating('BISCUIT','CALCIUM_SALT',5)
	insert_safety_rating('BISCUIT','SUGAR',6)