from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = "8949343588:AAGAxOyb8CCdmHBhh1mlPi2VH8JbbwSPP2g"

# ==================== MAVZULAR ====================
MAVZULAR = {
    1: "Siydik tanosil azolar anatomo-fiziologiyasi. Buyrak normal anatomiyasi va fiziologiya",
    2: "Siydik nayi, siydik pufagi, tashki siydik chiqaruv nayi anatomiya va fiziologiyasi",
    3: "Erkaklik tashki va icki jinsiy a'zolari tuzilishi",
    4: "Siydik tanosil azolari embriologiyasi",
    5: "Azolar tug'ma rivojlanish anomaliyalari",
    6: "Urologik kasalliklarning semiotikasi, sindromlar va simptomlar",
    7: "Laborator tekshirish usullari",
    8: "Zamonaviy instrumental tekshiruv usullari",
    9: "Siydik tanosil azolarning spetsifik va nospetsifik yallig'lanish kasalliklari. Assoratlanmagan pielonefrit",
    10: "Assoratlanmagan pielonefrit",
    11: "Assoratlanmagan va assoratlanmagan sistitlar",
    12: "Gonokokkli uretrit. Gonoreya kasalligi tashxislash va davolash",
    13: "Nogonokokkli va noinfektsion uretritlar",
    14: "Fimoz, parafimoz assorati va davolash usullari. Tsirqumsiziya tashrikh",
    15: "Utkir yerg'ok sindromi. Utkir orxoepididimit diagnostikasi va davolash, assoratlar",
    16: "Utkir assoratlanmagan prostatit",
    17: "Surunkali prostatit, prostatit assoratlar",
    18: "Urogenital tuberkulez",
    19: "Siydik tosh kasalligi",
    20: "Gidronefrotik transformatsiya",
    21: "Nefroptozis",
    22: "Tsistoureteral reflyuks kasalligi",
    23: "Prostata bezi xavfsiz giperplaziyasi (adenoma)",
    24: "Shoshilinch urologiya differensiatsiyasi",
    25: "Siydik-tanosil tizimi shikastlanishlari",
    26: "Varikotsele kasalligi",
    27: "Gidrotsele, spermatotsele",
    28: "Kriptorxizm va uning operativ davolashi",
    29: "Nefrogen arterial gipertenziya",
    30: "Neyrogen (avtonom) siydik pufagi va siydik pufagi atoniyasi differensiatsiyasi",
    31: "Siydik tutoqmaslik turlari va diagnostikasi, davolash prinsiplari",
    32: "Erkaklar erektil disfunktsiyasi",
    33: "Erkaklar bepushtligi va yordamchi reproduktiv texnologiyalar",
}

# ==================== TESTLAR ====================
TESTLAR = {
    1: [
        {
            "savol": "Buyraklar qayerda joylashgan?",
            "variantlar": ["Ko'krak qafasida", "Qorin bo'shlig'ida retroperitoneal", "Chov sohasida", "To'sh ortida"],
            "togri": 1
        },
        {
            "savol": "Kattalar buyragining og'irligi qancha?",
            "variantlar": ["50-100 g", "120-200 g", "300-400 g", "500 g dan ortiq"],
            "togri": 1
        },
    ],
    19: [
        {
            "savol": "Siydik tosh kasalligida eng ko'p uchraydigan simptom qaysi?",
            "variantlar": ["Isitma", "Og'riq (renal kolik)", "Shish", "Yo'tal"],
            "togri": 1
        },
    ],
}

# ==================== VIDEOLAR ====================
VIDEOLAR = {
    "Umumiy urologiya": [
        {"nomi": "Buyrak anatomiyasi", "link": "https://youtube.com"},
        {"nomi": "UTT tekshiruvi", "link": "https://youtube.com"},
    ],
    "Operatsiyalar": [
        {"nomi": "Nefrektomiya", "link": "https://youtube.com"},
        {"nomi": "Tsistoskopiya", "link": "https://youtube.com"},
    ],
}

# ==================== KITOBLAR ====================
KITOBLAR = [
    {"nomi": "EAU Guidelines 2024", "link": "https://uroweb.org/guidelines"},
    {"nomi": "Campbell-Walsh Urology", "link": "https://example.com"},
]

# ==================== FOYDALANUVCHI HOLATI ====================
user_states = {}


# ==================== ASOSIY MENYU ====================
def asosiy_menyu():
    keyboard = [
        [InlineKeyboardButton("📖 Mavzular", callback_data="mavzular")],
        [InlineKeyboardButton("📝 Testlar", callback_data="testlar")],
        [InlineKeyboardButton("🎥 Videolar", callback_data="videolar")],
        [InlineKeyboardButton("📚 Kitoblar", callback_data="kitoblar")],
        [InlineKeyboardButton("📊 Natijalarim", callback_data="natijalar")],
    ]
    return InlineKeyboardMarkup(keyboard)


# ==================== START ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ism = update.effective_user.first_name
    matn = (
        f"Salom, {ism}! 👋\n\n"
        "🏥 *Urologiya O'quv Botiga Xush Kelibsiz!*\n\n"
        "Bu bot sizga urologiya fanini o'rganishda yordam beradi.\n\n"
        "Quyidagi bo'limlardan birini tanlang:"
    )
    await update.message.reply_text(matn, reply_markup=asosiy_menyu(), parse_mode="Markdown")


# ==================== MAVZULAR BO'LIMI ====================
async def mavzular_sahifasi(query, sahifa=1):
    har_sahifada = 8
    boshlanish = (sahifa - 1) * har_sahifada
    tugash = boshlanish + har_sahifada
    mavzu_ids = list(MAVZULAR.keys())[boshlanish:tugash]
    jami_sahifa = (len(MAVZULAR) + har_sahifada - 1) // har_sahifada

    keyboard = []
    for mid in mavzu_ids:
        nomi = MAVZULAR[mid]
        qisqa = nomi[:38] + "..." if len(nomi) > 38 else nomi
        keyboard.append([InlineKeyboardButton(f"{mid}. {qisqa}", callback_data=f"mavzu_{mid}")])

    nav = []
    if sahifa > 1:
        nav.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"mavzular_s{sahifa-1}"))
    if sahifa < jami_sahifa:
        nav.append(InlineKeyboardButton("Keyingi ➡️", callback_data=f"mavzular_s{sahifa+1}"))
    if nav:
        keyboard.append(nav)
    keyboard.append([InlineKeyboardButton("🏠 Bosh menyu", callback_data="bosh")])

    await query.edit_message_text(
        f"📖 *Mavzular* ({sahifa}/{jami_sahifa} sahifa)\n\nMavzuni tanlang:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


# ==================== TESTLAR BO'LIMI ====================
async def testlar_sahifasi(query):
    keyboard = []
    for mid, mavzu in MAVZULAR.items():
        test_bor = "✅" if mid in TESTLAR else "🔒"
        qisqa = mavzu[:35] + "..." if len(mavzu) > 35 else mavzu
        keyboard.append([InlineKeyboardButton(f"{test_bor} {mid}. {qisqa}", callback_data=f"test_{mid}")])
    keyboard.append([InlineKeyboardButton("🏠 Bosh menyu", callback_data="bosh")])

    await query.edit_message_text(
        "📝 *Testlar*\n\n✅ — mavjud\n🔒 — tez orada\n\nMavzuni tanlang:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


# ==================== VIDEOLAR BO'LIMI ====================
async def videolar_sahifasi(query):
    keyboard = []
    for kategoriya in VIDEOLAR.keys():
        keyboard.append([InlineKeyboardButton(f"🎥 {kategoriya}", callback_data=f"video_kat_{kategoriya}")])
    keyboard.append([InlineKeyboardButton("🏠 Bosh menyu", callback_data="bosh")])

    await query.edit_message_text(
        "🎥 *Videolar*\n\nKategoriyani tanlang:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


# ==================== KITOBLAR BO'LIMI ====================
async def kitoblar_sahifasi(query):
    matn = "📚 *Kitoblar va Qo'llanmalar*\n\n"
    for i, kitob in enumerate(KITOBLAR, 1):
        matn += f"{i}. [{kitob['nomi']}]({kitob['link']})\n\n"
    keyboard = [[InlineKeyboardButton("🏠 Bosh menyu", callback_data="bosh")]]
    await query.edit_message_text(matn, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")


# ==================== CALLBACK HANDLER ====================
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "bosh":
        await query.edit_message_text(
            "🏥 *Urologiya O'quv Boti*\n\nBo'limni tanlang:",
            reply_markup=asosiy_menyu(),
            parse_mode="Markdown"
        )

    elif data == "mavzular":
        await mavzular_sahifasi(query, 1)

    elif data.startswith("mavzular_s"):
        sahifa = int(data.replace("mavzular_s", ""))
        await mavzular_sahifasi(query, sahifa)

    elif data.startswith("mavzu_"):
        mid = int(data.replace("mavzu_", ""))
        mavzu_nomi = MAVZULAR[mid]
        keyboard = [
            [InlineKeyboardButton("📝 Bu mavzudan test ishlash", callback_data=f"test_{mid}")],
            [InlineKeyboardButton("⬅️ Mavzularga qaytish", callback_data="mavzular")],
            [InlineKeyboardButton("🏠 Bosh menyu", callback_data="bosh")],
        ]
        await query.edit_message_text(
            f"📖 *Mavzu {mid}*\n\n{mavzu_nomi}\n\n"
            "_(Mavzu bo'yicha batafsil ma'lumot tez orada qo'shiladi)_",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data == "testlar":
        await testlar_sahifasi(query)

    elif data.startswith("test_"):
        mid = int(data.replace("test_", ""))
        if mid not in TESTLAR:
            await query.edit_message_text(
                f"🔒 Bu mavzu bo'yicha testlar tez orada qo'shiladi!",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Orqaga", callback_data="testlar")]]),
                parse_mode="Markdown"
            )
            return

        user_states[user_id] = {
            "mavzu": mid,
            "savol_index": 0,
            "togri": 0,
            "xato": 0,
        }
        await test_savol_yuborish(query, user_id)

    elif data.startswith("javob_"):
        javob = int(data.split("_")[1])
        await test_javob_tekshirish(query, user_id, javob)

    elif data == "keyingi_savol":
        if user_id in user_states:
            await test_savol_yuborish(query, user_id)

    elif data == "videolar":
        await videolar_sahifasi(query)

    elif data.startswith("video_kat_"):
        kat = data.replace("video_kat_", "")
        videolar = VIDEOLAR.get(kat, [])
        matn = f"🎥 *{kat}*\n\n"
        for v in videolar:
            matn += f"▶️ [{v['nomi']}]({v['link']})\n\n"
        keyboard = [
            [InlineKeyboardButton("⬅️ Videolarga qaytish", callback_data="videolar")],
            [InlineKeyboardButton("🏠 Bosh menyu", callback_data="bosh")],
        ]
        await query.edit_message_text(matn, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "kitoblar":
        await kitoblar_sahifasi(query)

    elif data == "natijalar":
        keyboard = [[InlineKeyboardButton("🏠 Bosh menyu", callback_data="bosh")]]
        await query.edit_message_text(
            "📊 *Natijalarim*\n\n_(Bu bo'lim tez orada ishga tushiriladi)_",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )


# ==================== TEST LOGIKASI ====================
async def test_savol_yuborish(query, user_id):
    holat = user_states[user_id]
    mid = holat["mavzu"]
    index = holat["savol_index"]
    savollar = TESTLAR[mid]

    if index >= len(savollar):
        togri = holat["togri"]
        jami = len(savollar)
        foiz = int((togri / jami) * 100)

        if foiz >= 80:
            baho = "🏆 A'lo!"
        elif foiz >= 60:
            baho = "👍 Yaxshi"
        elif foiz >= 40:
            baho = "📚 Qonikarli"
        else:
            baho = "❌ Qayta o'qing"

        keyboard = [
            [InlineKeyboardButton("🔄 Qayta ishlash", callback_data=f"test_{mid}")],
            [InlineKeyboardButton("📝 Boshqa mavzu", callback_data="testlar")],
            [InlineKeyboardButton("🏠 Bosh menyu", callback_data="bosh")],
        ]
        await query.edit_message_text(
            f"✅ *Test yakunlandi!*\n\n"
            f"📊 Natija: {togri}/{jami}\n"
            f"📈 Foiz: {foiz}%\n"
            f"Baho: {baho}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return

    savol = savollar[index]
    keyboard = []
    for i, variant in enumerate(savol["variantlar"]):
        keyboard.append([InlineKeyboardButton(f"{i+1}. {variant}", callback_data=f"javob_{i}")])

    await query.edit_message_text(
        f"📝 *Savol {index+1}/{len(savollar)}*\n\n{savol['savol']}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


async def test_javob_tekshirish(query, user_id, javob):
    holat = user_states[user_id]
    mid = holat["mavzu"]
    index = holat["savol_index"]
    savol = TESTLAR[mid][index]

    if javob == savol["togri"]:
        holat["togri"] += 1
        matn = "✅ *To'g'ri!*"
    else:
        holat["xato"] += 1
        togri_javob = savol["variantlar"][savol["togri"]]
        matn = f"❌ *Noto'g'ri!*\n\n✅ To'g'ri javob: *{togri_javob}*"

    holat["savol_index"] += 1
    keyboard = [[InlineKeyboardButton("Keyingi savol ➡️", callback_data="keyingi_savol")]]
    await query.edit_message_text(matn, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")


# ==================== BOTNI ISHGA TUSHIRISH ====================
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    print("✅ Urologiya boti ishga tushdi!")
    app.run_polling()


if __name__ == "__main__":
    main()
