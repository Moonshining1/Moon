from SACHIN_MUSIC.misc import SUDOERS
from SACHIN_MUSIC.utils.database import get_lang, is_maintenance
from strings import get_string
from SACHIN_MUSIC import app  # Ensure the `app` object is imported
import logging  # For error logging

SUPPORT_CHAT = "https://t.me/grandxmasti"  # Define SUPPORT_CHAT if not defined

# Decorator for handling language in regular commands
def language(mystic):
    async def wrapper(_, message, **kwargs):
        # Check for maintenance mode
        if await is_maintenance():
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    text=(
                        f"{app.mention} is under maintenance. "
                        f"Visit <a href='{SUPPORT_CHAT}'>Support Chat</a> for more info."
                    ),
                    disable_web_page_preview=True,
                )
        try:
            await message.delete()
        except Exception as e:
            logging.warning(f"Failed to delete message: {e}")

        # Fetch language
        try:
            lang_code = await get_lang(message.chat.id) or "en"
            language = get_string(lang_code)
        except Exception as e:
            logging.error(f"Error fetching language: {e}")
            language = get_string("en")

        return await mystic(_, message, language)

    return wrapper


# Decorator for handling language in callback queries
def languageCB(mystic):
    async def wrapper(_, CallbackQuery, **kwargs):
        # Check for maintenance mode
        if await is_maintenance():
            if CallbackQuery.from_user.id not in SUDOERS:
                return await CallbackQuery.answer(
                    text=(
                        f"{app.mention} is under maintenance. "
                        f"Visit Support Chat for more info."
                    ),
                    show_alert=True,
                )

        # Fetch language
        try:
            lang_code = await get_lang(CallbackQuery.message.chat.id) or "en"
            language = get_string(lang_code)
        except Exception as e:
            logging.error(f"Error fetching language: {e}")
            language = get_string("en")

        return await mystic(_, CallbackQuery, language)

    return wrapper


# Decorator for handling language at the start of bot interactions
def LanguageStart(mystic):
    async def wrapper(_, message, **kwargs):
        # Fetch language
        try:
            lang_code = await get_lang(message.chat.id) or "en"
            language = get_string(lang_code)
        except Exception as e:
            logging.error(f"Error fetching language: {e}")
            language = get_string("en")

        return await mystic(_, message, language)

    return wrapper
