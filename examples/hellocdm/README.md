# Hello CDM

This project shows you how to write a simple 'hello world' application that loads a CDM contract onto the ledger, exercises a choice, and reads it back.

## Quickstart

Compile the DAML model, fetch python dependencies.

```sh
daml build
pipenv install ../../resources/message_integration-0.0.1-py3-none-any.whl
```

Load the templates into the ledger:

```sh
daml sandbox --port 6865 --ledgerid hellocdm --static-time .daml/dist/*.dar
```

Start the HTTP rest adapter:

```sh
daml json-api --ledger-host localhost --ledger-port 6865 --http-port 7575 --max-inbound-message-size 52428800
```

Run the main program:

```sh
pipenv run python/main.py
```

In another shell session, run the bot, and then ***re-run*** the main program to trigger some actions.
```sh
pipenv run python/bot.py &
pipenv run python/main.py
```

## Tutorial

In this section we are going to walk throught the app step-by-step.

### Loading the DAML model onto a local ledger

First, have a look at the directory structure:
```sh
hellocdm
├── CashTransfer.json
├── daml
│   ├── Main.daml
│   └── Org/Isda/Cdm
├── daml.yaml
├── Pipfile
├── Pipfile.lock
├── python
│   ├── bot.py
│   └── main.py
├── README.md
└── ui
    ├── package.json
    ├── public
    ├── README.md
    ├── src
    └── yarn.lock
```

You will find our DAML template in `daml/Main.daml`.

```haskell
template Transfer
  with
    event : CDM.Event
    owner : Party
    obs   : Party
  where
    signatory owner
    observer obs

    key (owner, getGlobalKey event) : (Party, Text)
    maintainer key._1

    controller owner can
      SayHello : ContractId Transfer 
        with whomToGreet: Text
        do -- Need to project deep field this.contract.eventIdentifier[0].assignedIdentifier[0].value and version
          create this with event = updateIdentifier "CDM" event
```

This is a minimal template, which has only the bare requirements. It has some data, under `event`, and an `owner`, which will be the `signatory`. It has a single choice, `SayHello`, which updates the contract by setting `contract.eventIdentifier[0].assignedIdentifier[0].value` to `Hello, World!`, and incrementing `version`. This is done in a separate function, `update`, of which only the signature is shown above.

The CDM data model describing `CDM.Event`, is under `daml/Org/Isda/Cdm`, but we don't need to worry about it for this for the time being.

Bear in mind that a ledger can only house contracts instantiated from `template`s. Data can not live on it's own on the ledger (by anology to SQL you must create a record in a table - you can't upload a plain data type).

Now, let's start the ledger and http services:

```sh
daml build 
daml sandbox --port 6865 --ledgerid hellocdm --static-time .daml/dist/*.dar
```

The first command compiles our model to bytecode.

The second command will start a ledger locally. It's important that we don't change the `--ledgerid hellocdm`, as this is used for authentication using JWT. It's also importat to pass `--static-time`, as DABL does not support wall-clock time, and creation of contracts would fail; this also means that we need to pass a `meta` element in any creation messages to the ledger, which we'll explain in the next section.

Now, let's start the HTTP service, so we can create contracts and query the ledger:

```sh
daml json-api --ledger-host localhost --ledger-port 6865 --http-port 7575 --max-inbound-message-size 52428800
```

Note the `--max-inbound-message-size`, which we require, to be able to process CDM messages. If you forget this, the process will fail with a related message on start-up.

### Talking CDM with the ledger

Now let's have a look at `python/main.py`. It has four methods which correspond to these four steps:

1. `loadCDMFile` simply opens the `Event.json` file and loads it into a python dictionary. This file would be provided to you in the Hackathon. When this is run in the script, it outputs something like this:

```json
#### Loading CDM JSON from 'CashTransfer.json' ####
Loaded the following JSON object:
{'action': 'NEW', 'eventDate': {'day': 20, 'month': 3, 'year': 2018}, 'eventEffect': {'transfer': [{'globalReference': '69e7b2f5'}]}, 'eventIdentifier': [{'assignedIdentifier': [{'identifier': {'value': 'payment-1'}, 'version': 1}], 'issuerReference': {'globalReference': 'baa9cf67', 'externalReference': 'party1'}, 'meta': {'globalKey': '4576e46b'}}], 'eventQualifier': 'CashTransfer', 'messageInformation': {'messageId': {'value': '1486297', 'meta': {'scheme': 'http://www.party1.com/message-id'}}, 'sentBy': {'value': '894500DM8LVOSCMP9T34'}, 'sentTo': [{'value': '49300JZDC6K840D7F79'}]}, 'meta': {'globalKey': '14801403'}, 'party': [{'meta': {'globalKey': 'baa9cf67', 'externalKey': 'party1'}, 'partyId': [{'value': '894500DM8LVOSCMP9T34', 'meta': {'scheme': 'http://www.fpml.org/coding-scheme/external/iso17442'}}]}, {'meta': {'globalKey': 'a275c2fe', 'externalKey': 'party2'}, 'partyId': [{'value': '549300JZDC6K840D7F79', 'meta': {'scheme': 'http://www.fpml.org/coding-scheme/external/iso17442'}}]}], 'primitive': {'transfer': [{'cashTransfer': [{'amount': {'amount': 1480, 'currency': {'value': 'USD'}, 'meta': {'globalKey': '7c20311f'}}, 'payerReceiver': {'payerPartyReference': {'globalReference': 'baa9cf67', 'externalReference': 'party1'}, 'receiverPartyReference': {'globalReference': 'a275c2fe', 'externalReference': 'party2'}}}], 'meta': {'globalKey': '69e7b2f5'}, 'settlementDate': {'adjustedDate': {'value': {'day': 22, 'month': 3, 'year': 2018}}}}]}, 'timestamp': [{'dateTime': '2018-03-20T18:13:51Z', 'qualification': 'EVENT_CREATION_DATE_TIME'}]}
```

2. `convertCDMJsonToAdmlJson` changes the schema from the official CDM to be compatible with the ledger HTTP api. Running this would output the following:

```json
#### Converting to DAML JSON, wrapping in an 'Event' contract ####
Resulting JSON object:
{'account': [], 'action': 'ActionEnum_New', 'eventDate': '2018-03-20', 'eventEffect': {'contract': [], 'effectedContract': [], 'effectedExecution': [], 'execution': [], 'productIdentifier': [], 'transfer': [{'globalReference': '69e7b2f5'}]}, 'eventIdentifier': [{'assignedIdentifier': [{'identifier': {'value': 'payment-1'}, 'version': 1}], 'issuerReference': {'globalReference': 'baa9cf67', 'externalReference': 'party1'}, 'meta': {'globalKey': '4576e46b'}}], 'eventQualifier': 'CashTransfer', 'messageInformation': {'copyTo': [], 'messageId': {'value': '1486297', 'meta': {'scheme': 'http://www.party1.com/message-id'}}, 'sentBy': {'value': '894500DM8LVOSCMP9T34'}, 'sentTo': [{'value': '49300JZDC6K840D7F79'}]}, 'meta': {'globalKey': '14801403'}, 'party': [{'meta': {'globalKey': 'baa9cf67', 'externalKey': 'party1'}, 'partyId': [{'value': '894500DM8LVOSCMP9T34', 'meta': {'scheme': 'http://www.fpml.org/coding-scheme/external/iso17442'}}], 'person': []}, {'meta': {'globalKey': 'a275c2fe', 'externalKey': 'party2'}, 'partyId': [{'value': '549300JZDC6K840D7F79', 'meta': {'scheme': 'http://www.fpml.org/coding-scheme/external/iso17442'}}], 'person': []}], 'primitive': {'allocation': [], 'contractFormation': [], 'execution': [], 'inception': [], 'observation': [], 'quantityChange': [], 'reset': [], 'transfer': [{'cashTransfer': [{'amount': {'amount': 1480, 'currency': {'value': 'USD'}, 'meta': {'globalKey': '7c20311f'}}, 'breakdown': [], 'payerReceiver': {'payerPartyReference': {'globalReference': 'baa9cf67', 'externalReference': 'party1'}, 'receiverPartyReference': {'globalReference': 'a275c2fe', 'externalReference': 'party2'}}}], 'commodityTransfer': [], 'meta': {'globalKey': '69e7b2f5'}, 'securityTransfer': [], 'settlementDate': {'adjustedDate': {'value': '2018-03-22'}}}]}, 'timestamp': [{'dateTime': {'dateTime': '2018-03-20T18:13:51Z', 'timezone': 'UTC'}, 'qualification': 'EventTimestampQualificationEnum_eventCreationDateTime'}]}
```
Although both are JSON, the are subtle differences in how the CDM and DAML are encoded. This simply calls an external library to do this conversion for you. Compare for example, the `timestamp` and `qualification` (last two fields) with the output of step one.

3. `writeDAMLJsonToLedger` uses the `requests` library to make an HTTP POST request to create the contract from the previous section. The command is very simple:

```python
  return requests.post(
    httpEndpointPrefix + "/command/create",
    headers = tokenHeader,
    json = {
      "templateId" : {
        "moduleName": "Main",
        "entityName": contractName
      },
      "meta" : {
        "ledgerEffectiveTime": epoch # Wall time unsupported on DABL
      },
      "argument": {
        "event": damlDict,
        "owner": signatoryName
      }
    }
```

Notable is the `tokenHeader`, which must be passed to authenticate with the HTTP adapter. It is a digest of `argument.owner` and the ledger id (`hellocdm`), generated on https://JWT.io following [these instructions](https://docs.daml.com/json-api/index.html#example-session). Without this field, the HTTP adapter will reject the request.

There is also a `meta.ledgerEffectiveTime` member which is not required for the local sandbox, but is mandatory for DABL, which doesn't expose a concept of ledger time. This is used in conjunction with the `--static-time` switch we used to start the ledger in the first section.

Finally, the `argument` is the DAML-encoded CDM message we created in the previous section.

This returns an `HttpResponse` object, which is rendered as the HTTP 200 response code, if everything worked ok.

4. `readDAMLJsonFromLedger` is similar to the previous method. Reads the contracts we just generated back from the sandbox. It posts an argument `%templates` to the HTTP endpoint, which can be used to filter specific types of contracts:

```python
requests.post(
    ...
    json = {
      "%templates" : [ 
        {
          "moduleName" : "Main",
          "entityName" : contractName 
        }
      ]
    }
  )
```

5. `exerciseChoice` is the final step and is used to exercise the `SayHello` choice on our contract. Again, it's very similar to the other HTTP calls. Besides the aforementioned header and meta blocks, it requires a `contractId`, `choice` and `argument` to pass to the DAML choice. In our example, the choice is `SayHello`, and the argument is the greeting message. The script calls this with `World`, to update the contract identifier to "Hello, World!".

```python
  return requests.post(
    ...
    json = {
      ...
      "contractId": contractIdToExerciseOn,
      "choice": choiceName,
      "argument": choiceArguments,
    }
  )
```

Finally, let's test out the script:

```sh
pipenv install ../../resources/message_integration-0.0.1-py3-none-any.whl
pipenv run python/main.py
```

You should see some output from each step as it's executed, showing the HTTP responses. If you inspect the ledger now, you should see some new contracts.

### Workflow Automation

We now turn to the file `python/bot.py` which shows how to automate workflows. It uses the python [DAZL](https://github.com/lucianojoublanc-da/dazl-client) api to talk directly to the ledger, instead of making HTTP calls. 

You'll see the file has two annotated methods, which register callbacks:

```python

@user.ledger_init()
async def onInit(event: InitEvent):
  print("Ready & listening for new `Event` contracts ... ")

@user.ledger_created("Main.Event")
async def onCreate(event: ContractCreateEvent):
  allContracts = user.find(template = "Main.Event")
  ...
  user.submit_exercise(contract.cid, "SayHello", { "whomToGreet" : "CDM"})

network.run_forever()
```

The first, `ledger_init` is executed once the API is ready and connected to the ledger.

The second, `ledger_created` is executed whenever a new contract is created on the ledger. In our example, we exercise the same choice we did in our main script, but changed the id to `Hello, CDM!` (instead of `Hello, World!`).

The last line blocks the script and sits in a loop, making the above call-backs each time an event occurs.

We can now start up the script
```sh
$ pipenv run python python/bot.py
Ready & listening for new `Event` contracts ... 
```

Now, run the main script again, in a separate shell. The bot should print out something like:
```sh
payment-1
I have already greeted contract ##2:0, ignoring.
Hello, World!
Greeting (exercising choice) on contract # #3:1
payment-1
I have already greeted contract ##2:0, ignoring.
Hello, World!
Greeting (exercising choice) on contract # #3:1
Tried to send a command and failed!
```

The bot checks to see whether it's already greeted each contract (the id should equal "Hello, CDM!" in this case), and if not, it updates it.

Curiously, you'll note that the last line says "Tried to send a command and failed!". Your script may spew a lot of output and go into an infinte loop.
The reason for this is that _both_ our `main.py` and the `bot.py` are racing to update the same contract. To resolve this, comment out the lines related to

```python
httpExerciseResponse = exerciseChoice(...)
```

in the main script and run it again. The script should now work correctly.
