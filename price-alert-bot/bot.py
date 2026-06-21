import asyncio
from telegram import Bot

TELEGRAM_TOKEN = "7427465569:AAHL4PE1oHbygbW8SoOwbFZfE5VWnop_KZI"

async def send_alert(chat_id: str, product_name: str, price: float, url: str):
    bot = Bot(token=TELEGRAM_TOKEN)
    message = (
        f"🔔 *¡Bajada de precio!*\n\n"
        f"📦 *Producto:* {product_name}\n"
        f"💰 *Precio actual:* {price}€\n"
        f"🔗 [Ver en Amazon]({url})"
    )
    await bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode="Markdown"
    )

def notify(chat_id: str, product_name: str, price: float, url: str):
    asyncio.run(send_alert(chat_id, product_name, price, url))