import React from "react";
import Contracts from "../../components/Contracts/Contracts";
import { useLedgerState, getContracts } from "../../context/LedgerContext";

function Default() {

  const ledger = useLedgerState();
  const events = getContracts(ledger, "Main", "Event");

  return (
    <>
      <Contracts contracts={events} />
    </>
  );
}

export default Default