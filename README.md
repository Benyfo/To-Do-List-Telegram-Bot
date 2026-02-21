# To-Do-List-Telegram-Bot

A production-ready Telegram bot built with Python for managing personal to-do lists.  
It supports task creation, listing, deletion, basic statistics, backup functionality, and an interactive **Tic Tac Toe** game.

Built using `python-telegram-bot`, Flask, and SQLAlchemy with SQLite persistent storage.

---

## 📸 Bot Preview

![@ToDooList_bot pic](https://github.com/user-attachments/assets/603959d1-fee0-4e65-97c5-19f6dd5b162d)

---

## 🌍 Live Demo

The bot is deployed and running in production.

🌐 Website:  
- https://benyfo.ir  

🚀 Webhook Endpoint:  
- https://benyfo.ir/ToDooList_Bot/

🤖 Telegram Bot:  
- https://t.me/ToDooList_bot  
- Username: `@ToDooList_bot`

You can visit the website or open the Telegram link to start using the bot immediately.

---

## 💡 Feedback & Contributions

Have an idea to improve the bot?

- Open an Issue in this repository
- Submit a Pull Request
 
 Or contact me directly:

📧 **benyaminforooghi@gmail.com**

I actively maintain this project and plan to release new updates and improved versions over time.

---

## 🚀 Features

- ✅ Add new tasks
- 📑 List all tasks
- 📅 View today's tasks
- 📊 Simple productivity statistics
- ⚠️ Clear all tasks
- 💾 Backup tasks (text export)
- 🌍 Language system (extensible)
- 🎮 Built-in Tic Tac Toe game
- 🗄 Persistent storage using SQLite

## 🏗 Project Architecture

- Telegram Bot API (Webhook mode)
- Flask server for handling webhook requests
- SQLAlchemy ORM for database management
- SQLite database (`todo.db`)
- Deployable on cPanel (Passenger WSGI supported)

## 📦 Requirements

- Python 3.9+
- cPanel hosting with Python support
- Domain with SSL certificate (HTTPS required for webhook)

## 🔧 Installation (Local Development – Polling Mode)

```bash
git clone https://github.com/yourusername/To-Do-List-Telegram-Bot.git
cd To-Do-List-Telegram-Bot
```

## 🚀 Local Development Setup

### 1️⃣ Install Dependencies

```Bash
pip install -r requirements.txt
```

###  2️⃣ Create a .env File

```env
BOT_TOKEN=your_telegram_bot_token
```

### 3️⃣ Run the Bot

```bash
python run_bot.py
```

## 🌐 Production Deployment (cPanel + Webhook)

### 1️⃣ Hosting Requirements

- cPanel with Python application support
- SSL enabled (HTTPS is mandatory for Telegram webhooks)
- Example domain:   ```https://yourdomain.com/ToDooList_Bot/```

### 2️⃣ Upload Files

Upload these files to your hosting directory:

- app.py
- database.py
- passenger_wsgi.py
- requirements.txt
- .gitignore
- README.md
- LICENSE

### ⚠️ Do NOT upload:

- .env
- todo.db
- __pycache__/


### 3️⃣ Install Dependencies (cPanel Terminal)
```bash
pip install -r requirements.txt
```
### 4️⃣ Set Environment Variables

In __cPanel__ → __Setup Python App__ → __Environment Variables:__
```
BOT_TOKEN = your_token_here
```
### 5️⃣ Configure Webhook

Webhook URL format:

```code
https://yourdomain.com/your_path/webhook/YOUR_BOT_TOKEN
```
## 📁 Project StructureTo-Do-List-Telegram-Bot/

```code
│
├── app.py               # Flask application for Webhook mode
├── database.py          # Database models and session management
├── run_bot.py           # Polling script for local development
├── passenger_wsgi.py    # Entry point for cPanel hosting
├── requirements.txt     # Python dependencies
├── .gitignore           # Version control ignore list
├── README.md            # Documentation
└── LICENSE              # MIT License
```
## 🔐 Security Notes

- Never commit .env: Keeps your credentials private.
- Never expose your bot token: Revoke it immediately via @BotFather if leaked.
- Never push todo.db: Avoid overwriting production data with local tests.
- Always use HTTPS: Telegram will not send data to insecure HTTP endpoints.

## 📌 Future Improvements

 - PDF backup export: Professional formatted reports.
 - Task categories: Tagging and filtering (Work, Personal, etc.).
 - Multi-language: Support for more global languages.
 - Admin dashboard: Web-based interface for bot management.

## ⭐ Support

If you found this project helpful:

- ⭐ Star this repository
- 🍴 Fork it to add your own flair
- 🛠 Contribute improvements via Pull Requests
  
## 📜 License

This project is licensed under the MIT License.

---

## 🙌 Thank You

Thank you for taking the time to read this README.

If you found this project useful, consider giving it a ⭐ and sharing it with others.
