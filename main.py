import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, MenuButtonWebApp, WebAppInfo
from database import init_db, set_setting, get_setting, is_admin, add_admin, cursor, conn

TOKEN = "BOT_TOKENINGIZNI_SHU_YERGA_QO_YING"
WEBAPP_URL = "https://mansabov2010-jpg.github.io/grab-charakter/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

class AdminStates(StatesGroup):
    waiting_value = State()
    add_waifu_name = State()
    add_waifu_source = State()
    add_waifu_rarity = State()
    add_waifu_price = State()
    add_waifu_img = State()
    new_admin_id = State() # Yangi admin ID sini kiritish uchun

# Render 24/7 ishlashi uchun veb-server
async def health_check(request):
    return web.Response(text="Grab Character Bot 24/7 ishlamoqda!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonWebApp(
            text="💎",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📢 KANALIMIZ", url="https://t.me/kanal_havolasi"),
            InlineKeyboardButton(text="👥 GURUHIMIZ", url="https://t.me/guruh_havolasi")
        ]
    ])

    await message.answer(
        f"💎 <b>Gʀᴀʙ Cʜᴀʀᴀᴄᴛᴇʀ'ɢᴀ Xᴜꜱʜ Kᴇʟɪʙꜱɪᴢ!</b>\n\n"
        f"👋 Sᴀʟᴏᴍ, <b>{message.from_user.first_name}</b>!\n\n"
        f"🌟 Bᴜ ʙᴏᴛ ᴏʀǫᴀʟɪ ꜱᴇᴠɪᴍʟɪ ᴘᴇʀꜱᴏɴᴀᴊʟᴀﺭɴɪ ʏɪɢ'ɪɴɢ ᴠᴀ ɢᴜʀᴜʜʟᴀʀɴɪ ᴊᴏɴʟᴀɴᴛɪʀɪɴɢ!\n"
        f"✨ — — — — — — — — — ✨",
        parse_mode="HTML",
        reply_markup=kb
    )

# --- ADMIN PANEL (Faqat bazadagi adminlarira ochiladi) ---
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🪙 Tanga limiti", callback_data="set_tap_limit"),
         InlineKeyboardButton(text="⏳ Tiklanish vaqti", callback_data="set_tap_cooldown")],
        [InlineKeyboardButton(text="🎁 Kunlik sovg'a", callback_data="set_daily_reward")],
        [InlineKeyboardButton(text="📢 Reklama matni", callback_data="set_ad_text"),
         InlineKeyboardButton(text="🎯 Reklama tugmasi", callback_data="set_ad_trigger")],
        [InlineKeyboardButton(text="🎨 Fon xiraligi (Blur)", callback_data="set_bg_blur"),
         InlineKeyboardButton(text="🔵 Ko'k rang ochligi", callback_data="set_blue_shade")],
        [InlineKeyboardButton(text="📊 Drop foizlari", callback_data="set_drop_basic")],
        [InlineKeyboardButton(text="➕ Waifu qo'shish", callback_data="add_waifu")],
        [InlineKeyboardButton(text="🛡️ Yangi Admin qo'shish", callback_data="add_new_admin")] # Alohida bo'lim
    ])
    await message.answer("⚙️ <b>To'liq Boshqaruv Paneli:</b>", parse_mode="HTML", reply_markup=kb)

# Yangi admin qo'shish tugmasi bosilganda
@dp.callback_query(F.data == "add_new_admin")
async def start_add_admin(call: types.CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return
    await state.set_state(AdminStates.new_admin_id)
    await call.message.answer("🛡️ Yangi adminning Telegram ID raqamini yuboring:")

@dp.message(AdminStates.new_admin_id)
async def save_new_admin(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    try:
        new_id = int(message.text.strip())
        add_admin(new_id)
        await state.clear()
        await message.answer(f"✅ <code>{new_id}</code> ID raqamli foydalanuvchi muvaffaqiyatli <b>Admin</b> etib tayinlandi!", parse_mode="HTML")
    except ValueError:
        await message.answer("❌ Xato! Faqat raqamlardan iborat Telegram ID kiriting:")

@dp.callback_query(F.data.startswith("set_"))
async def ask_setting_value(call: types.CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return
    key = call.data.replace("set_", "")
    await state.update_data(setting_key=key)
    await state.set_state(AdminStates.waiting_value)
    await call.message.answer(f"✏️ <b>{key}</b> uchun yangi qiymat yuboring (Hozirgi: <code>{get_setting(key)}</code>):", parse_mode="HTML")

@dp.message(AdminStates.waiting_value)
async def save_setting_value(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    data = await state.get_data()
    set_setting(data["setting_key"], message.text)
    await state.clear()
    await message.answer("✅ Sozlama yangilandi!")

@dp.callback_query(F.data == "add_waifu")
async def start_add_waifu(call: types.CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return
    await state.set_state(AdminStates.add_waifu_name)
    await call.message.answer("1️⃣ Waifu ismini kiriting:")

@dp.message(AdminStates.add_waifu_name)
async def w_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AdminStates.add_waifu_source)
    await message.answer("2️⃣ Manbasini kiriting (Anime yoki o'yin):")

@dp.message(AdminStates.add_waifu_source)
async def w_source(message: types.Message, state: FSMContext):
    await state.update_data(source=message.text)
    await state.set_state(AdminStates.add_waifu_rarity)
    await message.answer("3️⃣ Darajasini kiriting (Basic, Rare, Divine, Season):")

@dp.message(AdminStates.add_waifu_rarity)
async def w_rarity(message: types.Message, state: FSMContext):
    await state.update_data(rarity=message.text)
    await state.set_state(AdminStates.add_waifu_price)
    await message.answer("4️⃣ Narxini kiriting (raqamda):")

@dp.message(AdminStates.add_waifu_price)
async def w_price(message: types.Message, state: FSMContext):
    await state.update_data(price=int(message.text))
    await state.set_state(AdminStates.add_waifu_img)
    await message.answer("5️⃣ Rasm havolasini (URL) yuboring:")

@dp.message(AdminStates.add_waifu_img)
async def w_img(message: types.Message, state: FSMContext):
    d = await state.get_data()
    cursor.execute("INSERT INTO waifus (name, source, rarity, price, image_url) VALUES (?, ?, ?, ?, ?)",
                   (d['name'], d['source'], d['rarity'], d['price'], message.text))
    conn.commit()
    await state.clear()
    await message.answer(f"✅ <b>{d['name']}</b> bazaga qo'shildi!", parse_mode="HTML")

async def main():
    init_db()
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
