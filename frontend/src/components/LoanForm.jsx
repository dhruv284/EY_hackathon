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
    <form onSubmit={submit}>
      <h3>Apply for Loan</h3>

      <input name="customer_id" placeholder="Customer ID (e.g. C001)" />
      <input name="pan" placeholder="PAN (e.g. ABCDE1234F)" />
      <input name="full_name" placeholder="Full Name" />
      <input name="phone" placeholder="Phone Number" />
      <input name="amount" placeholder="Loan Amount" />

      <button type="submit">Submit</button>
    </form>
  );
}
