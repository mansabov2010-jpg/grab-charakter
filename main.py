import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# 1. Tokeningizni shu yerga to'g'ridan-to'g'ri yozasiz
BOT_TOKEN = "9111857366:AAHx321dtWgJvO5zindpzWIY_1iWq4mgjlc"

# 2. Bot va Dispatcher ni sozlaymiz
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# 3. Tugmalarni yasash funksiyasi
def get_start_keyboard():
  keyboard = InlineKeyboardMarkup(
      inline_keyboard=[
          [
              InlineKeyboardButton(
                  text="📢 ᴋᴀɴᴀʟɪᴍɪᴢ", url="https://t.me/kanal_linki"
              ),
              InlineKeyboardButton(
                  text="👥 ɢᴜʀᴜʜɪᴍɪᴢ", url="https://t.me/guruh_linki"
              ),
          ],
          [
              InlineKeyboardButton(
                  text="🚀 ᴍɪɴɪ ɪʟᴏᴠᴀ",
                  web_app=types.WebAppInfo(url="https://mansabov2010-jpg.github.io/grab-charakter/"),
              )
          ],
      ]
  )
  return keyboard


# 4. /start buyrug'i kelganda ishlaydigan qism
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
  user_name = message.from_user.first_name

  welcome_text = (
      f"✨━ ━━━━━━━━━━━━ ━✨\n"
      f"💎 Gʀᴀʙ Cʜᴀʀᴀᴄᴛᴇʀ'ɢᴀ Xᴜꜱʜ Kᴇʟɪʙꜱɪᴢ! ✊\n\n"
      f"👋 Sᴀʟᴏᴍ, {user_name}!\n\n"
      f"🌟 Bᴜ ʙᴏᴛ oʀqᴀʟɪ sᴇvimli pᴇrsoɴᴀjlᴀrni yig'ing vᴀ guruhlᴀrni jоnlᴀntiring!\n"
      f"✨━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ✨"
  )

  await message.answer(
      welcome_text, reply_markup=get_start_keyboard(), parse_mode="Markdown"
  )


# 5. Botni ishga tushiruvchi asosiy funksiya
async def main():
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  print("Grab Character boti ishga tushdi...")
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())
