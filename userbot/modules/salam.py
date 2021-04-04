from platform import uname
from userbot import ALIVE_NAME, CMD_HELP
from userbot.events import register

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@register(outgoing=True, pattern='^.P(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("Shalom, Horas..\tSelamat Pagi")


@register(outgoing=True, pattern='^.S(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("Shalom, Horas..\tSelamat Siang")

@register(outgoing=True, pattern='^.Ss(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("Shalom, Horas..\tSelamat Siang")


@register(outgoing=True, pattern='^.M(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("Shalom, Horas..\tSelamat Malam")


@register(outgoing=True, pattern='^.B(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("Shalom, Horas..\t")


CMD_HELP.update({
    "salam":
    "`.P`\
\nUsage: Untuk Memberi salam Selamat Pagi.\
\n`.S`\
\nUsage: Untuk Memberi Salam Selamat Siang.\
\n'.M'\
\nUsage: Untuk Memberi Salam Selamat Malam"
})
