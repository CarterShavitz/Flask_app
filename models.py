import sqlite3


class Schema:
   def __init__(self):
       self.conn = sqlite3.connect('food.db')
       self.create_user_table()
       self.create_food_table()

   def __del__(self):
       # body of destructor
       self.conn.commit()
       self.conn.close()

   def create_food_table(self):

       query = """
       CREATE TABLE IF NOT EXISTS "Food" (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         Name TEXT,
         Calories TEXT,
         EatenOn Date DEFAULT CURRENT_DATE,
         UserId INTEGER FOREIGNKEY REFERENCES User(_id)
       );
       """

       self.conn.execute(query)

   def create_user_table(self):
       query = """
       CREATE TABLE IF NOT EXISTS "User" (
       _id INTEGER PRIMARY KEY AUTOINCREMENT,
       Name TEXT NOT NULL,
       Email TEXT,
       CreatedOn Date default CURRENT_DATE
       );
       """
       self.conn.execute(query)


class FoodModel:
   TABLENAME = "Food"

   def __init__(self):
       self.conn = sqlite3.connect('food.db')
       self.conn.row_factory = sqlite3.Row

   def __del__(self):
       # body of destructor
       self.conn.commit()
       self.conn.close()

   def get_by_id(self, id):
       where_clause = f"id = {id}"
       return self.list_items(where_clause)

   def create(self, params):
       print (params)
       query = f'insert into {self.TABLENAME} ' \
               f'(Name, Calories, UserId) ' \
               f'values ("{params.get("Name")}","{params.get("Calories")}",' \
               f'"{params.get("UserId")}")'

       """insert into food (Name, Calories, UserId) values ("food1","food1", "2025-03-25", 1)"""
      
       result = self.conn.execute(query)
       return self.get_by_id(result.lastrowid)

   def delete(self, item_id):
       query = f"DELETE FROM {self.TABLENAME} " \
               f"WHERE id = {item_id}"
       print (query)
       self.conn.execute(query)
       return self.list_items()

   def update(self, item_id, update_dict):
       """
       column: value
       Name: new name
       """
       set_query = ", ".join([f'{column} = "{value}"'
                    for column, value in update_dict.items()])

       query = f"UPDATE {self.TABLENAME} " \
               f"SET {set_query} " \
               f"WHERE id = {item_id}"
  
       self.conn.execute(query)
       return self.get_by_id(item_id)

   def list_items(self, where_clause="TRUE"):
       query = f"SELECT id, Name, Calories " \
               f"from {self.TABLENAME} " \
               f"WHERE {where_clause}"
       print (query)
       result_set = self.conn.execute(query).fetchall()
       print (result_set)
       result = [{column: row[i]
                 for i, column in enumerate(result_set[0].keys())}
                 for row in result_set]
       return result


class User:
   TABLENAME = "User"

   def create(self, name, email):
       query = f'insert into {self.TABLENAME} ' \
               f'(Name, Email) ' \
               f'values ({name},{email})'
       result = self.conn.execute(query)
       return result
