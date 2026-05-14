import {
  BrainCircuit,
  AlertTriangle,
  Activity,
  Building2,
  Clock3,
  TrendingUp,
  Wifi,
} from "lucide-react";

export default function RightPanel({
  agentStream,
  selectedNode,
}) {

  return (

    <div className="space-y-6">

      {/* ========================================= */}
      {/* NODE INTELLIGENCE */}
      {/* ========================================= */}

      <section className="bg-[#0b1023] rounded-3xl border border-cyan-500/10 overflow-hidden shadow-2xl">

        <div className="px-5 py-4 border-b border-cyan-500/10 flex items-center justify-between">

          <div className="flex items-center gap-3">

            <div className="p-2 rounded-xl bg-cyan-500/10 text-cyan-400">

              <Building2 size={18} />

            </div>

            <div>

              <h2 className="font-bold text-white">
                Node Intelligence
              </h2>

              <p className="text-xs text-gray-500">
                Realtime semantic context
              </p>

            </div>

          </div>

          <div className="flex items-center gap-2 text-green-400 text-xs">

            <Wifi size={12} />

            LIVE

          </div>

        </div>

        <div className="p-5">

          {selectedNode ? (

            <div className="space-y-5">

              <div>

                <div className="text-2xl font-black text-white">
                  {selectedNode.data.label}
                </div>

                <div className="text-sm text-cyan-400 mt-1">
                  {selectedNode.data.sector || "Unknown Sector"}
                </div>

              </div>

              <div className="grid grid-cols-2 gap-4">

                <MetricCard
                  label="Propagation"
                  value="87%"
                  color="cyan"
                />

                <MetricCard
                  label="Risk"
                  value="Moderate"
                  color="red"
                />

                <MetricCard
                  label="Confidence"
                  value="91%"
                  color="green"
                />

                <MetricCard
                  label="Mentions"
                  value="142"
                  color="violet"
                />

              </div>

              <div>

                <div className="text-xs tracking-wide text-gray-500 mb-2">

                  ACTIVE SIGNAL

                </div>

                <div className="bg-cyan-500/10 border border-cyan-400/20 rounded-2xl px-4 py-3 text-cyan-300 text-sm">

                  {selectedNode.data.signal || "No active signal"}

                </div>

              </div>

            </div>

          ) : (

            <div className="text-center py-12">

              <div className="w-16 h-16 rounded-3xl bg-[#111827] mx-auto flex items-center justify-center mb-4">

                <Building2
                  size={28}
                  className="text-gray-500"
                />

              </div>

              <h3 className="text-white font-semibold">
                No Node Selected
              </h3>

              <p className="text-gray-500 text-sm mt-2">
                Click on a graph node to inspect semantic propagation context
              </p>

            </div>

          )}

        </div>

      </section>

      {/* ========================================= */}
      {/* AI AGENT STREAM */}
      {/* ========================================= */}

      <section className="bg-[#0b1023] rounded-3xl border border-cyan-500/10 overflow-hidden shadow-2xl">

        <div className="px-5 py-4 border-b border-cyan-500/10 flex items-center gap-3">

          <div className="p-2 rounded-xl bg-violet-500/10 text-violet-400">

            <BrainCircuit size={18} />

          </div>

          <div>

            <h2 className="font-bold text-white">
              Multi-Agent Reasoning
            </h2>

            <p className="text-xs text-gray-500">
              AI consensus engine
            </p>

          </div>

        </div>

        <div className="max-h-[500px] overflow-y-auto p-5 space-y-4">

          {agentStream.map((item, index) => (

            <div
              key={index}
              className="bg-[#111827] rounded-2xl border border-cyan-500/5 p-4 hover:border-cyan-400/20 transition-all"
            >

              <div className="flex items-start justify-between mb-3">

                <div className="flex items-center gap-3">

                  <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-cyan-400 to-violet-500 flex items-center justify-center text-black font-bold text-sm">

                    AI

                  </div>

                  <div>

                    <div className="text-sm font-semibold text-white">

                      {item.agent}

                    </div>

                    <div className="flex items-center gap-2 text-xs text-gray-500">

                      <Clock3 size={11} />

                      Just now

                    </div>

                  </div>

                </div>

                <div className={`
                  px-3 py-1 rounded-full text-xs font-semibold
                  ${
                    item.type === "alert"
                      ? "bg-red-500/10 text-red-400"
                      : item.type === "warning"
                      ? "bg-yellow-500/10 text-yellow-400"
                      : "bg-cyan-500/10 text-cyan-400"
                  }
                `}>

                  {item.type}

                </div>

              </div>

              <p className="text-sm text-gray-300 leading-relaxed">

                {item.message}

              </p>

              {/* CONFIDENCE */}
              <div className="mt-4">

                <div className="flex justify-between text-xs mb-2">

                  <span className="text-gray-500">
                    Confidence
                  </span>

                  <span className="text-cyan-400">
                    {(item.confidence * 100).toFixed(0)}%
                  </span>

                </div>

                <div className="w-full h-2 rounded-full bg-[#1f2937] overflow-hidden">

                  <div
                    className="h-full bg-gradient-to-r from-cyan-400 to-violet-500 rounded-full"
                    style={{
                      width: `${item.confidence * 100}%`
                    }}
                  />

                </div>

              </div>

            </div>

          ))}

        </div>

      </section>

      {/* ========================================= */}
      {/* LIVE MARKET ALERTS */}
      {/* ========================================= */}

      <section className="bg-[#0b1023] rounded-3xl border border-cyan-500/10 overflow-hidden shadow-2xl">

        <div className="px-5 py-4 border-b border-cyan-500/10 flex items-center gap-3">

          <div className="p-2 rounded-xl bg-red-500/10 text-red-400">

            <AlertTriangle size={18} />

          </div>

          <div>

            <h2 className="font-bold text-white">
              Live Alerts
            </h2>

            <p className="text-xs text-gray-500">
              Semantic anomaly monitoring
            </p>

          </div>

        </div>

        <div className="p-5 space-y-4">

          <AlertCard
            title="Propagation Spike"
            text="AI demand pressure detected across semiconductor supply chain."
            color="red"
          />

          <AlertCard
            title="Transcript Update"
            text="New NVIDIA earnings transcript ingested."
            color="cyan"
          />

          <AlertCard
            title="Sector Acceleration"
            text="Cloud infrastructure heat increased +14%."
            color="green"
          />

        </div>

      </section>

    </div>
  );
}

/* ====================================================== */
/* METRIC CARD */
/* ====================================================== */

function MetricCard({ label, value, color }) {

  const styles = {
    cyan: "text-cyan-400 bg-cyan-500/10",
    red: "text-red-400 bg-red-500/10",
    green: "text-green-400 bg-green-500/10",
    violet: "text-violet-400 bg-violet-500/10",
  };

  return (

    <div className="bg-[#111827] rounded-2xl p-4 border border-cyan-500/5">

      <div className="text-xs text-gray-500 mb-2">
        {label}
      </div>

      <div className={`text-lg font-bold ${styles[color]}`}>
        {value}
      </div>

    </div>
  );
}

/* ====================================================== */
/* ALERT CARD */
/* ====================================================== */

function AlertCard({ title, text, color }) {

  const styles = {
    red: "border-red-500/20 bg-red-500/5",
    cyan: "border-cyan-500/20 bg-cyan-500/5",
    green: "border-green-500/20 bg-green-500/5",
  };

  return (

    <div className={`rounded-2xl border p-4 ${styles[color]}`}>

      <div className="flex items-center gap-2 mb-2">

        <TrendingUp
          size={15}
          className="text-white"
        />

        <h3 className="font-semibold text-white">
          {title}
        </h3>

      </div>

      <p className="text-sm text-gray-400 leading-relaxed">

        {text}

      </p>

    </div>
  );
}