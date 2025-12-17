import { applyLoan } from "../api/loanApi";

export default function LoanForm({ onResult }) {
  const submit = async (e) => {
    e.preventDefault();

    const data = {
      customer_id: e.target.customer_id.value,
      pan: e.target.pan.value,
      full_name: e.target.full_name.value,
      phone: e.target.phone.value,
      requested_amount: Number(e.target.amount.value),
    };

    const res = await applyLoan(data);
    onResult(res, data);
  };

  return (
    <form
      onSubmit={submit}
      className="space-y-8 max-w-xl mx-auto animate-fadeIn"
    >
      {/* Header */}
      <div className="text-center">
        <h3 className="text-3xl font-bold text-slate-800">Apply for Loan</h3>
        <p className="text-slate-500 mt-2 text-sm">
          Quick approval • No paperwork • Secure process
        </p>
      </div>

      {/* Inputs */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <Input name="customer_id" placeholder="Customer ID" />
        <Input name="pan" placeholder="PAN Number" className="uppercase" />
        <Input name="full_name" placeholder="Full Name" span />
        <Input name="phone" placeholder="Phone Number" type="tel" />
        <Input name="amount" placeholder="Loan Amount (₹)" type="number" />
      </div>

      {/* Submit */}
      <button
        type="submit"
        className="w-full py-3 rounded-xl bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white font-semibold shadow-lg hover:shadow-xl hover:scale-[1.02] transition-all"
      >
        🚀 Check Eligibility
      </button>

      {/* Trust */}
      <p className="text-xs text-center text-slate-400">
        🔒 256-bit encrypted • RBI compliant
      </p>
    </form>
  );
}

function Input({ span, className = "", ...props }) {
  return (
    <input
      {...props}
      required
      className={`w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition ${
        span ? "md:col-span-2" : ""
      } ${className}`}
    />
  );
}
