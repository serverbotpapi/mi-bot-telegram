from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.constants import ParseMode

# Aquí va tu token
TOKEN = '7706419150:AAHyfiazH-ZgEC2m9JkDYfxdiSDiCq5pDf4'

# Palabras prohibidas y otros filtros
FORBIDDEN_WORDS = ['spam', 'comprar', 'promoción']
FORBIDDEN_LINKS = ['http', 'https']

# Comando para mostrar reglas
async def rules(update: Update, context: CallbackContext):
    rules_text = """
    **Reglas del Grupo:**
    1. No se permiten enlaces.
    2. No se permite spam o publicidad.
    3. Respeta a los demás miembros.
    4. No se permiten compras ni ventas.
    """
    await update.message.reply_text(rules_text, parse_mode=ParseMode.MARKDOWN)

# Comando para mostrar ayuda
async def help_command(update: Update, context: CallbackContext):
    help_text = """
    **Comandos disponibles:**
    - /reglas: Ver las reglas del grupo.
    - /ayuda: Ver este mensaje de ayuda.
    """
    await update.message.reply_text(help_text)

# Función que da la bienvenida a nuevos miembros
async def welcome(update: Update, context: CallbackContext):
    new_member = update.message.new_chat_members[0]
    await update.message.reply_text(f"¡Bienvenido al grupo, {new_member.full_name}! Por favor, lee las reglas: /reglas.")

# Función que filtra enlaces
async def link_filter(update: Update, context: CallbackContext):
    if any(link in update.message.text for link in FORBIDDEN_LINKS):  # Filtrar enlaces
        await update.message.delete()
        await update.message.reply_text("No se permiten enlaces en este grupo.")

# Función que filtra palabras no deseadas
async def word_filter(update: Update, context: CallbackContext):
    if any(word in update.message.text.lower() for word in FORBIDDEN_WORDS):
        await update.message.delete()
        await update.message.reply_text("Este mensaje contiene contenido no permitido.")

# Función que controla el envío de mensajes repetidos
async def anti_spam(update: Update, context: CallbackContext):
    if update.message.text == context.user_data.get('last_message', ''):
        await update.message.delete()
        await update.message.reply_text("No puedes enviar el mismo mensaje varias veces.")
    else:
        context.user_data['last_message'] = update.message.text

# Función para manejar reportes
async def report(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Por favor, proporciona el mensaje o el comportamiento que deseas reportar.")
        return
    report_text = " ".join(context.args)
    admin_chat_id = '7591950565'  # Cambia esto por tu ID de administrador
    await context.bot.send_message(admin_chat_id, f"Nuevo reporte recibido:\n{report_text}")
    await update.message.reply_text("¡Gracias por tu reporte! Un administrador lo revisará pronto.")

# Main function
async def main():
    # Configura la aplicación del bot
    application = Application.builder().token(TOKEN).build()

    # Comandos y filtros
    application.add_handler(CommandHandler("reglas", rules))
    application.add_handler(CommandHandler("ayuda", help_command))
    application.add_handler(CommandHandler("reportar", report))

    # Mensajes y filtrado
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, link_filter))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, word_filter))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anti_spam))

    # Arrancar el bot
    await application.run_polling()

# Este bloque solo se ejecuta si no estamos en un entorno interactivo como IDLE
if __name__ == '__main__':
    import sys
    import asyncio  # Asegúrate de que asyncio esté importado aquí
    if sys.platform != 'win32':  # En plataformas diferentes a Windows
        asyncio.run(main())
    else:  # En Windows, usar la siguiente línea
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.run(main())
