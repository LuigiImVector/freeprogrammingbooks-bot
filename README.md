# Free programming books: Telegram bot

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Description

Un-official Telegram bot of [free-programming-books](https://github.com/EbookFoundation/free-programming-books/).

[![TELEGRAM](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/freeprogrammingbooks_bot)

## Contributing

#### Self-hosting

1. Fork this repository

2. ```sh
    $ git clone https://github.com/YourUsername/freeprogrammingbooks-bot.git
    $ cd freeprogrammingbooks-bot
    $ git remote add upstream https://github.com/LuigiImVector/freeprogrammingbooks-bot.git
    $ git fetch upstream
    $ git checkout -b newLocalBranchName upstream/main
    ```

3. Deploy app using [Heroku](https://heroku.com/deploy?template=https://github.com/LuigiImVector/freeprogrammingbooks-bot)

4. ```sh
    $ npm install -g heroku
    $ heroku login
    $ heroku pg:psql --app app-name < test/database.sql
    $ pip install -r requirements.txt
    ```

5. Setup autodeploy from github using `newLocalBranchName`

6. ```sh
    # After some changes
    $ git push -u origin newOriginBranchName
    ```

7. Open `https://app-name.herokuapp.com/` if the bot doesn't start (mainly the first time)

If you want to test the app     locally before committing, read [Heroku documentation](https://devcenter.heroku.com/articles/heroku-local).


#### Improve code

Create a Pull Request detailing the changes made.