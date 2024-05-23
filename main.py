import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.error import Conflict, NetworkError, Unauthorized
from keep_alive import keep_alive
import time

# Replace 'YOUR_BOT_TOKEN' with your actual bot token obtained from BotFather
TOKEN = '7073748087:AAHMd-DY5eXlBjdxN_Q0xSRTQCrXESN1usk'

# List of names (initial list)
names = ['Alice', 'Bob', 'Charlie', 'David', 'Emma']

def pick_names(update: Update, context: CallbackContext):
    num_names = int(context.args[0]) if context.args else 3
    if num_names < 1 or num_names > 10:
        update.message.reply_text("Please pick a number between 1 and 10.")
        return
    
    picked_names = random.sample(names, num_names)
    picked_names_str = ", ".join(picked_names)
    update.message.reply_text(f"The randomly picked names are: {picked_names_str}")

def pick_name(update: Update, context: CallbackContext):
    picked_name = random.choice(names)
    update.message.reply_text(f"The randomly picked name is: {picked_name}")

def add_name(update: Update, context: CallbackContext):
    new_name = context.args[0] if context.args else None
    if new_name:
        names.append(new_name)
        update.message.reply_text(f"Name '{new_name}' added successfully!")
    else:
        update.message.reply_text("Please provide a name to add.")

def add_names(update: Update, context: CallbackContext):
    names_to_add = context.args
    if names_to_add:
        names.extend(names_to_add)
        update.message.reply_text(f"Names {' '.join(names_to_add)} added successfully!")
    else:
        update.message.reply_text("Please provide names to add.")

def remove_name(update: Update, context: CallbackContext):
    name_to_remove = context.args[0] if context.args else None
    if name_to_remove:
        if name_to_remove in names:
            names.remove(name_to_remove)
            update.message.reply_text(f"Name '{name_to_remove}' removed successfully!")
        else:
            update.message.reply_text(f"Name '{name_to_remove}' not found in the list.")
    else:
        update.message.reply_text("Please provide a name to remove.")

def remove_all(update: Update, context: CallbackContext):
    names.clear()
    update.message.reply_text("All names removed from the list.")

def list_names(update: Update, context: CallbackContext):
    names_str = "\n".join(names)
    update.message.reply_text(f"Names in the list:\n{names_str}")

def help_command(update: Update, context: CallbackContext):
    help_text = """
    Available commands:
    /pickname - Pick one random name from the list
    /picknames <number> - Pick multiple random names from the list (up to 10)
    /addname <name> - Add a single name to the list
    /addnames <name1> <name2> ... - Add multiple names to the list
    /removename <name> - Remove a single name from the list
    /removeall - Remove all names from the list
    /list - List all names currently in the list
    /help - Show this help message
    """
    update.message.reply_text(help_text)

def error_callback(update: Update, context: CallbackContext):
    try:
        raise context.error
    except Conflict:
        # Handle the conflict error by restarting the bot
        print("Conflict error detected. Restarting the bot.")
        context.bot.stop()
        time.sleep(5)
        main()
    except NetworkError:
        time.sleep(5)
    except Unauthorized:
        # Handle unauthorized error
        pass

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("picknames", pick_names, pass_args=True))
    dp.add_handler(CommandHandler("pickname", pick_name))
    for i in range(2, 11):
        dp.add_handler(CommandHandler(f"picknames{i}", pick_names, pass_args=True))
    
    dp.add_handler(CommandHandler("addname", add_name, pass_args=True))
    dp.add_handler(CommandHandler("addnames", add_names, pass_args=True))
    dp.add_handler(CommandHandler("removename", remove_name, pass_args=True))
    dp.add_handler(CommandHandler("removeall", remove_all))
    dp.add_handler(CommandHandler("list", list_names))
    dp.add_handler(CommandHandler("help", help_command))
    
    dp.add_error_handler(error_callback)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    keep_alive()  # Add this line to start the keep-alive server
    main()

