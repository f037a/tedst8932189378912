from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
import paramiko
from wakeonlan import send_magic_packet

# Введите сюда токен вашего бота
TOKEN = '7584275912:AAHHHXshG0ba2z1RoxyJp4tUoBjOxX3ImQk'
# Данные для подключения по SSH
SSH_HOST = '192.168.1.104'
SSH_PORT = 2222  # Новый порт, который перенаправляется на 22
SSH_USER = 'admin'
SSH_PASSWORD = '0000'
MAC_ADDRESS = 'A8-A1-59-F2-EE-A1'  # Ваш MAC-адрес

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Привет! Я бот для включения и выключения компьютера.')

async def turn_on(update: Update, context: CallbackContext):
    send_magic_packet(MAC_ADDRESS)
    await update.message.reply_text(f'Компьютер с MAC-адресом {MAC_ADDRESS} включается...')

async def turn_off(update: Update, context: CallbackContext):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)
        
        ssh_client.exec_command('shutdown /s /t 1')
        await update.message.reply_text('Компьютер выключается...')
        ssh_client.close()
    except Exception as e:
        await update.message.reply_text(f'Ошибка при попытке выключить компьютер: {e}')

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("turn_on", turn_on))
    app.add_handler(CommandHandler("turn_off", turn_off))

    app.run_polling()

if __name__ == '__main__':
    main()
