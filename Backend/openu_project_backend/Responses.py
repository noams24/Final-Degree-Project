
def responses(input_text):
    user_message = str(input_text).lower()
    return user_message


start_response = "Welcome to *MoneyMate* bot!\nThis bot helps you manage and track your expenses in groups.\nFor more information, type /help"


a = "You can add new expenses, get an overview, adding/removing category, break even between users, export to Excel and more!\n\n"
b = "To add new expenses, simply write the amount of the new expence.\nFor exemple '30'.\nThen the bot will ask you to select category.\n"
c = "Type / to view all the commands\n\n"
d = "*Commands*:\n\n"
e = "/stats - see graphs of the expenses\n"
f = "/delete - delete the last expense you entered.\n"
ff = "You can also write after the command 'today', 'month' or 'all'. Only the admin of the group can delete the expenses\n"
g = "/list - get a list of all your expenses\n"
h = "/export - export the expenses as excel file\n"
i = "/breakeven - see how much each one owes to others\n"
j = "/addcategory - add new category\n"
k = "/deletecategory - delete category\n\n"
l = "*Website* management\n"
m = "To enter the website and see more details and charts about the group expenses you need to enter user name and password. you can do that with the commands:\n"
n = "/dashboard - see the dashboard of your groups via our website\n"
o = "/getlogin - get your login user name\n"
p = "/setlogin - set your login user name\n"
q = "/setpassword - set your password\n"

help_response = a+b+c+d+e+f+ff+g+h+i+j+k+l+m+n+o+p+q