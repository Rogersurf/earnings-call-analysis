import {
  Search,
  Bell,
  Activity,
  Database,
  BrainCircuit,
  AlertTriangle,
  Wifi,
  Sparkles,
} from "lucide-react";

export default function TopBar() {

  return (

    <header className="h-20 border-b border-cyan-500/10 bg-[#050816]/95 backdrop-blur-xl flex items-center justify-between px-8">

      {/* LEFT */}
      <div className="flex items-center gap-8">

        {/* LIVE */}
        <div className="flex items-center gap-3">

          <div className="relative">

            <div className="w-3 h-3 rounded-full bg-green-400 animate-pulse" />

            <div className="absolute inset-0 rounded-full bg-green-400 blur-md opacity-70 animate-pulse" />

          </div>

          <div>

            <div className="text-sm font-semibold text-white tracking-wide">
              LIVE SYSTEM
            </div>

            <div className="text-xs text-gray-500">
              Realtime semantic propagation active
            </div>

          </div>

        </div>

        {/* MARKET STATUS */}
        <div className="hidden xl:flex items-center gap-6">

          <StatusCard
            icon={Database}
            label="Transcripts"
            value="9,069"
            color="cyan"
          />

          <StatusCard
            icon={BrainCircuit}
            label="Agents"
            value="4 Active"
            color="violet"
          />

          <StatusCard
            icon={Activity}
            label="Propagations"
            value="42"
            color="green"
          />

          <StatusCard
            icon={AlertTriangle}
            label="Anomalies"
            value="3"
            color="red"
          />

        </div>

      </div>

      {/* CENTER SEARCH */}
      <div className="flex-1 flex justify-center px-12">

        <div className="w-full max-w-2xl relative">

          <Search
            size={18}
            className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500"
          />

          <input
            type="text"
            placeholder="Search company, signal, transcript, sector, agent..."
            className="
              w-full
              bg-[#0b1120]
              border border-cyan-500/10
              rounded-2xl
              h-12
              pl-12
              pr-6
              text-sm
              text-white
              placeholder:text-gray-500
              outline-none
              focus:border-cyan-400/40
              focus:shadow-[0_0_20px_rgba(0,255,255,0.08)]
              transition-all
            "
          />

        </div>

      </div>

      {/* RIGHT */}
      <div className="flex items-center gap-5">

        {/* MARKET */}
        <div className="hidden lg:flex items-center gap-2 px-4 py-2 rounded-xl bg-[#0d1324] border border-cyan-500/10">

          <Sparkles
            size={16}
            className="text-cyan-400"
          />

          <span className="text-sm text-gray-300">
            AI Propagation Engine Online
          </span>

        </div>

        {/* NOTIFICATION */}
        <button
          className="
            relative
            w-11 h-11
            rounded-2xl
            bg-[#0d1324]
            border border-cyan-500/10
            flex items-center justify-center
            hover:border-cyan-400/30
            transition-all
          "
        >

          <Bell
            size={18}
            className="text-gray-300"
          />

          <div className="absolute top-2 right-2 w-2 h-2 rounded-full bg-red-400 animate-pulse" />

        </button>

        {/* USER */}
        <div className="flex items-center gap-3 pl-2">

          <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center text-black font-bold">

            RB

          </div>

          <div className="hidden md:block">

            <div className="text-sm font-semibold text-white">
              Roger Braun
            </div>

            <div className="flex items-center gap-2 text-xs text-green-400">

              <Wifi size={12} />

              AI-LAB Connected

            </div>

          </div>

        </div>

      </div>

    </header>
  );
}

/* ---------- STATUS CARD ---------- */

function StatusCard({ icon: Icon, label, value, color }) {

  const colors = {
    cyan: "text-cyan-400 bg-cyan-500/10",
    violet: "text-violet-400 bg-violet-500/10",
    green: "text-green-400 bg-green-500/10",
    red: "text-red-400 bg-red-500/10",
  };

  return (

    <div className="flex items-center gap-3 px-4 py-2 rounded-2xl bg-[#0d1324] border border-cyan-500/10">

      <div className={`p-2 rounded-xl ${colors[color]}`}>

        <Icon size={15} />

      </div>

      <div>

        <div className="text-xs text-gray-500">
          {label}
        </div>

        <div className="text-sm font-semibold text-white">
          {value}
        </div>

      </div>

    </div>
  );
}