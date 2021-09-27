<p align="center"> <img height="120" width="120" src="https://cdn.discordapp.com/attachments/326432556037832704/891739081762033704/3.png" alt="hippalus"/></p>

# <div align="center">Hippalus</div>
<p align="center">A Discord bot useful for League of Legends players. Built using <a href="https://discordpy.readthedocs.io/en/stable/">Discord.py</a> and <a href="https://www.op.gg/">OP.GG</a>. Deployed to Heroku.</p>

## <div align="center">Invite bot to your server</div>
<p align="center">Please refer <a href="https://discordpy.readthedocs.io/en/stable/discord.html">here</a> to read how to create a bot app and invite it to your server.</p>

## <div align="center">Run locally</div>

- You need to have Python 3.9.7 installed.
- You need to have [geckodriver](https://github.com/mozilla/geckodriver/releases) installed and added to your PATH (selenium will search the PATH to find the executable).
- Run `pip install -r requirements.txt` to install dependencies.
- Create a `.env` file and add the following line, replacing ... with your token (you should have the token by now). <br>
  `DISCORD_TOKEN="..."`
- Run `python bot.py` to start the bot.
- The bot should be now online.
  - type `!hippalus` to get a list of the features

## <div align="center">Deploy to Heroku</div>

- Create a Heroku application via the CLI or via the Heroku Dashboard. Connect the app with a GitHub repository and enable automatic builds <br>
    `PS. automatic build means that everytime you push changes to remote, heroku will rebuild and redeploy the bot.`
- Specify build packs via the Heroku CLI
    1. [heroku-integrated-firefox-geckodriver](https://elements.heroku.com/buildpacks/pyronlaboratory/heroku-integrated-firefox-geckodriver) (required for selenium to work)<br>
        `heroku buildpacks:add https://github.com/pyronlaboratory/heroku-integrated-firefox-geckodriver` <br>
    2. [heroku/python](https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-python) (since this bot is made with Python) <br>
        `heroku buildpacks:add heroku/python` <br>
       1. Set Enviroment Variables <br>
           `$ heroku config:set FIREFOX_BIN=/app/vendor/firefox/firefox`<br>
           `$ heroku config:set GECKODRIVER_PATH=/app/vendor/geckodriver/geckodriver`<br>
           `$ heroku config:set LD_LIBRARY_PATH=/usr/local/lib:/usr/lib:/lib:/app/vendor`<br>
           `$ heroku config:set PATH=/usr/local/bin:/usr/bin:/bin:/app/vendor/`<br>
           `$ heroku config:set DISCORD_TOKEN=<YOUR DISCORD TOKEN HERE (FROM DISCORD DEVELOPER PORTAL)>`<br>
    3. Navigate to Deploy page of the Heroku Dashboard and Deploy main branch <br>
    4. After the deploy was successful open a terminal in the root folder of the repo and run <br>
        `$ heroku ps:scale worker=1`
    5. Lastly run `heroku logs --tail` and check the logs. <br>
       You should see the following: <br>
            `app[worker.1]: Logged in as Hippalus with id ...`
    6. The bot should be online on your server <br>
       - type `!hippalus` to get a list of the features