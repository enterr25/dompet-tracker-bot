import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
import os

# =================== KONFIG ===================
SCOPES = ['https://www.googleapis.com/auth/drive']
TEMPLATE_SHEET_ID = '1HX5qLaN6Ush86qg4g_bMOBRHKPtCuUMTzgLLlE6ho'
ADMIN_ID = 383820856
GOOGLE_FORM_LINK = 'https://docs.google.com/forms/d/e/1FAIpQLScovQbSOQrbJqeD-vcUGDH6vk5My-JeoM3qkgfcAK6LOTbegA/viewform'

# =================== AUTENTIKASI ===================
creds = service_account.Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
gc = gspread.authorize(creds)
drive_service = build('drive', 'v3', credentials=creds)

# =================== MULTI-USER ===================
def save_user_sheet_id(user_id, sheet_id):
    data = {}
    if os.path.exists("user_data.json"):
        with open("user_data.json", "r") as f:
            data = json.load(f)
    data[str(user_id)] = sheet_id
    with open("user_data.json", "w") as f:
        json.dump(data, f)

def get_user_sheet_id(user_id):
    if os.path.exists("user_data.json"):
        with open("user_data.json", "r") as f:
            data = json.load(f)
        return data.get(str(user_id))
    return None

def duplicate_template_for_user(user_id):
    new_title = f"CATATAN_KEUANGAN_{user_id}"
    copied_file = drive_service.files().copy(
        fileId=TEMPLATE_SHEET_ID,
        body={"name": new_title}
    ).execute()
    return copied_file["id"]

# =================== HANDLER ===================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    sheet_id = get_user_sheet_id(user_id)

    if not sheet_id:
        await update.message.reply_text(
            f"🚫 Kamu belum terdaftar.\n\nSilakan isi formulir ini untuk aktivasi:\n{GOOGLE_FORM_LINK}"
        )
        return

    keyboard = [
        [InlineKeyboardButton("➕ Catat Transaksi", callback_data="catat")],
        [InlineKeyboardButton("📊 Rekap", callback_data="rekap"), InlineKeyboardButton("📅 Laporan", callback_data="laporan")],
        [InlineKeyboardButton("💼 Rekening", callback_data="rekening"), InlineKeyboardButton("📂 Kategori", callback_data="kategori")],
        [InlineKeyboardButton("📤 Export", callback_data="export"), InlineKeyboardButton("🧠 Saldo", callback_data="saldo")],
        [InlineKeyboardButton("🔍 Cari", callback_data="cari"), InlineKeyboardButton("🗑️ Hapus", callback_data="hapus")],
        [InlineKeyboardButton("⏰ Pengingat (OFF)", callback_data="pengingat")],
        [InlineKeyboardButton("📈 Grafik", callback_data="grafik")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Menu Utama:", reply_markup=reply_markup)

async def idku(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(f"🆔 ID Telegram kamu: `{user_id}`", parse_mode="Markdown")

async def aktivasi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("🚫 Kamu bukan admin.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Format: /aktivasi <user_id>")
        return

    target_id = int(context.args[0])
    if get_user_sheet_id(target_id):
        await update.message.reply_text("✅ User ini sudah aktif.")
        return

    sheet_id = duplicate_template_for_user(target_id)
    save_user_sheet_id(target_id, sheet_id)
    await update.message.reply_text(
        f"✅ User {target_id} sudah diaktifkan.\nSheet: https://docs.google.com/spreadsheets/d/{sheet_id}"
    )

# =================== SETUP BOT ===================
async def main():
    app = Application.builder().token("7570088814:AAFcLOdNuGGNurkVfh55BqZUbD8NsH2b-ww").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("idku", idku))
    app.add_handler(CommandHandler("aktivasi", aktivasi))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
