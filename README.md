# DISCORD-MONEY-BOT

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

An intelligent, conversational bot that helps you manage your personal finances directly from your Discord server. Powered by Python and Wit.ai for Natural Language Understanding.

---

## ✨ Key Features

* **💬 Conversational Interface**: Interact with the bot using natural language (e.g., "I spent $15 on lunch") instead of rigid commands.
* **🤖 Dual Interaction Mode**: Supports both conversational messages and traditional `!` commands for flexibility.
* **💾 Persistent Data Storage**: All transactions and balances are saved to a local `JSON` file, so your data is never lost on restart.
* **📊 Financial Tracking**: Easily log expenses and income, check your current balance, and view a history of your latest transactions.
* **🔐 Secure & Configurable**: Sensitive information like API tokens is kept secure and separate from the code using a `.env` file.
* **🎯 Channel Specific**: The bot is designed to listen only in a designated channel to avoid spam.

---

## 🛠️ Tech Stack

This project was built using the following technologies:

<p align="left">
  <a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
  <a href="https://discordpy.readthedocs.io/en/latest/" target="_blank"> <img src="https://i.imgur.com/s2h4c29.png" alt="discordpy" width="40" height="40"/> </a>
  <a href="https://wit.ai/" target="_blank"> <img src="https://i.imgur.com/aK4a12C.png" alt="witai" width="40" height="40"/> </a>
</p>

* **Python**: The core programming language.
* **discord.py**: A modern, easy-to-use, feature-rich, and async-ready API wrapper for Discord.
* **Wit.ai**: A Natural Language Understanding (NLU) platform from Meta used to process conversational messages.
* **Requests**: For making API calls to Wit.ai.
* **Dotenv**: For managing environment variables securely.

---

## 🚀 Getting Started

Follow these steps to get a local copy up and running.

### Prerequisites

* Python 3.10 or higher
* A Discord account and a created Bot application.
* A Wit.ai account and a trained app.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MCarlos7/DISCORD-MONEY-BOT.git
    ```

2.  **Install Python packages:**
    Create a `requirements.txt` file with the necessary libraries and run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**
    Create a file named `.env` in the root of the project and fill it with your credentials. Use the `.env.example` file as a template.
    ```env
    # .env file
    TOKEN="YOUR_DISCORD_BOT_TOKEN"
    CANAL_PERMITIDO_ID="YOUR_DISCORD_CHANNEL_ID"
    WIT_AI_TOKEN="YOUR_WIT.AI_SERVER_ACCESS_TOKEN"
    ```

4.  **Train your Wit.ai App:**
    Make sure your Wit.ai app is trained with the following intents and entities as described in the development process:
    * **Intents**: `registrar_gasto`, `registrar_ingreso`, `consultar_saldo`, `ver_historial`.
    * **Entities**: `wit/amount_of_money`, `descripcion:descripcion`.

5.  **Run the bot:**
    ```bash
    python your_bot_file_name.py
    ```

---

## 💻 Usage

You can interact with the bot in two main ways:

#### 1. Conversational Messages
Simply talk to the bot in the designated channel.

> `I just received $1500 for my salary`
> `how much money do I have left?`
> `show me my recent transactions`

#### 2. Traditional Commands
For quick and precise actions, you can still use commands.

> `!gasto 25.50 Coffee and donut`
> `!ingreso 100 Gift from a friend`
> `!saldo`
> `!historial`
> `!ayuda`

---
Project Link: https://github.com/MCarlos7/DISCORD-MONEY-BOT.git
