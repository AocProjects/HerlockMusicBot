

import asyncio
import importlib
import sys

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from HerlockMusic import LOGGER, app, userbot
from HerlockMusic.core.call import Herlock
from HerlockMusic.plugins import ALL_MODULES
from HerlockMusic.utils.database import get_banned_users, get_gbanned

loop = asyncio.get_event_loop()


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("HerlockMusic").error(
            "Asistan İstemci Tanımlı Vars Yok!.. İşlemden Çıkılıyor."
        )
        return
    if (
        not config.SPOTIFY_CLIENT_ID
        and not config.SPOTIFY_CLIENT_SECRET
    ):
        LOGGER("HerlockMusic").warning(
            "Spotify Vars tanımlı değil. Botunuz spotify sorgularını oynatamayacak."
        )
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("HerlockMusic.plugins" + all_module)
    LOGGER("Herlockmusic.plugins").info(
        "Modüller Başarıyla İçe Aktarıldı "
    )
    await userbot.start()
    await Herlock.start()
    try:
        await Herlock.stream_call(
            "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"
        )
    except NoActiveGroupCall:
        LOGGER("HerlockMusic").error(
            "[ERROR] - \n\nLütfen Kaydedici Grubunuzun Sesli Aramasını açın. Günlük grubunuzdaki sesli aramayı asla kapatmadığınızdan/bitirmediğinizden emin olun."
        )
        sys.exit()
    except:
        pass
    await Herlock.decorators()
    LOGGER("HerlockMusic").info("Herlock Müzik Botu Başarıyla Başlatıldı")
    await idle()


if __name__ == "__main__":
    loop.run_until_complete(init())
    LOGGER("HerlockMusic").info("Herlock Music Bot'u Durdurmak! Güle güle")
