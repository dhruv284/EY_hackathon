import { uploadAadhaar } from "../api/loanApi";

export default function AadhaarUpload({ onVerified }) {
  const submit = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const res = await uploadAadhaar(formData);

    if (res.status === "VERIFIED") {
      alert("Aadhaar Verified");
      await onVerified(e.target.customer_id.value);; // re-triggers apply-loan
    } else {
      alert("Aadhaar verification failed");
    }
  };

  return (
    <form
      onSubmit={submit}
      className="max-w-md mx-auto bg-white rounded-2xl shadow-lg border border-slate-200 p-8 space-y-6"
    >
      {/* Header */}
      <div className="text-center space-y-2">
        <h3 className="text-2xl font-bold text-slate-800">
          Aadhaar Verification
        </h3>
        <p className="text-sm text-slate-500">
          Upload your Aadhaar to continue
        </p>
      </div>

      {/* Inputs */}
      <div className="space-y-4">
        <input
          name="customer_id"
          placeholder="Customer ID (e.g. C009)"
          required
          className="w-full px-4 py-3 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500 outline-none"
        />

        <input
          name="aadhaar_number"
          placeholder="12-digit Aadhaar Number"
          required
          className="w-full px-4 py-3 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500 outline-none"
        />

        <input
          name="aadhaar_file"
          type="file"
          required
          className="w-full text-sm file:mr-4 file:py-2 file:px-4
                     file:rounded-lg file:border-0
                     file:bg-indigo-50 file:text-indigo-700
                     hover:file:bg-indigo-100"
        />
      </div>

      {/* Submit */}
      <button
        type="submit"
        className="w-full py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold shadow-md hover:shadow-lg hover:scale-[1.02] transition"
      >
        🔐 Verify Aadhaar
      </button>

      {/* Trust */}
      <p className="text-xs text-center text-slate-400">
        Your Aadhaar data is encrypted & securely processed
      </p>
    </form>
  );
}

