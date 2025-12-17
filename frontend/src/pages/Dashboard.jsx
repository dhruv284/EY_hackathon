import { useState } from "react";
import LoanForm from "../components/LoanForm";
import AadhaarUpload from "../components/AadhaarUpload";
import SanctionView from "../components/SanctionView";
import Timeline from "../components/Timeline";
import { applyLoan } from "../api/loanApi";

export default function Dashboard() {
  const [stage, setStage] = useState("FORM");
  const [loanData, setLoanData] = useState(null);
  const [response, setResponse] = useState(null);

  // called after FORM submit
  const handleLoanResult = (res, data) => {
    setLoanData(data);
    setResponse(res);

    if (res.status === "PENDING") {
      setStage("AADHAAR");
    }

    if (res.status === "APPROVED") {
      setStage("SANCTION");
    }
  };

  // called after Aadhaar verified
  const handleAadhaarVerified = async () => {
    const res = await applyLoan(loanData);
    setResponse(res);

    if (res.status === "APPROVED") {
      setStage("SANCTION");
    }
  };

  return (
    <div style={{ padding: 30 }}>
      <h1>META_MINDS Loan Platform</h1>

      <Timeline stage={stage} />

      {stage === "FORM" && (
        <LoanForm onResult={handleLoanResult} />
      )}

      {stage === "AADHAAR" && (
        <AadhaarUpload onVerified={handleAadhaarVerified} />
      )}

      {stage === "SANCTION" && response && (
        <SanctionView data={response} />
      )}
    </div>
  );
}
