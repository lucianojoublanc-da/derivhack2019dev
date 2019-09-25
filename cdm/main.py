import json
import os
from dictdiffer import diff
import requests

from message_integration.metadata.cdm.cdmMetaDataReader import CdmMetaDataReader
from message_integration.metadata.damlTypes import Record
from message_integration.strategies.jsonCdmDecodeStrategy import JsonCdmDecodeStrategy
from message_integration.strategies.jsonCdmEncodeStrategy import JsonCdmEncodeStrategy

if __name__ == '__main__':
  with open('CDM.json') as metadataRaw:

    metadata = CdmMetaDataReader().fromJSON(json.load(metadataRaw))

    for filename in os.listdir('examples'):
      if filename.endswith("json"):
        with open('examples/' + filename) as inJson:
          # Decode json to match http-json-api
          inJsonDict = json.load(inJson)
          outJsonDict = JsonCdmDecodeStrategy(metadata).decode(inJsonDict, Record("Event"))
              
          # Encode
          inJsonDict2 = JsonCdmEncodeStrategy(metadata).encode(outJsonDict, Record("Event"))

          # Compare
          difference = list(diff(inJsonDict, inJsonDict2))
          print("Difference for " + filename + ": " + str(difference))
