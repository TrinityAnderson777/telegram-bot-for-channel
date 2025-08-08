
# README на русском

## Описание

Этот бот для Telegram предназначен для автоматической модерации сообщений. Он позволяет пользователю отправить сообщение, которое затем подтверждается через кнопку. После подтверждения сообщение пересылается модераторам в приватные сообщения (ЛС). Модераторы могут одобрить или отклонить сообщение, нажав соответствующие кнопки.

## Как работает

- Пользователь отправляет сообщение боту.
- Бот предлагает подтвердить отправку этого сообщения на модерацию.
- После подтверждения бот пересылает сообщение всем модераторам, которые находятся в указанной группе с правами администратора.
- Модераторы получают сообщение с двумя кнопками: **"Одобрить"** и **"Отклонить"**.
- При нажатии кнопки бот регистрирует решение модератора и выводит соответствующее сообщение.

## Как настроить

1. Вставьте ваш токен бота в переменную `TOKEN`.
2. Укажите ID группы с модераторами в переменной `MODERATION_CHAT_ID`. Это должна быть группа, где есть администраторы.
3. Запустите скрипт.
4. В Telegram отправьте команду `/start` или любое сообщение, и бот предложит подтвердить его отправку.
5. Модераторы, получив сообщение, могут одобрить или отклонить его.

## Установка

- Установите необходимые библиотеки:

BASH
pip install python-telegram-bot



- Запустите скрипт:

BASH
python ваш_скрипт.py


---

# README in English

## Description

This Telegram bot is designed for automatic message moderation. It allows a user to send a message, which is then confirmed via inline buttons. After confirmation, the message is forwarded to moderators via private messages. Moderators can approve or reject the message by clicking the corresponding buttons.

## How it works

- The user sends a message to the bot.
- The bot prompts to confirm sending this message for moderation.
- Upon confirmation, the bot sends the message to all moderators (admins of a specific group) in private messages.
- Moderators receive the message with two inline buttons: **"Approve"** and **"Reject"**.
- When a moderator clicks a button, the bot records the decision and displays an appropriate message.

## Setup instructions

1. Insert your bot token into the `TOKEN` variable.
2. Specify the moderator chat ID (the group where moderators are) in `MODERATION_CHAT_ID`. This should be the ID of a group where you have admins.
3. Run the script.
4. Send any message to the bot, and it will ask for confirmation.
5. Moderators will receive the message and can approve or reject it.

## Installation

- Install required libraries:

BASH
pip install python-telegram-bot


- Run the script:

BASH
python your_script.py


---
