import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, MessageHandler, filters)
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import matplotlib.pyplot as plt
import io

# Konfigurasi Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Konfigurasi Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet_transaksi = client.open("CATATAN KEUANGAN").worksheet("Transaksi")
sheet_rekening = client.open("CATATAN KEUANGAN").worksheet("Rekening")
sheet_kategori = client.open("CATATAN KEUANGAN").worksheet("Kategori")

# ===================== HANDLER =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Catat Transaksi", callback_data='catat')],
        [InlineKeyboardButton("Rekap", callback_data='rekap')],
        [InlineKeyboardButton("Laporan", callback_data='laporan')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Halo! Ini bot pencatat keuangan kamu 📝', reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'catat':
        await query.edit_message_text("Ketik format transaksi: jumlah, masuk/keluar, kategori, rekening, catatan")
    elif query.data == 'rekap':
        await query.edit_message_text("Rekap belum tersedia.")
    elif query.data == 'laporan':
        await query.edit_message_text("Laporan belum tersedia.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        jumlah, jenis, kategori, rekening, catatan = [x.strip() for x in text.split(',')]
        tanggal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet_transaksi.append_row([tanggal, jumlah, jenis, kategori, rekening, catatan])
        await update.message.reply_text("✅ Transaksi dicatat!")
    except Exception as e:
        logger.error(f"Error parsing message: {e}")
        await update.message.reply_text("Format salah. Gunakan: jumlah, masuk/keluar, kategori, rekening, catatan")

# ===================== MAIN =======================
async def main():
    app = Application.builder().token("7570088814:AAFcLOdNuGGNurkVfh55BqZUbD8NsH2b-ww").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
