import {
  LayoutDashboard,
  Network,
  Activity,
  BrainCircuit,
  Clock3,
  Search,
  MessagesSquare,
  BellRing,
  Newspaper,
  AlertTriangle,
  Settings,
  Database,
} from "lucide-react";

const sections = [
  {
    title: "MAIN",
    items: [
      { icon: LayoutDashboard, label: "Dashboard" },
      { icon: Network, label: "Graph Intelligence" },
      { icon: Activity, label: "Propagation Explorer" },
      { icon: BrainCircuit, label: "Sector Heatmap" },
      { icon: Clock3, label: "Temporal Replay" },
    ],
  },
  {
    title: "INTELLIGENCE",
    items: [
      { icon: Search, label: "Semantic Signals" },
      { icon: MessagesSquare, label: "Retrieval Chat" },
      { icon: BrainCircuit, label: "Multi-Agent Debate" },
    ],
  },
  {
    title: "MONITORING",
    items: [
      { icon: BellRing, label: "Live Transcripts" },
      { icon: Newspaper, label: "Market News" },
      { icon: AlertTriangle, label: "Alerts & Anomalies" },
    ],
  },
  {
    title: "SYSTEM",
    items: [
      { icon: Database, label: "API & Integrations" },
      { icon: Settings, label: "Settings" },
    ],
  },
];

export default function Sidebar() {

  return (

    <div className="w-72 min-h-screen bg-[#070b17] border-r border-cyan-500/10 flex flex-col">

      {/* LOGO */}
      <div className="px-6 py-8 border-b border-cyan-500/10">

        <h1 className="text-2xl font-black tracking-wide text-white">

          <span className="text-cyan-400">
            EARNINGS
          </span>

          {" "}INTELLIGENCE

        </h1>

        <p className="text-sm text-gray-400 mt-2">
          Financial Semantic Intelligence Platform
        </p>

      </div>

      {/* NAVIGATION */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-8">

        {sections.map((section) => (

          <div key={section.title}>

            <h2 className="text-xs tracking-[0.2em] text-gray-500 mb-4">

              {section.title}

            </h2>

            <div className="space-y-2">

              {section.items.map((item, index) => {

                const Icon = item.icon;

                const active =
                  item.label === "Dashboard";

                return (

                  <button
                    key={index}
                    className={`
                      w-full flex items-center gap-4
                      px-4 py-3 rounded-xl
                      transition-all duration-300
                      border
                      ${
                        active
                          ? "bg-cyan-500/10 border-cyan-400/40 text-cyan-300 shadow-[0_0_20px_rgba(0,255,255,0.15)]"
                          : "border-transparent text-gray-400 hover:bg-[#10182b] hover:text-white"
                      }
                    `}
                  >

                    <Icon size={18} />

                    <span className="text-sm font-medium">
                      {item.label}
                    </span>

                  </button>

                );
              })}

            </div>

          </div>

        ))}

      </div>

      {/* SYSTEM STATUS */}
      <div className="p-4 border-t border-cyan-500/10">

        <div className="bg-green-500/10 border border-green-400/20 rounded-2xl p-4">

          <div className="flex items-center gap-2">

            <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />

            <span className="text-green-300 text-sm font-medium">
              System Operational
            </span>

          </div>

          <p className="text-xs text-gray-400 mt-2">
            AI-LAB connected • WebSocket active
          </p>

        </div>

      </div>

    </div>
  );
}