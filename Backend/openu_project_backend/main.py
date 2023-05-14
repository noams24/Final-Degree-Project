from Responses import responses, get_price, get_category, valid_email
from config import TOKEN, Button, Command, categories_config

from backend import Database, get_categories, write_category, remove_category

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler
)


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if update.message.chat.type == 'private':
        await update.message.reply_text(f'This bot avaible only for groups!')
        return

    

    user_name = update.message.from_user.first_name
    group_name = update.message.chat.title
    user_id = update.message.from_user.id
    group_id = update.message.chat.id

    # checks of user enterd email and checks if it's valid
    if valid_email(update.message.text):
        response = db.add_user(user_id, user_name, email=update.message.text)
        await update.message.reply_text(response)
        return
    
    # check if user and group exists:
    response = db.exists(user_id, group_id, group_name)
    if response: 
        await update.message.reply_text(response) #user doesn't exists
        return

    all_categories = categories_config + get_categories(str(group_id))
    reply = responses(update.message.text)
    
    keyboard = [[]]
    j = 0
    for i, item in enumerate(all_categories):
        if i % 3 == 0 and i != 0:
            keyboard.append([])
            j += 1
        keyboard[j].append(InlineKeyboardButton(item, callback_data=item))
        
    if update.message.text.isnumeric():  # user report only number -> bot will suggests categories
        if int(update.message.text) < 0:
            update.message.reply_text("Expense must be greater than 0", reply_markup=reply_markup)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(reply, reply_markup=reply_markup)
    else:
        await update.message.reply_text("You must enter a number")



async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    msg = query.data
    await query.answer()
    group_id = query.message.chat.id

    responses = ["This Month", "Last Month", "All Time"]
    if msg in responses:
        result = db.total_expenses(group_id,msg)
        if not result:
            await query.message.reply_text(f'No expenses found')
            return
        db.piechart(group_id,msg)
        db.barchart(group_id,msg)
        await query.message.reply_text(f'Total expenses of the group is {result} ')
        await context.bot.send_photo(chat_id=group_id, photo=open('my_plot.png', 'rb'))
        await context.bot.send_photo(chat_id=group_id, photo=open('my_plot2.png', 'rb'))
        await query.message.delete()
        return

    if query.data == f"{Button.APPROVE.value}":
        price = get_price(query.message.text)
        category = get_category(query.message.text)

    else:  # Cancel button
        price = int(query.message.text)
        category = query.data

    user_id = query.message.reply_to_message.from_user.id
    user_name = query.message.reply_to_message.from_user.name
    date = query.message.date

    # add a new row to group table
    if query.message.chat.type == 'group':
        group_id = query.message.chat.id
        #group_name = query.message.chat.title
        db.new_expense(user_id, group_id, category, price)
        res = f"{user_name} spended {query.message.text} on {category}"
        await query.edit_message_text(text=res)

    # add a new row to private user table
    else:
        pass

# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# ---------------------- Commands ----------------------- #
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Inform user about what this bot can do"""
    # admins = update.get_bot().get_chat_administrators(update.message.chat.id)
    await update.message.reply_text("hi!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:


    if update.message.chat.type == 'private':
        await update.message.reply_text(f'This bot avaible only for groups!')
        return    

    keyboard = [
        [
            InlineKeyboardButton("This Month", callback_data="This Month"),
            InlineKeyboardButton("Last Month", callback_data="Last Month"),
            InlineKeyboardButton("All Time", callback_data="All Time")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a period of time", reply_markup=reply_markup)


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    if update.message.chat.type == 'private':
        await update.message.reply_text(f'This bot avaible only for groups!')
        return

    user_id = update.message.from_user.id
    group_id = update.message.chat.id
    deleted = db.delete(group_id, user_id)
    if deleted:
        await update.message.reply_text("Expenses deleted from the last Month!")
    else:
        await update.message.reply_text("Only the admin of the group can delete expenses!")



async def export(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    if update.message.chat.type == 'private':
        await update.message.reply_text(f'This bot avaible only for groups!')
        return

    db.toExcel(update.message.chat.id)
    await context.bot.send_document(chat_id=update.message['chat']['id'], document=open('expenses.xlsx', 'rb'))


async def breakeven(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    if update.message.chat.type == 'private':
        await update.message.reply_text(f'This bot avaible only for groups!')
        return

    response = db.breakeven(update.message.chat.id)
    if not response:
        response = "There is no breakeven for this group"
    await update.message.reply_text(response)


async def add_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if update.message.chat.type == 'private':
        await update.message.reply_text(f'This bot avaible only for groups!')
        return

    try:
        new_category = update.message.text.split()
        group_id = str(update.message.chat.id)
        added = write_category(group_id, new_category[1])
        await update.message.reply_text(added)
    except:
        await update.message.reply_text("an error has occured")


async def delete_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if update.message.chat.type == 'private':
        await update.message.reply_text(f'This bot avaible only for groups!')
        return

    try:
        new_category = update.message.text.split()
        group_id = str(update.message.chat.id)
        deleted = remove_category(group_id, new_category[1])
        await update.message.reply_text(deleted)
    except:
        await update.message.reply_text("an error has occured")


async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if update.message.chat.type == 'private':
        await update.message.reply_text(f'This bot avaible only for groups!')
        return

    group_id = str(update.message.chat.id)
    link ="www.google.com"
    await update.message.reply_text(text = f"<a href='{link}'>dashboard</a>", parse_mode = "html")
    

async def auth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if update.message.chat.type == 'private':
        await update.message.reply_text(f'This bot avaible only for groups!')
        return

    group_id = str(update.message.chat.id)
    auth_code = db.get_auth(group_id)
    await update.message.reply_text(f"Your Authentication code is {auth_code}")

# ---------------------- Commands - END ----------------------- #


# Run the program
if __name__ == '__main__':
    db = Database()
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler(f"{Command.START.value}", start))
    app.add_handler(CommandHandler(f"{Command.HELP.value}", help_command))
    app.add_handler(CommandHandler(f"{Command.DELETE.value}", delete))
    app.add_handler(CommandHandler(f"{Command.EXPORT.value}", export))
    app.add_handler(CommandHandler(f"{Command.STATS.value}", stats))
    app.add_handler(CommandHandler(f"{Command.BREAKEVEN.value}", breakeven))
    app.add_handler(CommandHandler(f"{Command.ADDCATEGORY.value}", add_category))
    app.add_handler(CommandHandler(f"{Command.DELETECATEGORY.value}", delete_category))
    app.add_handler(CommandHandler(f"{Command.DASHBOARD.value}", dashboard))
    app.add_handler(CommandHandler(f"{Command.AUTH.value}", auth))
    app.add_handler(CallbackQueryHandler(button))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')  # TODO: delete this debug line
    # Run the bot
    app.run_polling(poll_interval=1)
