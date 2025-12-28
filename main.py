
from rubka.asynco import Robot, Message, filters
from typing import Dict, Set

bot = Robot("token_soma")
chat_set: Set[int] = set()
owner = "guid_shoma"

@bot.on_message()
async def count_messages(bot: Robot, message: Message):
    chat_set.add(message.chat_id)


@bot.on_message(filters=filters.text_regex(r"(https?://|www\.|\.ir|\.com|\.net|t\.me|@\w+)") | filters.is_edited | filters.text_contains_any(["https","http", "@"]))
async def handle_links(bot: Robot, message: Message):
    await message.reply("لطفا لینک نفرست.")
    await message.delete()


@bot.on_message(filters=filters.text_startswith("پیام همگانی"))
async def broadcast_command(bot_obj: Robot, message: Message):
    id = message.sender_id
    if id != owner:
        return

    broadcast_text = message.text.replace("پیام همگانی", "").strip()
    if not broadcast_text:
        await message.reply("⚠️ لطفاً بعد از دستور، پیام خود را بنویسید.\n\nمثال:\nپیام همگانی سلام به همه گروه‌ها!")
        return
    

    status_message = await message.reply(f"🚀 در حال ارسال پیام همگانی به {len(chat_set)} گروه...\n\nلطفاً صبر کنید...")

    success_count = 0
    failed_groups = []
    for chat_id in chat_set:
        try:
            await bot_obj.send_message(chat_id, broadcast_text)
            success_count += 1
        except Exception as e:
            failed_groups.append(str(chat_id))
            print("{e}")

    result_text = f"ارسال پیام همگانی تمام شد.\n\n"
    result_text += f"📊 آمار:\n"
    result_text += f"✅ گروه‌های موفق: {success_count}\n"
    result_text += f"❌ گروه‌های ناموفق: {len(failed_groups)}"
    
    if failed_groups:
        result_text += f"\n\nآیدی گروه‌های ناموفق:\n{', '.join(failed_groups)}"

    await status_message.edit(result_text)
bot.run()
