import { uploadAadhaar } from "../api/loanApi";

export default function AadhaarUpload({ onVerified }) {
  const submit = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const res = await uploadAadhaar(formData);

    if (res.status === "VERIFIED") {
      alert("Aadhaar Verified");
      onVerified(); // NOW this re-triggers apply-loan
    } else {
      alert("Aadhaar verification failed");
    }
  };

  return (
    <form onSubmit={submit}>
      <h3>Upload Aadhaar</h3>

      <input
        name="customer_id"
        placeholder="Customer ID (e.g. C009)"
        required
      />
      <input
        name="aadhaar_number"
        placeholder="12-digit Aadhaar Number"
        required
      />
      <input
        name="aadhaar_file"
        type="file"
        required
      />

      <button type="submit">Verify Aadhaar</button>
    </form>
  );
}
