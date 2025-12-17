export default function Timeline({ stage }) {
  const steps = ["FORM", "AADHAAR", "SANCTION"];

  return (
    <div className="flex items-center justify-between max-w-3xl mx-auto">
      {steps.map((step, index) => {
        const isActive = step === stage;
        const isCompleted =
          steps.indexOf(stage) > index;

        return (
          <div key={step} className="flex-1 flex items-center">
            
            {/* Step Circle */}
            <div
              className={`w-9 h-9 flex items-center justify-center rounded-full text-sm font-semibold
              ${
                isCompleted
                  ? "bg-green-500 text-white"
                  : isActive
                  ? "bg-indigo-600 text-white ring-4 ring-indigo-200"
                  : "bg-slate-300 text-slate-600"
              }`}
            >
              {index + 1}
            </div>

            {/* Label */}
            <div className="ml-3">
              <p
                className={`text-sm font-medium ${
                  isActive || isCompleted
                    ? "text-slate-800"
                    : "text-slate-400"
                }`}
              >
                {step}
              </p>
            </div>

            {/* Connector */}
            {index < steps.length - 1 && (
              <div
                className={`flex-1 h-1 mx-4 rounded
                ${
                  isCompleted
                    ? "bg-green-400"
                    : "bg-slate-300"
                }`}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}
