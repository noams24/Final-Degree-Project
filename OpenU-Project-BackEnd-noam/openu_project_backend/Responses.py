
#examples:
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

