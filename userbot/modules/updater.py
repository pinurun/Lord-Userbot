"""
This module updates the userbot based on upstream revision
"""

from os import remove, execle, path, environ
import asyncio
import sys

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from userbot import (
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    HEROKU_API_KEY,
    HEROKU_APP_NAME,
    UPSTREAM_REPO_URL,
    UPSTREAM_REPO_BRANCH)
from userbot.events import register

requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), 'requirements.txt')


async def gen_chlog(repo, diff):
    ch_log = ''
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += f'•[{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n'
    return ch_log


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            ' '.join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is not None:
        import heroku3
        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if HEROKU_APP_NAME is None:
            await event.edit(
                '`[HEROKU]: Harap Siapkan Variabel` **HEROKU_APP_NAME** `'
                ' ᴜɴᴛᴜᴋ ᴅᴀᴘᴀᴛ ᴅᴇᴘʟᴏʏ ᴘᴇʀᴜʙᴀʜᴀɴ ᴛᴇʀʙᴀʀᴜ dari ᴘ ɪ ɴ ᴜ ʀ ᴜ ɴ.`'
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await event.edit(
                f'{txt}\n`ᴋʀᴇᴅᴇɴꜱɪᴀʟ ʜᴇʀᴏᴋᴜ ᴛɪᴅᴀᴋ ᴠᴀʟɪᴅ ᴜɴᴛᴜᴋ ᴅᴇᴘʟᴏʏ ᴘɪɴᴜʀᴜɴ.`'
            )
            return repo.__del__()
        await event.edit('`[HEROKU]:'
                         '\nᴅʏɴᴏ ᴘɪɴᴜʀᴜɴ ꜱᴇᴅᴀɴɢ ᴅᴀʟᴀᴍ ᴘʀᴏꜱᴇꜱ, ᴍᴏʜᴏɴ ᴍᴇɴᴜɴɢɢᴜ 7-8 ᴍᴇɴɪᴛ`'
                         )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_API_KEY + "@")
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except GitCommandError as error:
            await event.edit(f'{txt}\n`Terjadi Kesalahan Di Log:\n{error}`')
            return repo.__del__()
        build = app.builds(order_by="created_at", sort="desc")[0]
        if build.status == "failed":
            await event.edit(
                "`Build Gagal!\n" "Dibatalkan atau ada beberapa kesalahan...`"
            )
            await asyncio.sleep(5)
            return await event.delete()
        else:
            await event.edit("`ᴘɪɴᴜʀᴜɴ ʙᴇʀʜᴀꜱɪʟ ᴅɪ ᴅᴇᴘʟᴏʏ!\n" "ʀᴇꜱᴛᴀʀᴛɪɴɢ, ᴍᴏʜᴏɴ ᴍᴇɴᴜɴɢɢᴜ.....`")
            await asyncio.sleep(15)
            await event.delete()

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "#update \n"
                "`ᴘɪɴᴜʀᴜɴ ʙᴇʀʜᴀꜱɪʟ ᴅɪ ᴜᴘᴅᴀᴛᴇ`")

    else:
        await event.edit('`[HEROKU]:'
                         '\nHarap Siapkan Variabel` **HEROKU_API_KEY** `.`'
                         )
        await asyncio.sleep(10)
        await event.delete()
    return


async def update(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    await event.edit('**🔥 ᴘɪɴᴜʀᴜɴ** `ʙᴇʀʜᴀꜱɪʟ ᴅɪ ᴜᴘᴅᴀᴛᴇ!`')
    await asyncio.sleep(1)
    await event.edit('**🔥 ᴘɪɴᴜʀᴜɴ** `ᴅɪ ʀᴇꜱᴛᴀʀᴛ....`')
    await asyncio.sleep(1)
    await event.edit('`ᴍᴏʜᴏɴ ᴍᴇɴᴜɴɢɢᴜ ʙᴇʙᴇʀᴀᴘᴀ ᴅᴇᴛɪᴋ.`')
    await asyncio.sleep(10)
    await event.delete()

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#pinurun \n"
            "**ᴘɪɴᴜʀᴜɴ ᴛᴇʟᴀʜ ᴅɪ ᴘᴇʀʙᴀʀᴜɪ**")
        await asyncio.sleep(100)
        await event.delete()

    # Spin a new instance of bot
    args = [sys.executable, "-m", "userbot"]
    execle(sys.executable, *args, environ)
    return


@ register(outgoing=True, pattern=r"^.update(?: |$)(now|deploy)?")
async def upstream(event):
    "For .update command, check if the bot is up to date, update if specified"
    await event.edit("`ᴍᴇɴɢᴇᴄᴇᴋ ᴘᴇᴍʙᴀʀᴜᴀɴ, ꜱɪʟᴀᴋᴀɴ ᴍᴇɴᴜɴɢɢᴜ....`")
    conf = event.pattern_match.group(1)
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    try:
        txt = "`Maaf, Pembaruan Tidak Dapat Di Lanjutkan Karna "
        txt += "Beberapa Masalah Terjadi`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f'{txt}\n`Directory {error} Tidak Dapat Di Temukan`')
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f'{txt}\n`Gagal Awal! {error}`')
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await event.edit(
                f"`Sayangnya, Directory {error} Tampaknya Bukan Dari Repo."
                "\nTapi Kita Bisa Memperbarui Paksa Menggunakan .update now.`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await event.edit(
            '**[UPDATER]:**\n'
            f'`Looks like you are using your own custom branch ({ac_br}). '
            'in that case, Updater is unable to identify '
            'which branch is to be merged. '
            'please checkout to any official branch`')
        return repo.__del__()
    try:
        repo.create_remote('upstream', off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote('upstream')
    ups_rem.fetch(ac_br)

    changelog = await gen_chlog(repo, f'HEAD..upstream/{ac_br}')

    if changelog == '' and force_update is False:
        await event.edit(
            f'\n**🔥 ᴘ ɪ ɴ ᴜ ʀ ᴜ ɴ ꜱᴜᴅᴀʜ ᴠᴇʀꜱɪ ᴛᴇʀʙᴀʀᴜ**\n')
        await asyncio.sleep(15)
        await event.delete()
        return repo.__del__()

    if conf is None and force_update is False:
        changelog_str = f'**🔥 ᴘᴇᴍʙᴀʀᴜᴀɴ ᴜɴᴛᴜᴋ ᴘ ɪ ɴ ᴜ ʀ ᴜ ɴ \n[ᴘɪɴᴜʀᴜɴ]:\n\n✣ Pembaruan:**\n`{changelog}`'
        if len(changelog_str) > 4096:
            await event.edit("`Changelog Terlalu Besar, Lihat File Untuk Melihatnya.`")
            file = open("output.txt", "w+")
            file.write(changelog_str)
            file.close()
            await event.client.send_file(
                event.chat_id,
                "output.txt",
                reply_to=event.id,
            )
            remove("output.txt")
        else:
            await event.edit(changelog_str)
        return await event.respond('**ᴘᴇʀɪɴᴛᴀʜ ᴜɴᴛᴜᴋ ᴜᴘᴅᴀᴛᴇ ᴘɪɴᴜʀᴜɴ**\n >`.update now`\n >`.update deploy`\n\n__ᴜɴᴛᴜᴋ ᴍᴇɴɢ ᴜᴘᴅᴀᴛᴇ ꜰɪᴛᴜʀ ᴛᴇʀʙᴀʀᴜ ᴅᴀʀɪ ᴘ ɪ ɴ ᴜ ʀ ᴜ ɴ.__')

    if force_update:
        await event.edit(
            '`Sinkronisasi Paksa Ke Kode Userbot Stabil Terbaru, Harap Tunggu .....`')
    else:
        await event.edit('`✲ Proses Update ᴘ ɪ ɴ ᴜ ʀ ᴜ ɴ, Loading....1%`')
        await event.edit('`✲ Proses Update ᴘ ɪ ɴ ᴜ ʀ ᴜ ɴ, Loading....20%`')
        await event.edit('`✲ Proses Update ᴘ ɪ ɴ ᴜ ʀ ᴜ ɴ, Loading....35%`')
        await event.edit('`✲ Proses Update ᴘ ɪ ɴ ᴜ ʀ ᴜ ɴ, Loading....77%`')
        await event.edit('`✲ Proses Update ᴘ ɪ ɴ ᴜ ʀ ᴜ ɴ, Updating...90%`')
        await event.edit('`✲ Proses Update ᴘ ɪ ɴ ᴜ ʀ ᴜ ɴ, Mohon Menunggu....100%`')
    if conf == "now":
        await update(event, repo, ups_rem, ac_br)
        await asyncio.sleep(10)
        await event.delete()
    elif conf == "deploy":
        await deploy(event, repo, ups_rem, ac_br, txt)
        await asyncio.sleep(10)
        await event.delete()
    return


CMD_HELP.update({
    'update':
    ".update"
    "\nUsage: ᴜɴᴛᴜᴋ ᴍᴇɴɢ ᴜᴘᴅᴀᴛᴇ ꜰɪᴛᴜʀ ᴛᴇʀʙᴀʀᴜ ᴅᴀʀɪ ᴘ ɪ ɴ ᴜ ʀ ᴜ ɴ."
    "\n\n.update now"
    "\nUsage: Memperbarui ᴘ ɪ ɴ ᴜ ʀ ᴜ ɴ."
    "\n\n.update deploy"
    "\nUsage: Memperbarui ᴘ ɪ ɴ ᴜ ʀ ᴜ ɴ ᴅᴇɴɢᴀɴ ᴄᴀʀᴀ ᴅᴇᴘʟᴏʏ ᴜʟᴀɴɢ."
})
