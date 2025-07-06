import os
import asyncio
import datetime
import matplotlib.pyplot as plt
import io

from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes
)

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from utils import format_rp, filter_transaksi_by_date, rekapkan

# Konfigurasi Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet_transaksi = client.open("CATATAN KEUANGAN").worksheet("Transaksi")

# Fungsi pengecekan user
def is_registered(user_id):
    return True  # sementara aktif semua

# Command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_registered(update.effective_user.id):
        await update.message.reply_text("🚫 Kamu belum terdaftar. Silakan isi formulir pendaftaran.")
        return
    await update.message.reply_text("👋 Selamat datang di Dompet Tracker Bot!")

# Fungsi utama bot
async def main():
    TOKEN = os.getenv("7570088814:AAFcLOdNuGGNurkVfh55BqZUbD8NsH2b-ww") or "ISI_TOKEN_DISINI"
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot berjalan...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
