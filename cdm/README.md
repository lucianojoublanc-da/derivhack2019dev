# CDM / DAML JSON Translator

Refer to [the guide](../guide/README.md) for more information on how to use this.

## Building

1. Build the DAML model by running

    daml build

2. Build the python application by running

    pipenv install lib/message_integration-0.0.1-py3-none-any.whl
    pipenv install

## Running

Start each of the following commands in a separate shell. Make sure to ***pass all the arguments***.

1. Start the sandbox via

    daml sandbox .daml/dist/cdmIntro-0.0.1.dar -w --ledgerid "MyTestLedger"

2. Start the Http-Json-Api via

    daml json-api --ledger-host localhost --ledger-port 6865 --http-port 7575 --max-inbound-message-size 52428800

Start the example script:

    pipenv run python main.py
