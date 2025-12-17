import { useEffect } from "react";

export default function SanctionView({ pdfBlob }) {
  useEffect(() => {
    if (!pdfBlob) return;

    const url = URL.createObjectURL(pdfBlob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "sanction_letter.pdf";
    a.click();

    return () => URL.revokeObjectURL(url);
  }, [pdfBlob]);

  return (
    <div className="max-w-lg mx-auto bg-white rounded-2xl shadow-xl border border-slate-200 p-8 text-center space-y-6">
      
      <div className="flex justify-center">
        <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center">
          <span className="text-3xl">🎉</span>
        </div>
      </div>

      <h3 className="text-2xl font-bold text-slate-800">
        Loan Approved
      </h3>

      <p className="text-sm text-slate-500">
        Your sanction letter has been downloaded successfully.
      </p>

      <button
        onClick={() => {
          const url = URL.createObjectURL(pdfBlob);
          const a = document.createElement("a");
          a.href = url;
          a.download = "sanction_letter.pdf";
          a.click();
        }}
        className="w-full py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold shadow-md hover:shadow-lg transition"
      >
        📄 Download Again
      </button>

      <p className="text-xs text-slate-400">
        This document is digitally signed and legally valid.
      </p>
    </div>
  );
}
