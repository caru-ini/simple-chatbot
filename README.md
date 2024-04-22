# SIMPLE-CHATBOT

>[!WARNING]
>This project is still in development and is not ready for use.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

A simple chatbot using OPENAI API for Discord.

### Features

- Chatting
- Summarization
- Question Answering

## Table of Contents

- [SIMPLE-CHATBOT](#simple-chatbot)
  - [Description](#description)
    - [Features](#features)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [1. Clone the repository](#1-clone-the-repository)
    - [2. Create and activate a virtual environment (optional)](#2-create-and-activate-a-virtual-environment-optional)
      - [Create a venv](#create-a-venv)
    - [Activate the venv](#activate-the-venv)
    - [3. Install the dependencies](#3-install-the-dependencies)
    - [4. Configuration](#4-configuration)
    - [5. Invite the bot to your server](#5-invite-the-bot-to-your-server)
    - [6. Run the bot](#6-run-the-bot)
    - [7. Sync commands](#7-sync-commands)
  - [Usage](#usage)
    - [Commands](#commands)
  - [Acknowledgements](#acknowledgements)
  - [License](#license)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/caru_ini/simple-chatbot.git
```

### 2. Create and activate a virtual environment (optional)

#### Create a venv

```bash
python -m venv venv
```

### Activate the venv

Linux/MacOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Configuration

Copy the `.env.example` file to `.env` and fill in the necessary information.

```bash
cp .env.example .env
```

### 5. Invite the bot to your server

### 6. Run the bot

```bash
python main.py
```

### 7. Sync commands

Execute this command in your server to sync the commands.

```plaintext
!sync *
```

## Usage

```bash
python main.py
```

### Commands

- `/chat <message> <window>` - Chat with the bot
  - `message` - The message to send
  - `window` - The number of messages to consider
- `/summary` - Summarize channel messages
  - `window` - The number of messages to consider
- `/ask <question>` - Ask a question (no context)
  - `question` - The question to ask
- `/auto_reply <enabled>` - Enable or disable auto-reply
  - `enabled` - `True` or `False` (empty to toggle)
- `/purge <limit>` - Purge messages (owner only)
  - `limit` - The number of messages to delete

## TODO

- [ ] Add web search feature
- [ ] Add image support
- [ ] Add i8n support

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgements

The author shall not be liable for any damages caused by this repository.

## License

This project is licensed under the [MIT License](LICENSE).
