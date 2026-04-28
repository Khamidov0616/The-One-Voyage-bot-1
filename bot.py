import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8652719743:AAEvLMvUXi3-RKgkLhJIEHKKin9BOY4j0jE"
BOOKING_URL = "https://www.booking.com/index.html?aid=304142"
AVIASALES_URL = "https://www.aviasales.uz/?params=TAS1"
ADMIN = "@khamidov_0616"

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

PRICES = [
    {"nomi": "🇹🇷 Turkiya - Antaliya", "narx": "$450/kishi", "izoh": "7 kecha, All Inclusive"},
    {"nomi": "🇦🇪 Dubay", "narx": "$680/kishi", "izoh": "5 kecha, Nonushta"},
    {"nomi": "🇪🇬 Misr - Sharm el-Shayx", "narx": "$520/kishi", "izoh": "6 kecha, All Inclusive"},
    {"nomi": "🇹🇭 Tailand - Phuket", "narx": "$750/kishi", "izoh": "7 kecha, Nonushta"},
    {"nomi": "🇮🇹 Italiya - Rim", "narx": "$1100/kishi", "izoh": "5 kecha, B&B"},
    {"nomi": "🚗 Transfer - Dubay", "narx": "$25/kishi", "izoh": "Aeroport - mehmonxona"},
    {"nomi": "🚗 Transfer - Antaliya", "narx": "$15/kishi", "izoh": "Aeroport - mehmonxona"},
]

user_lang = {}

def lang(uid): return user_lang.get(uid, 'uz')

def main_kb(uid):
    uz = lang(uid) == 'uz'
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏨 " + ("Mehmonxona" if uz else "Отель"), callback_data='hotel'),
         InlineKeyboardButton("🚗 " + ("Transfer" if uz else "Трансфер"), callback_data='transfer')],
        [InlineKeyboardButton("✈️ " + ("Aviabilet" if uz else "Авиабилет"), callback_data='flights'),
         InlineKeyboardButton("💰 " + ("Narxlar" if uz else "Цены"), callback_data='price')],
        [InlineKeyboardButton("📦 " + ("Tur paket" if uz else "Тур пакет"), callback_data='package'),
         InlineKeyboardButton("📞 " + ("Bog'lanish" if uz else "Связаться"), callback_data='contact')],
        [InlineKeyboardButton("🌐 Til / Язык", callback_data='language')],
    ])

def back_kb(uid):
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ " + ("Orqaga" if lang(uid)=='uz' else "Назад"), callback_data='menu')]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    uz = lang(uid) == 'uz'
    text = "✈️ *The One Voyage* ga xush kelibsiz!\n\nQuyidagi bo'limdan birini tanlang 👇" if uz else "✈️ Добро пожаловать в *The One Voyage*!\n\nВыберите раздел 👇"
    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=main_kb(uid))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    uz = lang(uid) == 'uz'
    d = q.data

    if d == 'menu':
        text = "✈️ *The One Voyage* ga xush kelibsiz!\n\nQuyidagi bo'limdan birini tanlang 👇" if uz else "✈️ Добро пожаловать в *The One Voyage*!\n\nВыберите раздел 👇"
        await q.edit_message_text(text, parse_mode='Markdown', reply_markup=main_kb(uid))

    elif d == 'language':
        await q.edit_message_text("🌐 Tilni tanlang / Выберите язык:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🇺🇿 O'zbek", callback_data='lang_uz'),
             InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')]]))

    elif d == 'lang_uz':
        user_lang[uid] = 'uz'
        await q.edit_message_text("✅ Til o'zgartirildi!\n\n✈️ *The One Voyage* ga xush kelibsiz!\n\nQuyidagi bo'limdan birini tanlang 👇", parse_mode='Markdown', reply_markup=main_kb(uid))

    elif d == 'lang_ru':
        user_lang[uid] = 'ru'
        await q.edit_message_text("✅ Язык изменён!\n\n✈️ Добро пожаловать в *The One Voyage*!\n\nВыберите раздел 👇", parse_mode='Markdown', reply_markup=main_kb(uid))

    elif d == 'hotel':
        text = f"🏨 *Mehmonxona qidirish*\n\n1️⃣ Booking.com da qidiring 👇\n2️⃣ Yoki admin ga yozing: {ADMIN}\n\n📍 Shahar\n📅 Kirish/Chiqish\n👥 Mehmonlar soni" if uz else f"🏨 *Поиск отеля*\n\n1️⃣ Найдите на Booking.com 👇\n2️⃣ Или напишите: {ADMIN}\n\n📍 Город\n📅 Даты\n👥 Гостей"
        await q.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏨 Booking.com", url=BOOKING_URL)],
            [InlineKeyboardButton("⬅️ " + ("Orqaga" if uz else "Назад"), callback_data='menu')]]))

    elif d == 'flights':
        text = f"✈️ *Aviabilet qidirish*\n\n1️⃣ Aviasales da qidiring 👇\n2️⃣ Yoki admin: {ADMIN}" if uz else f"✈️ *Авиабилеты*\n\n1️⃣ Найдите на Aviasales 👇\n2️⃣ Или admin: {ADMIN}"
        await q.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✈️ Aviasales", url=AVIASALES_URL)],
            [InlineKeyboardButton("⬅️ " + ("Orqaga" if uz else "Назад"), callback_data='menu')]]))

    elif d == 'transfer':
        text = f"🚗 *Transfer qidirish*\n\n📍 Qayerdan\n📍 Qayerga\n📅 Sana va vaqt\n👥 Yo'lovchilar soni\n\n_Misol: Dubay aeroport → Atlantis, 10-iyun 14:00, 2 kishi_\n\nAdmin: {ADMIN}" if uz else f"🚗 *Поиск трансфера*\n\n📍 Откуда\n📍 Куда\n📅 Дата и время\n👥 Пассажиров\n\nАдмин: {ADMIN}"
        await q.edit_message_text(text, parse_mode='Markdown', reply_markup=back_kb(uid))

    elif d == 'price':
        text = "💰 *Joriy narxlar:*\n\n" if uz else "💰 *Актуальные цены:*\n\n"
        for p in PRICES:
            text += f"🔹 *{p['nomi']}*\n   💵 {p['narx']}\n   _{p['izoh']}_\n\n"
        text += f"\n📞 Bron: {ADMIN}" if uz else f"\n📞 Бронирование: {ADMIN}"
        await q.edit_message_text(text, parse_mode='Markdown', reply_markup=back_kb(uid))

    elif d == 'package':
        text = f"📦 *Tur paket*\n\nTur paketlar haqida ma'lumot uchun:\n\n👤 {ADMIN}\n🕐 10:00 - 22:00" if uz else f"📦 *Тур пакет*\n\nДля информации:\n\n👤 {ADMIN}\n🕐 10:00 - 22:00"
        await q.edit_message_text(text, parse_mode='Markdown', reply_markup=back_kb(uid))

    elif d == 'contact':
        text = f"📞 *Bog'lanish*\n\n👤 {ADMIN}\n🕐 10:00 - 22:00\n\nBemalol yozing! 😊" if uz else f"📞 *Связаться*\n\n👤 {ADMIN}\n🕐 10:00 - 22:00\n\nПишите! 😊"
        await q.edit_message_text(text, parse_mode='Markdown', reply_markup=back_kb(uid))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    uz = lang(uid) == 'uz'
    text = f"✅ *So'rovingiz qabul qilindi!*\n\nAdmin tez orada bog'lanadi: {ADMIN}" if uz else f"✅ *Запрос принят!*\n\nАдмин свяжется с вами: {ADMIN}"
    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=main_kb(uid))

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot ishga tushdi!")
    app.run_polling(drop_pending_updates=True)
