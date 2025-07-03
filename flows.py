from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    filters,
)

from router import pick_manager # routing to a manager


# ──────────────────────────────── STEP MAP ────────────────────────────────
LANG, TOPIC, MODEL, MARKET, ASKING, PR_EXTRA, PAY_EXTRA = range(7)

# ──────────────────────────────── TEXTS and CONSTANTS ────────────────────────────────
LANG_BUTTONS = [
    ("EN", "English 🇬🇧"),
    ("UA", "Українська 🇺🇦"),
    ("RU", "Русский 🇷🇺"),
    ("PT", "Português 🇧🇷"),
    ("ES", "Español 🇪🇸"),
]

GREETING = {
    "EN": "Splendid! I'm here to make our conversation as comfortable "
          "and enjoyable as possible! 😊\nWhat can I do for you?",
    "UA": "Чудово! Я тут, щоб наша розмова була максимально комфортною "
          "та приємною! 😊\nЧим я можу допомогти?",
    "RU": "Отлично! Я здесь, чтобы сделать наш разговор максимально удобным "
          "и приятным! 😊\nЧем могу помочь?",
    "PT": "Perfeito! Estou aqui para tornar nossa conversa o mais confortável "
          "e agradável possível! 😊\nComo posso ajudar?",
    "ES": "¡Estupendo! Estoy aquí para que nuestra conversación sea lo más "
          "cómoda y agradable posible! 😊\n¿En qué puedo ayudarte?",
}

TOPIC_BUTTONS = {
    "EN": [
        ("streamer",  "Verify my account (streamer)"),
        ("webmaster", "Verify my account (webmaster)"),
        ("pr",        "Connect me with PR/Marketing"),
        ("payment",   "I'd like to offer payment solutions"),
        ("other",     "Other"),
    ],
    "UA": [
        ("streamer",  "Підтвердити акаунт (стример)"),
        ("webmaster", "Підтвердити акаунт (вебмайстер)"),
        ("pr",        "Зʼєднати з PR/маркетингом"),
        ("payment",   "Пропоную платіжні рішення"),
        ("other",     "Інше"),
    ],
    "RU": [
        ("streamer",  "Верифицировать аккаунт (стример)"),
        ("webmaster", "Верифицировать аккаунт (вебмастер)"),
        ("pr",        "Связать с PR/маркетингом"),
        ("payment",   "Предлагаю платёжные решения"),
        ("other",     "Другое"),
    ],
    "PT": [
        ("streamer",  "Verificar minha conta (streamer)"),
        ("webmaster", "Verificar minha conta (webmaster)"),
        ("pr",        "Falar com PR/Marketing"),
        ("payment",   "Oferecer soluções de pagamento"),
        ("other",     "Outro"),
    ],
    "ES": [
        ("streamer",  "Verificar mi cuenta (streamer)"),
        ("webmaster", "Verificar mi cuenta (webmaster)"),
        ("pr",        "Conectar con PR/Marketing"),
        ("payment",   "Ofrecer soluciones de pago"),
        ("other",     "Otro"),
    ],
}

PAYMENT_Q = {
    "EN": "What is your preferred payment model?",
    "UA": "Яка модель оплати для вас бажана?",
    "RU": "Какую модель оплаты вы предпочитаете?",
    "PT": "Qual é o modelo de pagamento preferido?",
    "ES": "¿Cuál es tu modelo de pago preferido?",
}

PAYMENT_BTNS = [
    ("rs",  "RS / Hybrid / CPA"),
    ("cpm", "CPM"),
]

PAY_LABEL = {"rs": "RS / Hybrid / CPA", "cpm": "CPM"} # dictionary for the manager message 

MARKET_Q = {
    "EN": "Please share the main markets you work with.",
    "UA": "Оберіть основні ринки, з якими ви працюєте.",
    "RU": "Выберите основные рынки, с которыми вы работаете.",
    "PT": "Por favor, indique os principais mercados com que trabalha.",
    "ES": "Indica los principales mercados con los que trabajas.",
}

MARKET_BTNS = {
    "EN": [
        ("eu",    "Europe"),
        ("ca",    "Canada / Oceania"),
        ("latam", "Latin America"),
        ("other", "Other markets"),
    ],
    "UA": [
        ("eu",    "Європа"),
        ("ca",    "Канада / Океанія"),
        ("latam", "Латинська Америка"),
        ("other", "Інші ринки"),
    ],
    "RU": [
        ("eu",    "Европа"),
        ("ca",    "Канада / Океания"),
        ("latam", "Латинская Америка"),
        ("other", "Другие рынки"),
    ],
    "PT": [
        ("eu",    "Europa"),
        ("ca",    "Canadá / Oceania"),
        ("latam", "América Latina"),
        ("other", "Outros mercados"),
    ],
    "ES": [
        ("eu",    "Europa"),
        ("ca",    "Canadá / Oceanía"),
        ("latam", "América Latina"),
        ("other", "Otros mercados"),
    ],
}

QUESTIONS = {
    "EN": {
        "title": "Please answer the following questions:",
        "items": [
            ("traffic",   "What are your sources of traffic? (share links if there are any)"),
            ("geo",       "Please specify your main GEOs"),
            ("deal",      "What deal are you looking for?"),
            ("tgcontact", "Share your Telegram contact (@ nickname)"),
            ("email",     "Your email in our affiliate program"),
        ],
    },
    "UA": {
        "title": "Будь ласка, дайте відповіді на наступні запитання:",
        "items": [
            ("traffic",   "Які ваші джерела трафіку? (поділіться посиланнями, якщо є)"),
            ("geo",       "Вкажіть основні GEO"),
            ("deal",      "Який тип співпраці вас цікавить?"),
            ("tgcontact", "Поділіться своїм Telegram-контактом (@ nickname)"),
            ("email",     "Ваш email у нашій партнерській програмі"),
        ],
    },
    "RU": {
        "title": "Пожалуйста, ответьте на следующие вопросы:",
        "items": [
            ("traffic",   "Откуда ваш трафик? (пришлите ссылки, если есть)"),
            ("geo",       "Укажите основные GEO"),
            ("deal",      "Какой тип сделки вас интересует?"),
            ("tgcontact", "Поделитесь вашим Telegram-контактом (@ nickname)"),
            ("email",     "Ваш email в нашей партнёрской программе"),
        ],
    },
    "PT": {
        "title": "Por favor, responda às seguintes perguntas:",
        "items": [
            ("traffic",   "Quais são as suas fontes de tráfego? (envie links se houver)"),
            ("geo",       "Informe seus principais GEOs"),
            ("deal",      "Que tipo de acordo você procura?"),
            ("tgcontact", "Compartilhe seu contato no Telegram (@ nickname)"),
            ("email",     "Seu email no nosso programa de afiliados"),
        ],
    },
    "ES": {
        "title": "Por favor, responde a las siguientes preguntas:",
        "items": [
            ("traffic",   "¿Cuáles son tus fuentes de tráfico? (comparte enlaces si los tienes)"),
            ("geo",       "Especifica tus GEOs principales"),
            ("deal",      "¿Qué tipo de acuerdo buscas?"),
            ("tgcontact", "Comparte tu contacto de Telegram (@ nickname)"),
            ("email",     "Tu correo electrónico en nuestro programa de afiliados"),
        ],
    },
}

CONFIRM = {
    "EN": "✅ Thank you for your answers! One of our managers will contact you "
          "shortly.\nIf there are any more questions, I'm always here to help.",
    "UA": "✅ Дякуємо за відповіді! Наш менеджер незабаром зв'яжеться з вами.\n"
          "Якщо виникнуть додаткові питання, я завжди поруч.",
    "RU": "✅ Спасибо за ответы! Наш менеджер скоро свяжется с вами.\n"
          "Если появятся вопросы, я всегда на связи.",
    "PT": "✅ Obrigado pelas respostas! Um dos nossos gerentes entrará em "
          "contato em breve.\nQualquer dúvida, estou sempre por aqui.",
    "ES": "✅ ¡Gracias por tus respuestas! Uno de nuestros managers se pondrá "
          "en contacto contigo en breve.\nSi tienes más preguntas, estoy aquí."
}

PR_INSTR = {
    "EN": "Please send your commercial offer here – @YourUsername",
    "UA": "Надішліть вашу комерційну пропозицію сюди – @YourUsername",
    "RU": "Отправьте ваше коммерческое предложение сюда – @YourUsername",
    "PT": "Envie sua proposta comercial aqui – @YourUsername",
    "ES": "Envía tu propuesta comercial aquí – @YourUsername",
}

PAY_INSTR = {
    "EN": "Please send your payment-solution proposal here – @YourUsername",
    "UA": "Надішліть вашу пропозицію щодо платіжних рішень сюди – @YourUsername",
    "RU": "Отправьте ваше предложение по платёжным решениям сюда – @YourUsername",
    "PT": "Envie sua proposta de solução de pagamento aqui – @YourUsername",
    "ES": "Envía tu propuesta de soluciones de pago aquí – @YourUsername",
}

ADDITIONAL_Q_BUTTON = {
    "EN": "There are additional questions left",
    "UA": "У мене залишилися додаткові питання",
    "RU": "У меня остались дополнительные вопросы",
    "PT": "Ainda tenho dúvidas",
    "ES": "Aún tengo preguntas",
}

START_OVER = range(1)  # just a symbolic constant, value not important

# ────────────────────────── Questions / Answers ────────────────────────────
def build_language_kb():
    # helper to show language buttons for the start over function
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(lbl, callback_data=code)]
         for code, lbl in LANG_BUTTONS]
    )

async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Restart the wizard without deleting the previous message.
    query = update.callback_query
    await query.answer()

    context.user_data.clear()               

    #  Send a fresh language-picker message
    await query.message.reply_text(
        "Hello there! I'm Titan Partners Bot 🤖\n"
        "Before we dive into our chat, could you please let me know which "
        "language you prefer to use?",
        reply_markup=build_language_kb(),
    )

    return LANG

def add_start_over(btn_rows: list[list[InlineKeyboardButton]]):
    # Function to add Start Over button
    btn_rows.append([InlineKeyboardButton("🔄 Start over", callback_data="start_over")])
    return btn_rows

def build_combined_prompt(lang: str) -> str:
    data = QUESTIONS[lang]
    lines = [data["title"], ""]                     # title + blank line
    for idx, (_key, question) in enumerate(data["items"], start=1):
        lines.append(f"{idx}. {question}")
    return "\n".join(lines)

# async function as it waits for the user response
async def start_wizard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton(text=label, callback_data=code)] 
        for code, label in LANG_BUTTONS # take labels from LANG_BUTTONS for each button
    ]

    await update.message.reply_text(
        "Hello there! I'm Titan Partners Bot 🤖\n"
        "Before we dive into our chat, could you please let me know which "
        "language you prefer to use?",
        reply_markup=InlineKeyboardMarkup(kb),  # shows the language buttons markup
    )
    return LANG    

async def choose_lang(update: Update, context):
    # Once the user picked a language and the first question is showed

    query = update.callback_query
    lang_code = query.data   # carries the chosen language
    await query.answer()    # sends an ack back to Telegram so the loading spinner on the user’s button stops

    context.user_data["lang"] = lang_code
    context.user_data["answers"] = {}


    buttons = add_start_over([
    [InlineKeyboardButton(text=label, callback_data=code)]
    for code, label in TOPIC_BUTTONS[lang_code]
    ])
    

    await query.message.reply_text( # the reply text
        GREETING[lang_code],
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    return TOPIC



async def choose_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    topic_code = query.data
    await query.answer()

    lang = context.user_data["lang"]

    # 1. Streamer / Webmaster
    if topic_code in ("streamer", "webmaster"):
        context.user_data["role"] = topic_code

        buttons = add_start_over([
            [InlineKeyboardButton(t, callback_data=c)] for c, t in PAYMENT_BTNS
        ])

        await query.message.reply_text(
            PAYMENT_Q[lang],
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        return MODEL

    # --- 2. PR / Marketing ----------------------------------------------
    if topic_code == "pr":
        btns = add_start_over([
            [InlineKeyboardButton(ADDITIONAL_Q_BUTTON[lang], callback_data="pr_extra")]
        ])
        await query.message.reply_text(PR_INSTR[lang], reply_markup=InlineKeyboardMarkup(btns))
        return PR_EXTRA

    # --- 3. Payment-solutions -------------------------------------------
    if topic_code == "payment":
        btns = add_start_over([
            [InlineKeyboardButton(ADDITIONAL_Q_BUTTON[lang], callback_data="pay_extra")]
        ])
        await query.message.reply_text(PAY_INSTR[lang], reply_markup=InlineKeyboardMarkup(btns))
        return PAY_EXTRA

    # --- 4. Other  -------------------------------------------------------
    prompt = build_combined_prompt(lang)
    await query.message.reply_text(prompt)
    return ASKING        


async def choose_payment_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    model_code = query.data
    await query.answer()

    context.user_data["answers"]["payment_model"] = model_code

    lang = context.user_data["lang"]

    # build buttons
    btns = add_start_over([
        [InlineKeyboardButton(t, callback_data=c)] for c, t in MARKET_BTNS[lang]
    ])

    await query.message.reply_text(MARKET_Q[lang], reply_markup=InlineKeyboardMarkup(btns))
    return MARKET


async def choose_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    market_code = query.data
    await query.answer()

    lang = context.user_data["lang"]
    context.user_data["answers"]["market"] = market_code

    prompt = build_combined_prompt(lang)

    await query.message.reply_text(
        prompt,
        reply_markup=InlineKeyboardMarkup(add_start_over([])),
    )
    return ASKING

async def handle_questions_left_pr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 'Additional questions left' button handler if user wants PR/Marketing

    query = update.callback_query
    await query.answer()

    # --- Notify manager straight away ------------------------------------
    lang = context.user_data["lang"]
    mgr_user, mgr_chat = pick_manager({})          # pass empty dict or adjust

    await context.bot.send_message(
        chat_id=mgr_chat,
        text=(
            f"⚡ PR/Marketing lead #{update.effective_user.id} "
            f"(@{update.effective_user.username or 'no_username'}) [{lang}]\n"
            "They clicked ‘additional questions’ after the PR offer prompt."
        )
    )

    # --- Confirm to the user ---------------------------------------------
    await query.message.reply_text(
        "✅ Thanks! One of our managers will reach out shortly.",
        reply_markup=InlineKeyboardMarkup(add_start_over([])), # Add Start Over button
    )

    return ConversationHandler.END            # conversation finished

async def handle_questions_left_payment_solutions(update: Update, context: ContextTypes.DEFAULT_TYPE):   # NEW
    # 'Additional questions left' button handler if user wants payment solutions
    
    query = update.callback_query
    await query.answer()

    lang = context.user_data.get("lang", "EN")
    mgr_user, mgr_chat = pick_manager({})

    await context.bot.send_message(
        mgr_chat,
        text=(
            f"⚡ Payment-solutions lead #{update.effective_user.id} "
            f"(@{update.effective_user.username or 'no_username'}) [{lang}]\n"
            "They clicked ‘additional questions’ after the payment offer prompt."
        )
    )

    await query.message.reply_text(
        "✅ Thanks! One of our managers will reach out shortly.",
        reply_markup=InlineKeyboardMarkup(add_start_over([])), # Add Start Over button
    )

    return ConversationHandler.END



# ───────────────────────────── QUESTION LOOP ─────────────────────────────

async def collect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang     = context.user_data["lang"]
    answers  = context.user_data.setdefault("answers", {})
    role     = context.user_data.get("role")                 # streamer / webmaster / None
    answers["raw_reply"] = update.message.text               # save the whole reply

    # ---------- Confirmation to user ----------
    await update.message.reply_text(
        CONFIRM.get(lang, CONFIRM["EN"]),
        reply_markup=InlineKeyboardMarkup(add_start_over([])),  # with Start Over button
    )

    # ---------- Manager alert ----------
    mgr_user, mgr_chat = pick_manager(answers)

    # build optional tags
    lines = [
        f"⚡ New affiliate #{update.effective_user.id} "
        f"(@{update.effective_user.username or 'no_username'}) [{lang}]"
    ]

    if role == "streamer":
        lines.append("ROLE: Streamer")
    elif role == "webmaster":
        lines.append("ROLE: Webmaster")

    if "payment_model" in answers:
        lines.append(f"Payment model: {PAY_LABEL.get(answers['payment_model'], answers['payment_model'])}")

    if "market" in answers:
        lines.append(f"Market: {MARKET_BTNS.get(answers['market'], answers['market'])}")

    lines.append("Combined answers:")
    lines.append(update.message.text)

    await context.bot.send_message(mgr_chat, text="\n".join(lines))
    return FINISHED

# -- helpers ---------------------------------------------------------------
async def _show_language_picker(query):
    kb = [[InlineKeyboardButton(lbl, callback_data=code)] for code, lbl in LANG_BUTTONS]
    await query.message.edit_text(
        "Hello there! I'm Titan Partners Bot 🤖\n"
        "Before we dive into our chat, could you please let me know which "
        "language you prefer to use?",
        reply_markup=InlineKeyboardMarkup(kb),
    )
    return LANG

# ────────────────────────── CONVERSATION HANDLER ─────────────────────────
START_OVER_HANDLER = CallbackQueryHandler(start_over, pattern="^start_over$")
FINISHED = 8  # any unused state id

def build_conv_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start_wizard)], # whenever the user sends /start, the wizard starts (or restarts) and start_wizard runs
        states={ # Each constant (LANG, TOPIC, …) is an int (0, 1, 2, …)
            LANG:   [CallbackQueryHandler(choose_lang)], # LANG − waits for a button -> choose_lang
            TOPIC:  [START_OVER_HANDLER, CallbackQueryHandler(choose_topic)], # TOPIC − waits for a button -> choose_topic
            MODEL:  [START_OVER_HANDLER, CallbackQueryHandler(choose_payment_model)], # MODEL − waits for a button -> choose_payment_model
            MARKET: [START_OVER_HANDLER, CallbackQueryHandler(choose_market)], # MARKET − waits for a button -> choose_market
            PR_EXTRA: [START_OVER_HANDLER, CallbackQueryHandler(handle_questions_left_pr)], # questions left button -> routed to the manager
            PAY_EXTRA: [START_OVER_HANDLER, CallbackQueryHandler(handle_questions_left_payment_solutions)], # questions left button -> routed to the manag
            ASKING: [START_OVER_HANDLER, MessageHandler(filters.TEXT & ~filters.COMMAND, collect)], # ASKING − waits for free-text -> collect
            FINISHED: [START_OVER_HANDLER],
        },
        fallbacks=[], # Empty list – we didn’t add a cancel flow
        allow_reentry=True, # True, so typing /start mid-flow restarts from the top instead of being ignored
    )







