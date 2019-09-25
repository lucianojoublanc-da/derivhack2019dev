# CDM / DAML JSON Translator

Refer to [the guide](../guide/README.md) for more information on how to use this.

## Building

Build the python application by running

    pipenv install lib/message_integration-0.0.1-py3-none-any.whl
    pipenv install

## Running

Start the example script. This loads files from `examples`, uses `CDM.json` metadata to round-trip them, and prints the differences between the two (which should be empty).

    pipenv run python main.py
