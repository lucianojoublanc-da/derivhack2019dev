# Hello CDM

This project shows you how to write a simple 'hello world' application that loads a CDM contract onto the ledger, exercises a choice, and reads it back.

## Quickstart

Compile the DAML model, fetch python dependencies.

```sh
daml build
pipenv install
```

Load the templates into the ledger:

```sh
daml sandbox --port 6865 --ledgerid allocs --wall-clock-time .daml/dist/*.dar
```

Start the HTTP rest adapter:

```sh
daml json-api --ledger-host localhost --ledger-port 6865 --http-port 7575
```

Run the main program:

```sh
pipenv run main.py
```

In another shell session, run the bot, and then ***re-run*** the main program to trigger some actions.
```sh
pipenv run bot.py
pipenv run main.py
```
