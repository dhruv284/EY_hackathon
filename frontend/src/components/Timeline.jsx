export default function Timeline({ stage }) {
  const steps = ["FORM", "AADHAAR", "SANCTION"];
  return (
    <div style={{ display: "flex", gap: 20 }}>
      {steps.map((s) => (
        <div key={s} style={{ fontWeight: stage === s ? "bold" : "normal" }}>
          {s}
        </div>
      ))}
    </div>
  );
}
