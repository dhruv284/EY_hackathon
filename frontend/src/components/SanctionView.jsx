export default function SanctionView({ data }) {
  return (
    <div>
      <h3>Loan Approved 🎉</h3>
      <a href={`https://sanction-agent.onrender.com/${data.sanction.sanction_letter}`}>
        Download Sanction Letter
      </a>
    </div>
  );
}
