<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## MUSIC USERBOT + [User Bot](https://github.com/The-HellBot/HellBot)


## 🚀 <a name="deploy"></a>Deploy To Heroku

- [![Deploy](https://te.legra.ph/file/2a24a198476d4abf505da.jpg)](https://heroku.com/deploy/)



-------------

## [REPL](https://replit.com/@dominator454/stringforbot?v=1)
## ☁️ <a name="self_host"></a>Self Host

```bash
$ git clone https://github.com/The-HellBot/Music
$ cd Music
$ cp sample.env .env
< edit .env with your own values >
$ sudo docker build . -t musicplayer
$ sudo docker run musicplayer
```
## Support
   <a href="https://t.me/dominator_bot_official"><img src="https://img.shields.io/badge/Channel%20Support%3F-yes-green?&style=flat-square?&logo=telegram" width=220px></a></p>
   <a href="https://t.me/dominator_bot_support"><img src="https://img.shields.io/badge/Group%20Support%3F-yes-green?&style=flat-square?&logo=telegram" width=220px></a></p>
  
## ⚒ <a name="configs"></a>Configs

- `API_ID`: Telegram app id.
- `API_HASH`: Telegram app hash.
- `SESSION`: Pyrogram string session. You can generate from [here](https://replit.com/@AsmSafone/genStr).
- `SUDO_USERS`: ID of sudo users (separate multiple ids with space).
- `PREFIX`: Commad prefixes (separate multiple prefix with space). Eg: `! /`
- `LANGUAGE`: An [available](#languages) bot language (can change it anytime). Default: `en`
- `CUSTOM_QUALITY`: Custom stream quality for the userbot in vc. Default: `high`

## 📄 <a name="commands"></a>Commands

Command | Description
:--- | :---
• !ping | Check if alive or not
• !start / !help | Show the help for commands
• !mode / !switch | Switch the stream mode (audio/video)
• !p / !play [song name or youtube link] | Play a song in vc, if already playing add to queue
• !radio / !stream [radio url or stream link] | Play a live stream in vc, if already playing add to queue
• !pl / !playlist [youtube playlist link] | Play the whole youtube playlist at once
• !skip / !next | Skip to the next song
• !m / !mute | Mute the current stream
• !um / !unmute | Unmute the muted stream
• !ps / !pause | Pause the current stream
• !rs / !resume | Resume the paused stream
• !list / !queue | Show the songs in the queue
• !mix / !shuffle | Shuflle the queued playlist
• !loop / !repeat | Enable or disable the loop mode
• !lang / language [language code] | Set the bot language in group
• !ip / !import | Import queue from exported file
• !ep / !export | Export the queue for import in future
• !stop / !leave | Leave from vc and clear the queue

## 🗣 <a name="languages"></a>Languages

```text
en    English
```

## 📃 <a name="license"></a>License

Music Player is licenced under the GNU Affero General Public License v3.0.
Read more [here](./LICENSE).
