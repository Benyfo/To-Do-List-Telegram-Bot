import os
import logging
import random
from flask import Flask, request
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

application = ApplicationBuilder().token(TOKEN).build()

import asyncio
asyncio.run(application.initialize())

main_menu = ReplyKeyboardMarkup([
    ["📑 List", "📝 Add"],
    ["📅 Today", "📊 Stats"],
    ["⚠️ Clear", "💾 Backup"],
    ["❓ Help", "🌍 Language"],
    ["🎮 Tic Tac Toe"]
], resize_keyboard=True)

HELP_TEXT = """
دستورها:
/start          - شروع و نمایش منو
/help           - نمایش این راهنما
/add <متن>      - اضافه کردن تسک (مثال: /add خرید نان)
/list           - دیدن تمام تسک‌ها
/today          - نمایش تسک‌های امروز
/stats          - آمار ساده (تعداد تسک‌ها)
/clear          - پاک کردن همه تسک‌ها
/backup         - پشتیبان‌گیری (فعلاً متن)
/language       - تغییر زبان (فعلاً فقط فارسی)
/start_ttt      - شروع بازی دوز
"""

tasks = {}          

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! من ربات ToDo شما هستم ✅\n" + HELP_TEXT,
        reply_markup=main_menu
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT, reply_markup=main_menu)

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    task_text = ' '.join(context.args).strip()
    if not task_text:
        await update.message.reply_text("لطفاً متن تسک را بعد از /add بنویسید\nمثال: /add خرید نان و شیر")
        return

    if user_id not in tasks:
        tasks[user_id] = []
    tasks[user_id].append(task_text)

    await update.message.reply_text(f"تسک اضافه شد ✅\n{task_text}\n\nتعداد کل تسک‌ها: {len(tasks[user_id])}")

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in tasks or not tasks[user_id]:
        await update.message.reply_text("شما هنوز هیچ تسکی اضافه نکردید!")
        return

    task_list = "\n".join([f"• {i+1}. {task}" for i, task in enumerate(tasks[user_id])])
    await update.message.reply_text(f"لیست تمام تسک‌ها:\n{task_list}")

async def today_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in tasks or not tasks[user_id]:
        await update.message.reply_text("هیچ تسکی برای امروز ندارید!")
        return

    task_list = "\n".join([f"• {task}" for task in tasks[user_id]])
    await update.message.reply_text(f"تسک‌های امروز:\n{task_list}")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    total = len(tasks.get(user_id, []))
    await update.message.reply_text(
        f"آمار بهره‌وری شما:\n"
        f"تعداد کل تسک‌ها: {total}\n"
        f"تسک‌های امروز: {total} (فعلاً همه تسک‌ها)"
    )

async def clear_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in tasks:
        del tasks[user_id]
    await update.message.reply_text("تمام تسک‌های شما پاک شد ✅")

async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in tasks or not tasks[user_id]:
        await update.message.reply_text("هیچ تسکی برای پشتیبان‌گیری وجود ندارد!")
        return

    task_list = "\n".join([f"• {task}" for task in tasks[user_id]])
    await update.message.reply_text(
        f"پشتیبان تسک‌ها (متن ساده):\n\n{task_list}\n\n"
        f"در آینده به صورت PDF ارسال خواهد شد."
    )

async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("در حال حاضر فقط زبان فارسی پشتیبانی می‌شود.\nگزینه‌های دیگر بعداً اضافه خواهد شد.")

# Tic Tac Toe
games = {}

async def tic_tac_toe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    board = [" "] * 9
    games[user_id] = board
    keyboard = build_board_keyboard(board)
    await update.message.reply_text("شروع بازی Tic Tac Toe ✅ شما X هستید", reply_markup=keyboard)

def build_board_keyboard(board):
    keys = []
    for i in range(0, 9, 3):
        row = [InlineKeyboardButton(board[i+j] if board[i+j] != " " else "➖", callback_data=str(i+j)) for j in range(3)]
        keys.append(row)
    return InlineKeyboardMarkup(keys)

async def ttt_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    board = games.get(user_id)
    if not board:
        await query.answer("ابتدا /start_ttt بزن")
        return
    pos = int(query.data)
    if board[pos] != " ":
        await query.answer("این خانه پر است")
        return
    board[pos] = "X"
    if check_winner(board, "X"):
        await query.edit_message_text("شما بردید 🎉", reply_markup=build_board_keyboard(board))
        games.pop(user_id, None)
        return
    empty = [i for i, v in enumerate(board) if v == " "]
    if empty:
        bot_move = random.choice(empty)
        board[bot_move] = "O"
        if check_winner(board, "O"):
            await query.edit_message_text("ربات برد 😢", reply_markup=build_board_keyboard(board))
            games.pop(user_id, None)
            return
    await query.edit_message_text("بازی Tic Tac Toe", reply_markup=build_board_keyboard(board))

def check_winner(b, p):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    return any(b[i]==b[j]==b[k]==p for i,j,k in wins)

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("add", add_task))
application.add_handler(CommandHandler("list", list_tasks))
application.add_handler(CommandHandler("today", today_tasks))
application.add_handler(CommandHandler("stats", stats))
application.add_handler(CommandHandler("clear", clear_tasks))
application.add_handler(CommandHandler("backup", backup))
application.add_handler(CommandHandler("language", language))
application.add_handler(CommandHandler("start_ttt", tic_tac_toe))
application.add_handler(CallbackQueryHandler(ttt_callback))

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("دستور نامعتبر!\nاز منو استفاده کن یا /help بزن.")

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

@app.route(f'/webhook/{TOKEN}', methods=['POST'])
async def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        if update:
            await application.process_update(update)
        return 'ok', 200
    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)
        return 'error', 500

@app.route('/')
def home():
    return "@ToDooList_bot in telegram is running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)