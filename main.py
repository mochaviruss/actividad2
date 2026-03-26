import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db():
    return psycopg2.connect(os.getenv("DATABASE_URL"))


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            chat_id BIGINT NOT NULL,
            role VARCHAR(20) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def get_historial(chat_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT role, content FROM messages WHERE chat_id = %s ORDER BY created_at DESC LIMIT 10",
        (chat_id,)
    )
    filas = cur.fetchall()
    cur.close()
    conn.close()
    return list(reversed(filas))


def guardar_mensaje(chat_id, role, content):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (chat_id, role, content) VALUES (%s, %s, %s)",
        (chat_id, role, content)
    )
    conn.commit()
    cur.close()
    conn.close()


def preguntar_ia(mensajes):
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama3-8b-8192",
        "messages": mensajes
    }
    respuesta = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        json=body,
        headers=headers
    )
    return respuesta.json()["choices"][0]["message"]["content"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola! Soy tu asistente. En que te puedo ayudar?")


async def limpiar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM messages WHERE chat_id = %s", (update.effective_chat.id,))
    conn.commit()
    cur.close()
    conn.close()
    await update.message.reply_text("Listo, empezamos de cero.")


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    texto = update.message.text

    guardar_mensaje(chat_id, "user", texto)
    historial = get_historial(chat_id)

    mensajes = [{"role": "system", "content": "Eres un asistente util y amigable que responde en español."}]
    mensajes += [{"role": m["role"], "content": m["content"]} for m in historial]

    respuesta = preguntar_ia(mensajes)
    guardar_mensaje(chat_id, "assistant", respuesta)
    await update.message.reply_text(respuesta)


if __name__ == "__main__":
    init_db()
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clear", limpiar))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    logger.info("Bot iniciado")
    app.run_polling()
