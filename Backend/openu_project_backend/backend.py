import uuid
import random
import json
import string
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import bcrypt

import config
from config import categories_config

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host =      config.DB_HOST,
            database =  config.DB_DATABASE_NAME,
            user =      config.DB_USER,
            password =  config.DB_PASSWORD,
            port =  int(config.DB_PORT))
        
        self.cur = self.conn.cursor()
    
    # -------------------- SETs / CREATEs ------------------   
    def create_user(self, user_id, user_name, login_name, password, is_admin) -> str:
        ''' create user in 'users' table '''
        #validate login_name #NOTE: XXX: !NICE TO HAVE! more validation cases
        if len(login_name) < config.LOGIN_NAME_MIN_LENGTH: return None
        if len(login_name) > config.LOGIN_NAME_MAX_LENGTH: return None
        
        #set new login_name in db
        self.cur.execute(f"INSERT INTO users (pk_id, user_name, login_name, password, is_admin) VALUES ('{user_id}', '{user_name}', '{(login_name).lower()}', '{password}', '{is_admin}')")
        self.conn.commit()
        
        return login_name

    def create_group(self, group_id, group_name):
        ''' create group in 'groups' table '''
        self.cur.execute(f"INSERT INTO groups (pk_id, group_name) VALUES ('{group_id}', '{group_name}')")
        self.conn.commit()
    
    def set_login_name(self, user_id, login_name) -> str:
        ''' set new login_name for user_id, return None if failed, return login_name if valid '''
        #validate login_Name #NOTE: XXX: !NICE TO HAVE! more validation cases
        if len(login_name) < config.LOGIN_NAME_MIN_LENGTH or len(login_name) > config.LOGIN_NAME_MAX_LENGTH:
            return "Login name should be between [{LOGIN_NAME_MIN_LENGTH}-{LOGIN_NAME_MAX_LENGTH}] charatcers"
        
        self.cur.execute(f"select * from users where login_name = '{login_name}'") #make sure login_name not exists
                
        already_exist_login_name = self.cur.fetchall()
        if already_exist_login_name:
            return "Login name already exists, please choose another one"
        #set new login_Name in db
        self.cur.execute(f"UPDATE users SET login_name = '{login_name}' WHERE pk_id = {user_id}")
        self.conn.commit()
        
        return "Successfully updated login name!"
    
    def set_password(self, user_id, password) -> str:
        ''' set new password for user_id, return None if failed, return password if valid '''
        if len(password) < config.PASSWORD_MIN_LENGTH: return None
        if len(password) > config.PASSWORD_MAX_LENGTH: return None

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()
        query = "UPDATE users SET password = %s WHERE pk_id = %s"
        self.cur.execute(query, (hashed_password, user_id))
        self.conn.commit()
        return 1
       
    def create_usergroups(self, user_id, group_id, is_group_admin) -> None:
        ''' create connection (row) in 'usergroups' table '''
        self.cur.execute(f"INSERT INTO usergroups (fk_user_id, fk_group_id, role) VALUES ('{user_id}', '{group_id}', '{is_group_admin}')")
        self.conn.commit()
    
    def new_expense(self, user_id,group_id, category, price):
        self.cur.execute("INSERT INTO userproducts (fk_user_id,fk_group_id,category_name,amount) VALUES (%s, %s, %s ,%s)",(user_id, group_id,category, price))
        self.conn.commit()

    # -------------------- GETs ------------------
    def get_password(self, user_id) -> str:
        ''' Get password from 'users' table following given user_id '''
        #get password following given user_id
        self.cur.execute(f"select password from users where pk_id = {user_id}")
        plain_password = self.cur.fetchall()[0][0] #return list of tuples thats why
        if plain_password:
            return plain_password
        else:
            return None
        
    def get_login(self, user_id) -> str:
        ''' Get login_name from 'users' table following given user_id '''
        #get login_name following given user_id
        self.cur.execute(f"select login_name from users where pk_id = {user_id}")
        login_name = self.cur.fetchall()[0][0] #return list of tuples thats why
        if login_name:
            return login_name
        else:
            return None
        
    # -------------------- IS_EXISTS ------------------
    def is_user_exists(self, user_id):
        ''' Check if user exists.\n
            Return (True, string of the details about the user) if exists,\n
            Return (False, None) if not exists'''
            
        #check if user_id exists
        self.cur.execute(f"select * from users where pk_id = {user_id}")
        user = self.cur.fetchall()
        if user:
            return True
        else:
            return False
    
    def is_usergroups_row_exists(self, user_id, group_id) -> bool:
        ''' return True if user-group row is already exists '''
        self.cur.execute(f"SELECT * FROM usergroups WHERE fk_user_id = {user_id} AND fk_group_id = {group_id}")
        row = self.cur.fetchall()
        if row:
            return True
        else:
            return False
    
    def is_group_exists(self, group_id):
        ''' Check if group exists, return True / False'''
        #check if group_id exists
        self.cur.execute(f"select * from groups where pk_id = {group_id}")
        group = self.cur.fetchall() 
        if group:
            return True
        else:
            return False
   
    def exists(self,user_id, user_name, group_id, group_name, group_admin_flag: bool= False, update=None):
        """ activate on report. check if user, group and usergroups exists - else create them for tracking the report """
        
        #check if user exists
        if not self.is_user_exists(user_id):
            #if not create random user
            while True:
                login_name = generate_random_username().lower()
                self.cur.execute(f"select * from users where login_name = '{login_name}'") #make sure login_name not exists
                user = self.cur.fetchall()
                if not user:
                    break
            temp_password = f"{uuid.uuid4()}" #generate new password
            self.create_user(user_id, user_name, login_name, temp_password, is_admin=0)
  
        # check if group exists
        if not self.is_group_exists(group_id):
            self.create_group(group_id=group_id, group_name=group_name)

        # check if user-group connection exists:
        if not self.is_usergroups_row_exists(user_id,group_id):
            self.create_usergroups(user_id=user_id, group_id=group_id, is_group_admin=1)

    # -------------------- FUNCTIONS ------------------
    def insert(self, message_id, group_id, group_name, user_id, user_name, category, price):
        self.cur.execute("INSERT INTO db VALUES (?,?,?,?,?,?,?)",(message_id, group_id, group_name, user_id, user_name, category, price))
        self.conn.commit()

    def delete(self,group_id, user_id,delete_date):
        self.cur.execute(f"select role from usergroups where fk_group_id = {group_id} and fk_user_id = {user_id} ")
        user_role = self.cur.fetchone()[0]
        if user_role == 1:
            if delete_date == 'latest':
                query = f'''select *
           FROM userproducts
           WHERE fk_group_id = {group_id}
           ORDER BY "pk_id" DESC
           LIMIT 1;'''
                self.cur.execute(query)
                exepense_id = self.cur.fetchone()[0]
                self.cur.execute(f"DELETE FROM userproducts WHERE pk_id = {exepense_id}")
                #self.cur.execute(f"""DELETE FROM userproducts WHERE fk_group_id = {group_id} ORDER BY date_created DESC LIMIT 1)""")
            elif delete_date == 'today':
                self.cur.execute(f"DELETE FROM userproducts WHERE fk_group_id = {group_id} and EXTRACT(DAY FROM date_created) = EXTRACT(DAY FROM CURRENT_DATE)")
            elif delete_date == 'month':
                self.cur.execute(f"DELETE FROM userproducts WHERE fk_group_id = {group_id} and EXTRACT(MONTH FROM date_created) = EXTRACT(MONTH FROM CURRENT_DATE)")
            elif delete_date == 'all':
                self.cur.execute(f"DELETE FROM userproducts WHERE fk_group_id = {group_id}")
            else:
                return "invalid format"
        else:
            return "Only the admin of the group can delete expenses!"
        self.conn.commit()
        
        return "Succesfuly deleted!"

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
                            result += b1[0] + " owe " + b2[0] + " " + str(round(b1[1])) + " ₪\n"
                            b2[1] = b2[1] + b1[1]
                            b1[1] = 0
                            break
                        else: # b1 pay part of his debt to b2
                            result += b1[0] + " owe " + b2[0] + " " + str(round(-b2[1])) + " ₪\n"
                            b1[1] = b1[1] + b2[1]
                            b2[1] = 0
        return result

    def list_of_expenses(self,group_id, date,group_type):
        result = f"Expenses for {date}:\n\n"

        if date == "this Month":
             query = (f"with temp as (select pk_id, user_name from users) select user_name, amount, category_name, date_created from userproducts up join temp t on up.fk_user_id = t.pk_id where fk_group_id = {group_id} and EXTRACT(MONTH FROM date_created) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM date_created) = EXTRACT(YEAR FROM CURRENT_DATE)")
        elif date == "last Month":
             query = (f"with temp as (select pk_id, user_name from users) select user_name, amount, category_name, date_created from userproducts up join temp t on up.fk_user_id = t.pk_id where fk_group_id = {group_id} AND EXTRACT(MONTH FROM date_created) = EXTRACT(MONTH FROM CURRENT_DATE)-1 AND EXTRACT(YEAR FROM date_created) = EXTRACT(YEAR FROM CURRENT_DATE)")
        else:
             query = (f"with temp as (select pk_id, user_name from users) select user_name, amount, category_name, date_created from userproducts up join temp t on up.fk_user_id = t.pk_id where fk_group_id = {group_id}")
        self.cur.execute(query)
        data = self.cur.fetchall()
        if not data:
            return "no expenses found"
        last_date = data[0][3].day
        result += f"*{data[0][3].day}/{data[0][3].month}/{data[0][3].year}*\n"
        if group_type == 'group':
            for row in data:
                if row[3].day != last_date:
                    result += f"*{row[3].day}/{row[3].month}/{row[3].year}*\n"
                    last_date = row[3].day
                result += f"{row[0]} spent {row[1]}₪ on {row[2]}\n"
        else:
            for row in data:
                if row[3].day != last_date:
                    result += f"*{row[3].day}/{row[3].month}/{row[3].year}*\n"
                    last_date = row[3].day
                result += f"{row[1]}₪ on {row[2]}\n"
        return result

    # end of class


#other functions:

def write_category(group_id, new_category):

    try:
        open("categories.json").read(1)
    except:
        # file is empty
        data = {}
        with open("categories.json", "w") as f:
            json.dump(data, f)
        # file is not empty, read JSON file into a dictionary
    with open("categories.json", "r") as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
                # file is not in valid JSON format
            data = {}
    # add a new key-value pair with a string value to the dictionary
    #print(group_id)
    #print(data)
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
    
    try:
        with open("categories.json", "r") as f:
            data = json.load(f)
            if group_id in data:
                return data[group_id]
            return []
    except:
        data = {}
        json_string = json.dumps(data)
        with open("categories.json", "w") as f:
            f.write(json_string)
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


def generate_random_username(length=config.LOGIN_NAME_MIN_LENGTH+2):
    characters = string.ascii_letters + string.digits  # Letters + Digits
    username = ''.join(random.choice(characters) for _ in range(length))
    return username


def valid_input(input):

    if not input.isnumeric():
        return "You must enter a number"

    if int(input) < 0:
        return "Expense must be greater than 0"
    
    if int(input) > 10000000:
        return "Expense must be less than 10,000,000"
