# Tutorial

This document serves as a step-by-step walkthrough of the examples that are provided under the [ui](../ui) and [bot](../bot) dirs. 

The examples consist of a rudimentary [FIX 5](https://fixtrading.org) allocation workflow. This was chosen as it is similar to the hackathon exercises, yet the standard and workflows differ.

The target audience is expected to be familiar with DAML, including how to write a basic model with scenarios, load them onto the sandbox, and visualize it with the navigator. This is all covered in the [quickstart](https://docs.daml.com/getting-started/quickstart.html), up to the [Integrate with the ledger](https://docs.daml.com/getting-started/quickstart.html#integrate-with-the-ledger) section.

## The Model

Let's have a look at the [ui](../ui) directory:

```
ui
├── daml
│   ├── Fix5.daml
│   ├── Main.daml
│   └── Scenarios.daml
├── daml.yaml
└── python
    └── ui.ipynb
```

This has been created by the DAML assistant, and has the usual directory structure for a DAML project, with the addition of a `python` folder to hold our client/ui code.

You will find the DAML model is split across two files, `Fix5`, which contains only DAML `data` definitions, and the `Main` module, which defines the `templates`. This has been deliberately done to mirror the way the CDM model is structured in the hackathon (except the data model is provided in a pre-built `*.dar` file).

To recap, in our example, `data` are pure data structures that could be code-generated from a formal standard such as FIX in our case, or CDM in the hackathon. For instance, the first data type describes an execution:

```haskell
-- Orders/Executions -------------------------------------------

-- This is a really cut-down version of the actual message
data ExecutionReport =
  ExecutionReport with
    orderID: Text
    parties: [Parties]
    ordStatus: OrdStatus
    tradeDate: Date
    avgPx: Decimal
    cumQty: Int
  deriving (Eq, Show)
```

These data structures would be mapped from a formal specification, but contain no notion of semantics. Also, they are not contracts - they can't live on the ledger on their own. A DAML contract, on the other hand, must have a `signatory`, which **give a DAML `Party` the right to do something**. In the `Main.daml` file, we wrap this type in a `template`:

```haskell
template Execution
  with
    report: ExecutionReport
    broker: Party
  where
    ensure [ broker ] == gatherParties ExecutingFirm [ report ]
    signatory broker
    observer gatherParties ClientID [ report ]
```

Note the `ensure` statement, which enforces that the signatory in this contract is consistent with the parties on the execution. It prevents, for example, a client from creating an execution.

You will find two more contracts, `ProposeBilateralAllocation` and `Allocation` that follow this same pattern. 

Before loading the contracts into the ledger, we can test out that these work through VSCode. Load up VSCode if you haven't done so already with the `daml studio` command from the `ui` directory. Make sure you have the official DAML plugin installed.

If you navigate to the file `Scenario.daml`, click on the link above `setup = scenario do`, and you shoudl get a table that looks something like this (the second table is only visible when clicking 'show archived'):

<head><meta content="text/html; charset=UTF-8" http-equiv="content-type"></head><body class="c80"><h1 class="c29" id="h.5gnzsgly1ltj"><span class="c12 c78">Main:BilateralAllocation</span></h1><a id="t.a9f01c21c189abb65d68966261fedcc477e68700"></a><a id="t.0"></a><table class="c32"><tbody><tr class="c55"><td class="c89" colspan="1" rowspan="1"><p class="c5"><span class="c12 c10">broker</span></p></td><td class="c89" colspan="1" rowspan="1"><p class="c5"><span class="c12 c10">client</span></p></td><td class="c48" colspan="1" rowspan="1"><p class="c5"><span class="c10">id</span></p></td><td class="c8" colspan="1" rowspan="1"><p class="c5"><span class="c10">status</span></p></td><td class="c22" colspan="1" rowspan="1"><p class="c5"><span class="c10">initiator</span></p></td><td class="c76" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.allocID</span></p></td><td class="c51" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.allocTransType</span></p></td><td class="c90" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.allocType</span></p></td><td class="c33" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.refAllocID</span></p></td><td class="c88" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.allocCancReplaceReason</span></p></td><td class="c23" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.ordAllocGrp</span></p></td><td class="c24" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.side</span></p></td><td class="c67" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.instrument.symbol</span></p></td><td class="c26" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.instrument.securityID</span></p></td><td class="c37" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.instrument.securityIDSource</span></p></td><td class="c97" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.avgPx</span></p></td><td class="c79" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.quantity</span></p></td><td class="c59" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.tradeDate</span></p></td><td class="c64" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.settlDate</span></p></td><td class="c57" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.allocGrp</span></p></td><td class="c6" colspan="1" rowspan="1"><p class="c5"><span class="c10">responder</span></p></td><td class="c44" colspan="1" rowspan="1"><p class="c5"><span class="c10">affirmation.allocID</span></p></td><td class="c7" colspan="1" rowspan="1"><p class="c5"><span class="c10">affirmation.parties</span></p></td><td class="c34" colspan="1" rowspan="1"><p class="c5"><span class="c10">affirmation.allocStatus</span></p></td><td class="c77" colspan="1" rowspan="1"><p class="c5"><span class="c10">affirmation.matchStatus</span></p></td><td class="c39" colspan="1" rowspan="1"><p class="c5"><span class="c10">affirmation.allocAckGrp</span></p></td></tr><tr class="c50"><td class="c0" colspan="1" rowspan="1"><p class="c5"><span class="c1">X</span></p></td><td class="c0" colspan="1" rowspan="1"><p class="c5"><span class="c1">X</span></p></td><td class="c72" colspan="1" rowspan="1"><p class="c2"><span class="c1">#1:1</span></p></td><td class="c65" colspan="1" rowspan="1"><p class="c2"><span class="c1">active</span></p></td><td class="c36" colspan="1" rowspan="1"><p class="c2"><span class="c1">&#39;client&#39;</span></p></td><td class="c75" colspan="1" rowspan="1"><p class="c2"><span class="c1">&quot;&quot;</span></p></td><td class="c73" colspan="1" rowspan="1"><p class="c2"><span class="c1">Fix5:AllocTransType:New</span></p></td><td class="c74" colspan="1" rowspan="1"><p class="c2"><span class="c1">Fix5:AllocType:Preliminary</span></p></td><td class="c31" colspan="1" rowspan="1"><p class="c2"><span class="c1">none</span></p></td><td class="c41" colspan="1" rowspan="1"><p class="c2"><span class="c1">none</span></p></td><td class="c27" colspan="1" rowspan="1"><p class="c2"><span class="c1">[]</span></p></td><td class="c13" colspan="1" rowspan="1"><p class="c2"><span class="c1">Fix5:Side:Buy</span></p></td><td class="c82" colspan="1" rowspan="1"><p class="c2"><span class="c1">&quot;BARC&quot;</span></p></td><td class="c17" colspan="1" rowspan="1"><p class="c2"><span class="c1">&quot;GB0031348658&quot;</span></p></td><td class="c71" colspan="1" rowspan="1"><p class="c2"><span class="c1">&quot;ISIN&quot;</span></p></td><td class="c28" colspan="1" rowspan="1"><p class="c2"><span class="c1">140.5200000000</span></p></td><td class="c9" colspan="1" rowspan="1"><p class="c2"><span class="c1">100000</span></p></td><td class="c58" colspan="1" rowspan="1"><p class="c2"><span class="c1">2019-09-06T</span></p></td><td class="c60" colspan="1" rowspan="1"><p class="c2"><span class="c1">2019-09-10T</span></p></td><td class="c87" colspan="1" rowspan="1"><p class="c2"><span class="c1">[Fix5:AllocGrp with allocAccount = &quot;Account1&quot;; allocPrice = 140.5200000000; allocQty = 100000; parties = [(Fix5:Parties with partyID = &quot;client&quot;; partyIDSource = &quot;LEI&quot;; partyRole = Fix5:PartyRole:ClientID), (Fix5:Parties with partyID = &quot;broker&quot;; partyIDSource = &quot;LEI&quot;; partyRole = Fix5:PartyRole:ExecutingFirm)]; allocNetMoney = 14052000.0000000000; allocSettlCurrAmt = 140520.0000000000; allocSettlCurr = &quot;GBP&quot;]</span></p></td><td class="c45" colspan="1" rowspan="1"><p class="c2"><span class="c1">&#39;broker&#39;</span></p></td><td class="c62" colspan="1" rowspan="1"><p class="c2"><span class="c1">&quot;&lt;contract-id&gt;&quot;</span></p></td><td class="c20" colspan="1" rowspan="1"><p class="c2"><span class="c1">[Fix5:Parties with partyID = &quot;client&quot;; partyIDSource = &quot;LEI&quot;; partyRole = Fix5:PartyRole:ClientID, Fix5:Parties with partyID = &quot;broker&quot;; partyIDSource = &quot;LEI&quot;; partyRole = Fix5:PartyRole:ExecutingFirm]</span></p></td><td class="c4" colspan="1" rowspan="1"><p class="c2"><span class="c1">Fix5:AllocStatus:Accepted</span></p></td><td class="c63" colspan="1" rowspan="1"><p class="c2"><span class="c1">Fix5:MatchStatus:Compared</span></p></td><td class="c66" colspan="1" rowspan="1"><p class="c2"><span class="c1">[]</span></p></td></tr></tbody></table><h1 class="c29" id="h.ucygrs1iuqa1"><span class="c12 c78">Main:ProposeBilateralAllocation</span></h1><a id="t.1d372f02c00977c88adb94b85fbc9253088a480b"></a><a id="t.1"></a><table class="c32"><tbody><tr class="c55"><td class="c21" colspan="1" rowspan="1"><p class="c5"><span class="c12 c10">broker</span></p></td><td class="c21" colspan="1" rowspan="1"><p class="c5"><span class="c10 c12">client</span></p></td><td class="c25" colspan="1" rowspan="1"><p class="c5"><span class="c10">id</span></p></td><td class="c6" colspan="1" rowspan="1"><p class="c5"><span class="c10">status</span></p></td><td class="c38" colspan="1" rowspan="1"><p class="c5"><span class="c10">initiator</span></p></td><td class="c34" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.allocID</span></p></td><td class="c92" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.allocTransType</span></p></td><td class="c69" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.allocType</span></p></td><td class="c30" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.refAllocID</span></p></td><td class="c54" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.allocCancReplaceReason</span></p></td><td class="c84" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.ordAllocGrp</span></p></td><td class="c35" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.side</span></p></td><td class="c52" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.instrument.symbol</span></p></td><td class="c46" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.instrument.securityID</span></p></td><td class="c47" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.instrument.securityIDSource</span></p></td><td class="c16" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.avgPx</span></p></td><td class="c70" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.quantity</span></p></td><td class="c7" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.tradeDate</span></p></td><td class="c85" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.settlDate</span></p></td><td class="c68" colspan="1" rowspan="1"><p class="c5"><span class="c10">instruction.allocGrp</span></p></td><td class="c53" colspan="1" rowspan="1"><p class="c5"><span class="c10">responder</span></p></td></tr><tr class="c50"><td class="c11" colspan="1" rowspan="1"><p class="c5"><span class="c1">X</span></p></td><td class="c11" colspan="1" rowspan="1"><p class="c5"><span class="c1">X</span></p></td><td class="c40" colspan="1" rowspan="1"><p class="c2"><span class="c14">#0:0</span></p></td><td class="c45" colspan="1" rowspan="1"><p class="c2"><span class="c14">archived</span></p></td><td class="c61" colspan="1" rowspan="1"><p class="c2"><span class="c14">&#39;client&#39;</span></p></td><td class="c4" colspan="1" rowspan="1"><p class="c2"><span class="c14">&quot;&quot;</span></p></td><td class="c83" colspan="1" rowspan="1"><p class="c2"><span class="c14">Fix5:AllocTransType:New</span></p></td><td class="c56" colspan="1" rowspan="1"><p class="c2"><span class="c14">Fix5:AllocType:Preliminary</span></p></td><td class="c81" colspan="1" rowspan="1"><p class="c2"><span class="c14">none</span></p></td><td class="c3" colspan="1" rowspan="1"><p class="c2"><span class="c14">none</span></p></td><td class="c93" colspan="1" rowspan="1"><p class="c2"><span class="c14">[]</span></p></td><td class="c18" colspan="1" rowspan="1"><p class="c2"><span class="c14">Fix5:Side:Buy</span></p></td><td class="c49" colspan="1" rowspan="1"><p class="c2"><span class="c14">&quot;BARC&quot;</span></p></td><td class="c19" colspan="1" rowspan="1"><p class="c2"><span class="c14">&quot;GB0031348658&quot;</span></p></td><td class="c42" colspan="1" rowspan="1"><p class="c2"><span class="c14">&quot;ISIN&quot;</span></p></td><td class="c91" colspan="1" rowspan="1"><p class="c2"><span class="c14">140.5200000000</span></p></td><td class="c95" colspan="1" rowspan="1"><p class="c2"><span class="c14">100000</span></p></td><td class="c20" colspan="1" rowspan="1"><p class="c2"><span class="c14">2019-09-06T</span></p></td><td class="c86" colspan="1" rowspan="1"><p class="c2"><span class="c14">2019-09-10T</span></p></td><td class="c96" colspan="1" rowspan="1"><p class="c2"><span class="c14">[Fix5:AllocGrp with allocAccount = &quot;Account1&quot;; allocPrice = 140.5200000000; allocQty = 100000; parties = [(Fix5:Parties with partyID = &quot;client&quot;; partyIDSource = &quot;LEI&quot;; partyRole = Fix5:PartyRole:ClientID), (Fix5:Parties with partyID = &quot;broker&quot;; partyIDSource = &quot;LEI&quot;; partyRole = Fix5:PartyRole:ExecutingFirm)]; allocNetMoney = 14052000.0000000000; allocSettlCurrAmt = 140520.0000000000; allocSettlCurr = &quot;GBP&quot;]</span></p></td><td class="c15" colspan="1" rowspan="1"><p class="c2"><span class="c14">&#39;broker&#39;</span></p></td></tr></tbody></table><p class="c2 c94"><span class="c12 c43"></span></p></body>

The VSCode extension runs a local sandbox and executes your scenario, displaying the results. This is handy when you are developing your model and don't want to have to spin up a ledger to visualize the results, as described in the next section.

## Interacting with the Ledger

Now we will start up the sandbox ledger ourselves and create some contracts. First, compile your model:

```sh
daml build
```

This creates a `*.dar` file under `.daml/dist`, which you must load into the ledger so that it knows about your contracts.

Next, we start the sandbox (in a new shell preferrably):

```sh
> daml sandbox --port 6865 --ledgerid allocs --wall-clock-time .daml/dist/*.dar

	Sandbox verbosity changed to INFO
DAML LF Engine supports LF versions: 0, 0.dev, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.dev; Transaction versions: 1, 2, 3, 4, 5, 6, 7, 8; Value versions: 1, 2, 3, 4, 5
Starting plainText server
listening on localhost:6865
   ____             ____
  / __/__ ____  ___/ / /  ___ __ __
 _\ \/ _ `/ _ \/ _  / _ \/ _ \\ \ /
/___/\_,_/_//_/\_,_/_.__/\___/_\_\

Initialized sandbox version 100.13.23 with ledger-id = allocs, port = 6865, dar file = List(.daml/dist/ui-0.0.1.dar), time mode = WallClock, ledger = in-memory, daml-engine = {}

```

The `--ledgerid` switch needs to be consistent with the JWT tokens we will use for authentication in our python code. `--wall-clock-time` is also required; otherwise contract creation will fail.

Now, we start the http REST api (in a new shell preferrably):

```sh
> daml json-api --ledger-host localhost --ledger-port 6865 --http-port 7575

13:05:36.495 [main] INFO  com.digitalasset.http.Main$ - Config(ledgerHost=localhost, ledgerPort=6865, httpPort=7575, applicationId=HTTP-JSON-API-Gateway, maxInboundMessageSize=4194304)
13:05:37.841 [http-json-ledger-api-akka.actor.default-dispatcher-9] INFO  com.digitalasset.http.HttpService$ - Connected to Ledger: allocs
13:05:39.334 [http-json-ledger-api-akka.actor.default-dispatcher-9] INFO  com.digitalasset.http.HttpService$ - Started server: ServerBinding(/127.0.0.1:7575)

```

Finally, start your jupyter notebook, which we will be using as a rudimentary UI:

```sh
jupyter notebook python/ui.ipynb
```

This should open up a web page on `localhost:8888`. You will also need to have the [BeakerX](http://beakerx.com/documentation) extension installed; otherwise some of the controls will fail to render.

If this is the first time you are using jupyter, you can get a quick tutorial through the **Help > User Interface Tour**.

Next, we will create some execution contracts on the ledger. Run all the cells up to and including the "Setup" cell with Shift + Enter (or going to the menu **Cell > Run all above**). This command within the cell sends the HTTP POST request to the process we started with `daml json-api` above:

```python
    requests.post(
        "http://{}:{}/command/create".format(host,port),
        headers = brokerHeader,
        json = execution(round(99.0 + random(), 2), int(1000 * random()))
    )
```

As a side note, you will see that `brokerHeader`, defined at the top of the notebook, has a JWT token that is used to authenticate the party on the http-json api. TODO: link here to the official docs once they're available.

Now, let's check the executions actually exist on the ledger. Run the next cell, "Client", which cointain this call to fetch the contracts:

```python
executionsResponse = requests.post(
    "http://{}:{}/contracts/search".format(host,port),
    json = { "%templates" : [{ "moduleName" : "Main", "entityName" : "Execution"}]},
    headers = clientHeader
)
```

This is similar to the previous call; it provides a URI for the REST endpoint, a token in the header, and some json to filter the results. In fact, we could have fetched all contracts from the shell using `curl` to send a plain HTTP POST request to this process:

```sh
curl  http://localhost:7575/contracts/search --header "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsZWRnZXJJZCI6ImFsbG9jcyIsImFwcGxpY2F0aW9uSWQiOiJhbGxvY3MiLCJwYXJ0eSI6ImNsaWVudCJ9.ayhBmc7qfT1kjF_1AM7RTTQ4ZXsjM9q1sP-CaMYExPg"
```

To end this section, let's recap what we've done:

  * We loaded up our allocations model into a sandbox ledger.
  * We started a process that serves HTTP requests on port 7575.
  * We POSTed to this process from our python worksheet, creating some `Execution` contracts as `broker`
  * We POSTed to this process form our python worksheet, to read back the created contracts as `client`.

To finish off, we suggest you execute the remaining cells in the workbook, reading the comments that explain what is happening.
