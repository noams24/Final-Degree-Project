import os
from sys import exit
from enum import Enum
#from dotenv import load_dotenv
from typing import \
    Final  # A special typing construct to indicate to type checkers that a name cannot be re-assigned or overridden in a subclass

# load .env file
#load_dotenv()

# BOT Token
# TOKEN: Final = '5673704938:AAH7bcLtTitCVkmYyoDNSnMTRyvUaI5VsKk' -Money_Friendly_Bot
TOKEN: Final = '6186969245:AAGNbZJG8cH2etqCiKkhi6zmqZ5X16VrF3A'

# BOT name ro identify in group chats
BOT_USERNAME: Final = '@MoneyMateIL_bot'


# telegram info
# TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Commands
class Command(Enum):
    START = "start"  # start conversation
    HELP = "help"  # get information to how to use the bot
    STATS = "stats"  # show stats of the group
    NEW = "new"  # add a new expense
    DELETE = "delete"  # delete a new expenses
    SUM = "sum"  # get the total expenses in a specific month or year in a pie chart histogram
    LIST = "list"  # get a list of all your expenses in a specific month or year
    EXPORT = "export"  # export the expenses of a given month as excel file
    STOP = "stop"  # stops a recurring expense
    LINK = "link"  # send fast UI link (NICE TO HAVE)
    BREAKEVEN = "breakeven"
    ADDCATEGORY = "add_category"
    DELETECATEGORY = "delete_category"
    DASHBOARD = "dashboard"
    AUTH = "auth"
'''
start -  start conversation
help - get information to how to use the bot
stats - show stats of the group
delete - delete expenses from the last month
list - get a list of all your expenses in a specific month
export - export the expenses of a given month as excel file
dashboard - show the dashboard of the group
breakeven - show the breakeven of the group
add_category - add a new category
delete_cateogry - delete a category
auth - send the authentication number of the group
'''

# buttons:
class Button(Enum):
    APPROVE = "Approve ✅"
    CANCEL = "Cancel ❌"


class Status(Enum):
    APPROVED = "Approved ✅"
    CANCELLED = "Cancelled ❌"


# categories:
class Category(Enum):
    FOOD = "food"
    GAS = "gas"
    GROCERIES = "groceries"
    SHOPPING = "shopping"
    CLOTHES = "clothes"
    ENTERTAIMENT = "entertaiment"
    OTHER = "other"
    # TODO: verify categories

categories_config = ["food", "gas", "groceries", "shopping", "clothes", "entertaiment", "other"]
