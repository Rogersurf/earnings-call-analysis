import {
  ArrowRight,
  Activity,
  Cpu,
  Cloud,
  Zap,
  TrendingUp,
} from "lucide-react";

/* ====================================================== */
/* ICONS */
/* ====================================================== */

const eventIcons = {
  Semiconductors: Cpu,
  Cloud: Cloud,
  Energy: Zap,
  Hardware: Activity,
};

/* ====================================================== */
/* COLORS */
/* ====================================================== */

const eventColors = {
  Semiconductors: "from-cyan-400 to-blue-500",
  Cloud: "from-violet-400 to-fuchsia-500",
  Energy: "from-yellow-400 to-orange-500",
  Hardware: "from-green-400 to-emerald-500",
};

/* ====================================================== */
/* MAIN */
/* ====================================================== */

export default function BottomTimeline({
  events,
}) {

  return (

    <div className="relative overflow-hidden">

      {/* ========================================= */}
      {/* HEADER */}
      {/* ========================================= */}

      <div className="flex items-center justify-between mb-6">

        <div>

          <h2 className="text-xl font-bold text-white">
            Temporal Propagation Replay
          </h2>

          <p className="text-sm text-gray-400 mt-1">
            Observe how semantic signals propagate across the economy over time
          </p>

        </div>

        <div className="flex items-center gap-2 text-cyan-400 text-sm">

          <TrendingUp size={16} />

          Live Temporal Engine

        </div>

      </div>

      {/* ========================================= */}
      {/* TIMELINE */}
      {/* ========================================= */}

      <div className="overflow-x-auto pb-4 scrollbar-thin scrollbar-thumb-cyan-500/20">

        <div className="flex items-center gap-6 min-w-max pr-10">

          {events.map((event, index) => {

            const Icon =
              eventIcons[event.target] || Activity;

            const gradient =
              eventColors[event.target] ||
              "from-cyan-400 to-blue-500";

            return (

              <div
                key={index}
                className="flex items-center gap-6"
              >

                {/* EVENT CARD */}
                <div className="
                  relative
                  min-w-[300px]
                  bg-[#0f172a]/90
                  border border-cyan-500/10
                  rounded-3xl
                  overflow-hidden
                  backdrop-blur-xl
                  hover:border-cyan-400/30
                  transition-all duration-300
                  hover:scale-[1.02]
                  group
                ">

                  {/* GLOW */}
                  <div className={`
                    absolute inset-0 opacity-10
                    bg-gradient-to-br ${gradient}
                    blur-2xl
                  `} />

                  {/* TOP */}
                  <div className="
                    relative
                    p-5
                    border-b border-cyan-500/10
                    flex items-center justify-between
                  ">

                    <div>

                      <div className="text-xs tracking-[0.2em] text-gray-500">

                        {event.quarter}

                      </div>

                      <h3 className="text-lg font-bold text-white mt-1">

                        {event.target}

                      </h3>

                    </div>

                    <div className={`
                      w-12 h-12 rounded-2xl
                      bg-gradient-to-br ${gradient}
                      flex items-center justify-center
                      shadow-[0_0_30px_rgba(0,255,255,0.15)]
                    `}>

                      <Icon
                        size={22}
                        className="text-black"
                      />

                    </div>

                  </div>

                  {/* BODY */}
                  <div className="relative p-5">

                    <p className="text-gray-300 leading-relaxed text-sm">

                      {event.event}

                    </p>

                    {/* SIGNAL */}
                    <div className="
                      mt-5
                      flex items-center gap-2
                      text-cyan-400 text-xs
                    ">

                      <div className="
                        w-2 h-2 rounded-full
                        bg-cyan-400
                        animate-pulse
                      " />

                      Semantic propagation active

                    </div>

                  </div>

                </div>

                {/* ARROW */}
                {index !== events.length - 1 && (

                  <div className="relative flex items-center">

                    {/* LINE */}
                    <div className="
                      w-20 h-[2px]
                      bg-gradient-to-r
                      from-cyan-400
                      to-violet-500
                    " />

                    {/* ARROW */}
                    <ArrowRight
                      size={20}
                      className="
                        text-cyan-400
                        absolute
                        right-[-10px]
                        drop-shadow-[0_0_8px_rgba(0,255,255,0.5)]
                      "
                    />

                  </div>

                )}

              </div>

            );
          })}

        </div>

      </div>

      {/* ========================================= */}
      {/* BOTTOM GLOW */}
      {/* ========================================= */}

      <div className="
        absolute
        bottom-[-120px]
        left-1/2
        -translate-x-1/2
        w-[700px]
        h-[200px]
        bg-cyan-500/10
        blur-[140px]
        rounded-full
        pointer-events-none
      " />

    </div>
  );
}