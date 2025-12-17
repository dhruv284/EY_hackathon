export default function SanctionView({ data }) {
  return (
    <div className="max-w-lg mx-auto bg-white rounded-2xl shadow-xl border border-slate-200 p-8 text-center space-y-6">
      
      {/* Success Icon */}
      <div className="flex justify-center">
        <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center">
          <span className="text-3xl">🎉</span>
        </div>
      </div>

      {/* Title */}
      <h3 className="text-2xl font-bold text-slate-800">
        Loan Approved
      </h3>

      <p className="text-sm text-slate-500">
        Your loan request has been successfully approved.
      </p>

      {/* Download Link */}
      <a
        href={`http://localhost:9007${data.sanction.sanction_letter}`}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-block w-full py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold shadow-md hover:shadow-lg hover:scale-[1.02] transition"
      >
        📄 Download Sanction Letter
      </a>

      {/* Trust text */}
      <p className="text-xs text-slate-400">
        This document is digitally signed and legally valid.
      </p>
    </div>
  );
}
