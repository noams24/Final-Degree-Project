
#examples:
import re
groups = ['123','1234']
users = ['12', '124']

def responses(input_text):
    user_message = str(input_text).lower()

    msg = user_message.split()
    return user_message

def get_price(input_text):
    msg = input_text.split()
    for s in msg:
        if s.isnumeric():
            return s

def get_category(input_text):
    msg = input_text.split()
    for s in msg:
        if not s.isnumeric():
            return s

def add_row_private(user_id):
    # private user
    if user_id in users:
        pass
    # create new user table
    else:
        pass


def valid_email(email):
    if len(email) > 7:
        if re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) != None:
            return True
    return False
