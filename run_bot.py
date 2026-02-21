from app import application as telegram_app

if __name__ == "__main__":
    print("ToDo List Bot started (Polling)...")
    telegram_app.run_polling()