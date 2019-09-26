import requests
from datetime import date, time

brokerHeader = { "Authorization" : """Bearer xxxx"""}
clientHeader = { "Authorization" : """Bearer xxxx"""}
host = "localhost"
port = "7575"
endpoint = "https://{}:{}".format(host, port)
metadataFileName = "../cdm/CDM.json"

def loadCDMFile(fileName):

  """Opens a file containing a CDM JSON instance, and decodes into a Python
     dictionary."""

  return {}

def convertCDMJsonToDAMLJson(cdmDict):

  """Given a CDM dict, convert it into a dict that can be understood by the
     DAML HTTP REST service"""

  return {}

def writeDAMLJsonToLedger(damlDict, contractName, signatoryName, httpEndpointPrefix):

  """Given a dict containing a DAML contract, load to the ledger via the HTTP
     REST service. Return resulting HTTP code."""

  return 404

def readDAMLJsonFromLedger(contractName, signatoryName, httpEndpointPrefix):

  """Given the contract name, query ledger for all such contracts, returning
     them as a list."""

  return []

def exerciseSayHello(cashXferContractId, signatoryName, whomToGreet):

  """Exercises 'SayHello' on a CashTransfer contract.
  This sets the `contract.eventIdentifier.assignedIdentifier.identifier.value` 
  to the given text, and increments the `version` by one.
  Return the new contract ID.
  """

  return "#9999999999:9999999999"
  
if __name__ == '__main__' : 
  print("#### Loading CDM JSON from 'CashTransfer.json' ####")
  cdmJson = loadCDMFile("CashTransfer.json")
  print("Loaded the following JSON object:")
  print(cdmJson)

  print("#### Converting to DAML JSON, wrapping in an 'Event' contract ####")
  damlJson = convertCDMJsonToDAMLJson(cdmJson)
  print("Resulting JSON object:")
  print(damlJson)

  print("#### Sending Event contract to ledger as Alice ####")
  httpCreateResponse = writeDAMLJsonToLedger(damlJson, "Event", "Alice", endpoint)
  print("HTTP service responded: {}".format(httpCreateResponse))

  if httpCreateResponse == 200:
    print("#### Reading Event contracts from Ledger as Alice ####")
    httpContractsResponse = readDAMLJsonFromLedger("Event", "Alice", endpoint)
    print("HTTP service responded: " + httpContractResponse.json())

    if httpContractResponse == 200:
      print("#### Exercising `SayHello` on the first `CashTransfer` contract ####")
      firstContract = httpContractResponse.json()["result"]["activeContracts"][0]
      httpExerciseResponse = exerciseSayHello(firstContract, "Alice", endpoint)

    else:
      print("#### Failed trying to exercise the new contract ###")
      print(httpExerciseResponse.json())

  else:
    print("There was a problem creating the contract:")
    print(httpCreateResponse.json())
