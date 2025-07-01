import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from flows import build_conv_handler        # pulls the wizard handler script 

# 1) Load secret token from .env
load_dotenv()
TOKEN = os.getenv("TG_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("TG_BOT_TOKEN not found. Did you create .env?")

# 2) (Optional) basic logging. Debug purpose
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

# 3) Bootstrap application & add the wizard handler
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(build_conv_handler())     # where flows.py logic is used
    app.run_polling()

if __name__ == "__main__":
    main()