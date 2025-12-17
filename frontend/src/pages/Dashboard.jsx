import { useState } from "react";
import LoanForm from "../components/LoanForm";
import AadhaarUpload from "../components/AadhaarUpload";
import SanctionView from "../components/SanctionView";
import Timeline from "../components/Timeline";
import { applyLoan } from "../api/loanApi";

export default function Dashboard() {
  const [pdfBlob, setPdfBlob] = useState(null);
  const [stage, setStage] = useState("FORM");
  const [loanData, setLoanData] = useState(null);
  const [response, setResponse] = useState(null);

  const handleLoanResult = (res, data) => {
    if (!res || !res.status) return;

    setLoanData(data);
    setResponse(res);

    if (res.status === "PENDING") {
      setStage("AADHAAR");
    }

    if (res.status === "APPROVED") {
      setPdfBlob(res.pdfBlob);   // ✅ store PDF
      setStage("SANCTION");
    }
  };


  const handleAadhaarVerified = async () => {
    if (!loanData) return;

    const res = await applyLoan(loanData);
    if (!res || !res.status) return;

    const status = res.status.toUpperCase(); 

    setResponse(res);

    if (status === "APPROVED") {
      setPdfBlob(res.pdfBlob);
      setStage("SANCTION");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-200 flex items-center justify-center p-6">
      <div className="w-full max-w-4xl bg-white rounded-2xl shadow-xl p-8 space-y-8">

        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-slate-800">
            META_MINDS Loan Platform
          </h1>
          <p className="text-slate-500 text-sm">
            Fast • Secure • Paperless Loan Approval
          </p>
        </div>

        {/* Timeline */}
        <Timeline stage={stage} />

        {/* Content */}
        <div className="bg-slate-50 rounded-xl p-6 border border-slate-200">
          {stage === "FORM" && (
            <LoanForm onResult={handleLoanResult} />
          )}

          {stage === "AADHAAR" && (
            <AadhaarUpload onVerified={handleAadhaarVerified} />
          )}

          {stage === "SANCTION" && (
            <SanctionView pdfBlob={pdfBlob} />
          )}

        </div>

        {/* Footer */}
        <div className="text-center text-xs text-slate-400">
          © {new Date().getFullYear()} META_MINDS • All rights reserved
        </div>
      </div>
    </div>
  );
}

