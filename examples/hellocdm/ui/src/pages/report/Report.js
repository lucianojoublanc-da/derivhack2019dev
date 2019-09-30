import React from "react";
import Contracts from "../../components/Contracts/Contracts";
import { useLedgerDispatch, useLedgerState, getContracts, sendCommand, fetchContracts } from "../../context/LedgerContext";
import { useUserState } from "../../context/UserContext";

export default function Report() {

  const user = useUserState();
  const ledger = useLedgerState();
  const ledgerDispatch = useLedgerDispatch();
  const events = getContracts(ledger, "Main", "Event");

  const exerciseChoice = async (c, whomToGreet) => {
    const command = {
      templateId: { moduleName: "Main", entityName: "Event" },
      contractId: c.contractId,
      choice: "SayHello",
      argument: { whomToGreet },
      meta: { ledgerEffectiveTime: 0 }
    };
    await sendCommand(ledgerDispatch, user.token, "exercise", command, () => {}, () => {});
    await fetchContracts(ledgerDispatch, user.token, () => {}, () => {});
  }

  return (
    <>
      <Contracts
        contracts={events}
        columns={[
          ["ContractId", "contractId"],
          ["Identifier", "argument.contract.eventIdentifier.0.assignedIdentifier.0.identifier.value"],
          ["Version", "argument.contract.eventIdentifier.0.assignedIdentifier.0.version"],
          ["Amount", "argument.contract.primitive.transfer.0.cashTransfer.0.amount.amount"],
          ["Ccy", "argument.contract.primitive.transfer.0.cashTransfer.0.amount.currency.value"],
          ["Payer", "argument.contract.primitive.transfer.0.cashTransfer.0.payerReceiver.payerPartyReference.externalReference"],
          ["Receiver", "argument.contract.primitive.transfer.0.cashTransfer.0.payerReceiver.receiverPartyReference.externalReference"],
        ]}
        actions={[["Say Hello", exerciseChoice, "Whom to greet"]]}
      />
    </>
  );
}

