import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import random
from collections import defaultdict
import json
from config import categories_config

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
           )
        
        self.cur = self.conn.cursor()
       

    def new_expense(self, user_id,group_id, category, price):
        self.cur.execute("INSERT INTO userproducts (fk_user_id,fk_group_id,category_name,amount) VALUES (%s, %s, %s ,%s)",(user_id, group_id,category, price))
        self.conn.commit()
    

    def delete(self,group_id, user_id):
        self.cur.execute(f"select role from usergroups where fk_group_id = {group_id} and fk_user_id = {user_id} ")
        user_role = self.cur.fetchone()[0]
        if user_role == 1:
            self.cur.execute(f"DELETE FROM userproducts WHERE fk_group_id = {group_id} and EXTRACT(MONTH FROM date_created) = EXTRACT(MONTH FROM CURRENT_DATE)")
            self.conn.commit()
        return user_role

    def toExcel(self, group_id):
        query = f"select u.user_name as user, category_name as category, amount as price from userproducts up join users u on up.fk_user_id = u.pk_id where fk_group_id = {group_id}"
        df = pd.read_sql(query, self.conn)
        df.to_excel("expenses.xlsx", index=False)  

    def piechart(self, group_id, date):
        if date == "This Month":
            query = f"SELECT category_name, SUM(amount) FROM userproducts where fk_group_id = {group_id} AND EXTRACT(MONTH FROM date_created) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM date_created) = EXTRACT(YEAR FROM CURRENT_DATE) GROUP BY category_name"
        elif date == "Last Month":
            query = f"SELECT category_name, SUM(amount) FROM userproducts where fk_group_id = {group_id} AND EXTRACT(MONTH FROM date_created) = EXTRACT(MONTH FROM CURRENT_DATE) -1 AND EXTRACT(YEAR FROM date_created) = EXTRACT(YEAR FROM CURRENT_DATE) GROUP BY category_name"
        else:
            query = f"SELECT category_name, SUM(amount) FROM userproducts where fk_group_id = {group_id} GROUP BY category_name"
        
        self.cur.execute(query)
        data = self.cur.fetchall()
        # create lists of categories and total prices
        categories = [row[0][::1] for row in data]
        prices = [row[1] for row in data]

        plt.pie(prices, labels=categories, autopct='%1.1f%%')
        plt.axis('equal')
        plt.title('Expenses')
        plt.savefig('my_plot.png')
        plt.clf()

    def barchart(self,group_id, date):
        if date == "This Month":
            query = f"select u.user_name, sum(amount) from userproducts up join users u on up.fk_user_id = u.pk_id where fk_group_id = {group_id} AND EXTRACT(MONTH FROM up.date_created) = EXTRACT(MONTH FROM CURRENT_DATE) group by u.user_name"
        elif date == "Last Month":
            query = f"select u.user_name, sum(amount) from userproducts up join users u on up.fk_user_id = u.pk_id where fk_group_id = {group_id} AND EXTRACT(MONTH FROM up.date_created) = EXTRACT(MONTH FROM CURRENT_DATE) -1 group by u.user_name"
        else:
            query = f"select u.user_name, sum(amount) from userproducts up join users u on up.fk_user_id = u.pk_id where fk_group_id = {group_id} group by u.user_name"
        
        self.cur.execute(query)
        data = self.cur.fetchall()
        # create lists of categories and total prices
        users = [row[0][::1] for row in data]
        prices = [row[1] for row in data]

        plt.bar(users, prices)
        plt.xlabel('user')
        plt.ylabel('amount spend')
        plt.title('Expenses by users')
        plt.savefig('my_plot2.png')
        plt.clf()

    def total_expenses(self, group_id, date):
        if date == "This Month":
            self.cur.execute(f'SELECT SUM(amount) FROM userproducts where fk_group_id = {group_id} AND EXTRACT(MONTH FROM date_created) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM date_created) = EXTRACT(YEAR FROM CURRENT_DATE)')

        elif date == "Last Month":
            self.cur.execute(f'SELECT SUM(amount) FROM userproducts where fk_group_id = {group_id} AND EXTRACT(MONTH FROM date_created) = EXTRACT(MONTH FROM CURRENT_DATE)-1 AND EXTRACT(YEAR FROM date_created) = EXTRACT(YEAR FROM CURRENT_DATE)')
        else:
           self.cur.execute(f'SELECT SUM(amount) FROM userproducts where fk_group_id = {group_id}') 
        return self.cur.fetchone()[0]

    def exists(self,user_id, group_id, group_name):

        #check if user exists
        self.cur.execute(f"select * from users where pk_id = {user_id}")
        user = self.cur.fetchall()
        if not user:
            return "Please enter Email first!"
            #self.cur.execute("INSERT INTO users (pk_id,user_name,email,is_admin) VALUES (%s, %s, %s, %s)",(user_id, user_name, email, 0))
            #self.conn.commit()
        
        # check if group exists
        self.cur.execute(f"select * from groups where pk_id = {group_id}")
        group= self.cur.fetchall()
        if not group:
            auth = random.randint(10000,99999)
            self.cur.execute("INSERT INTO groups (pk_id,group_name,auth) VALUES (%s,%s,%s)",(group_id,group_name,auth))
            self.conn.commit()

        # check if user is in group:
        self.cur.execute(f"select * from usergroups where fk_user_id = {user_id} and fk_group_id = {group_id}")
        usergroups= self.cur.fetchall()
        if not usergroups:
            if group:
                role = 0
            else:
                role = 1
            self.cur.execute("INSERT INTO usergroups (fk_user_id,fk_group_id, role) VALUES (%s, %s, %s)",(user_id, group_id, role))
            self.conn.commit()

    def add_user(self,user_id,user_name, email):
        #check if user exists

        #check if email already in the db:
        self.cur.execute(f"select * from users where email = '{email}'")
        email_in_db = self.cur.fetchall()
        if email_in_db:
            return "Email already in the db"
        

        self.cur.execute(f"select * from users where pk_id = {user_id}")
        user = self.cur.fetchall()
        if not user:
            self.cur.execute("INSERT INTO users (pk_id,user_name,email,is_admin) VALUES (%s, %s, %s, %s)",(user_id, user_name, email, 0))
            self.conn.commit()
            return "User added"
        #update 
        else:
            return "User already has email"

        



    def breakeven(self, group_id):
        
        self.cur.execute(f"select u.user_name, sum(amount)from userproducts up join users u on up.fk_user_id = u.pk_id where fk_group_id = {group_id} group by u.user_name")
        data = self.cur.fetchall()
        if not data:
            return "No expenses to split"
        balances = []
        sum = 0
        average = 0
        result = ""
        # חישוב המוצע שכל אדם צריך לשלם
        for person in data:
            sum += person[1]
        average = sum / len(data)
        # חישוב המאזן של כל אדם
        for person in data:
            balances.append([person[0], average - person[1]])
        for b1 in balances:
            if b1[1] > 0:
                for b2 in balances:
                    if b2[1] < 0:
                        if b1[1] <= -b2[1]: # b1 pay all his debt to b2
                            result += b1[0] + " give to " + b2[0] + " " + str(b1[1]) + " mesos"
                            b2[1] = b2[1] + b1[1]
                            b1[1] = 0
                            break
                        else: # b1 pay part of his debt to b2
                            result += b1[0] + " give to " + b2[0] + " " + str(-b2[1]) + " mesos"
                            b1[1] = b1[1] + b2[1]
                            b2[1] = 0
        return result



    def get_auth(self, group_id):
        self.cur.execute(f"select auth from groups where pk_id = {group_id}")
        row = self.cur.fetchone()[0]
        return row
    

    # end of class

    '''
    def get_users(self):
        self.cur.execute("select * from users")
        rows = self.cur.fetchall()
        print(rows)


    def get_user_products(self):
        self.cur.execute("select * from userproducts")
        rows = self.cur.fetchall()
        print(rows)

    def get_productcategories(self):
        self.cur.execute("select * from productcategories")
        rows = self.cur.fetchall()
        print(rows)
    '''
    
#other functions:

def write_category(group_id, new_category):
    if not open("categories.json").read(1):
        # file is empty
        data = {}
    else:
        # file is not empty, read JSON file into a dictionary
        with open("categories.json", "r") as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                # file is not in valid JSON format
                data = {}
    # add a new key-value pair with a string value to the dictionary
    
    if group_id in data:
        if new_category in data[group_id] or new_category in categories_config:
            return "Category already exists!"
        else: 
            data[group_id].append(new_category) # add new category to the group

    # group not exist. add new group    
    else:
        data[group_id] = [new_category]
    # write the updated dictionary to the same JSON file
    with open("categories.json", "w") as f:
        json.dump(data, f)
    return "Category added successfuly!"


def get_categories(group_id):
    if not open("categories.json").read(1):
        # file is empty
        return []
    else:
        # file is not empty, read JSON file into a dictionary
        with open("categories.json", "r") as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                # file is not in valid JSON format
                data = {}
    if group_id in data:
        return data[group_id]
    else:
        return []

def remove_category(group_id, category):
    if not open("categories.json").read(1):
        # file is empty
        return "category not exist"
    else:
        # file is not empty, read JSON file into a dictionary
        with open("categories.json", "r") as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                # file is not in valid JSON format
                return "category not exist"
    if group_id in data:
        if category in data[group_id]:
            data[group_id].remove(str(category))
            with open("categories.json", "w") as f:
                json.dump(data, f)
            return "category removed successfuly!"
    else:
        return "category not exist"



#print(add_category("1","foodd"))
#db = Database()
#print(db.split(-895523590))
#db.barchart(-895523590, "")
#db.barchart(-749348626, "")
#print(db.total_expenses(-749348626))
#db.toExcel(-749348626)
#db.piechart(-749348626)
