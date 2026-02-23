import logging
import math
import re
import os
from fractions import Fraction
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

user_data = {}

# -----------------------
# لوحة احترافية ثابتة
# -----------------------
def build_keyboard():
    keyboard = [
        ["(", ")", "√", "𝑎⁄𝑏", "⌫"],
        ["7", "8", "9", "÷"],
        ["4", "5", "6", "×"],
        ["1", "2", "3", "−"],
        ["0", ".", "=", "+"],
        ["🧹 AC"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# -----------------------
# تقييم العملية
# -----------------------
def evaluate_expression(expr):
    try:
        expr = expr.replace("÷", "/").replace("×", "*").replace("−", "-")
        expr = re.sub(r'√\((.*?)\)', r'math.sqrt(\1)', expr)
        tokens = re.split(r'(\D)', expr)
        new_expr = ""
        for t in tokens:
            if t.isdigit():
                new_expr += f"Fraction({t})"
            else:
                new_expr += t
        result = eval(new_expr)
        return str(result)
    except:
        return "خطأ ❌"


# -----------------------
# start
# -----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id] = ""
    await update.message.reply_text(
        "🧮 PRO Calculator\n\n0",
        reply_markup=build_keyboard()
    )


# -----------------------
# استقبال الضغط
# -----------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_data:
        user_data[user_id] = ""

    if text == "🧹 AC":
        user_data[user_id] = ""
    elif text == "⌫":
        user_data[user_id] = user_data[user_id][:-1]
    elif text == "√":
        user_data[user_id] += "√("
    elif text == "𝑎⁄𝑏":
        user_data[user_id] += "/"
    elif text == "=":
        user_data[user_id] = evaluate_expression(user_data[user_id])
    else:
        user_data[user_id] += text

    result = user_data[user_id] if user_data[user_id] else "0"

    await update.message.reply_text(
        f"🧮 PRO Calculator\n\n{result}",
        reply_markup=build_keyboard()
    )


# -----------------------
# تشغيل البوت
# -----------------------
def main():
    TOKEN = os.getenv("8623573779:AAH4BuGTGJ1pFZQaYQ9nnLmo0KNjv7P_yDo")  # استخدم Environment Variable
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("PRO Calculator Running...")
    app.run_polling()


if __name__ == "__main__":
    main()