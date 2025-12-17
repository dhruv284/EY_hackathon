const BASE_URL = "https://master-agent-hiye.onrender.com";
export async function applyLoan(data) {
  const res = await fetch(`${BASE_URL}/apply-loan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  const contentType = res.headers.get("content-type");

  // ✅ Approved → PDF
  if (contentType && contentType.includes("application/pdf")) {
    const blob = await res.blob();
    return {
      status: "APPROVED",
      pdfBlob: blob,
    };
  }

  // ❌ Rejected / Pending
  return await res.json();
}
export async function uploadAadhaar(formData) {
  const res = await fetch(
    "https://ey-hackathon-adgl.onrender.com/verify/aadhaar",
    {
      method: "POST",
      body: formData,
    }
  );
  return res.json();
}
