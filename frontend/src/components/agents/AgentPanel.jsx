// ============================================================
// FILE: frontend/src/components/agents/AgentPanel.jsx
// ============================================================

import React from "react";

// ============================================================
// COMPONENT
// ============================================================

export default function AgentPanel({

    agents
}) {

    // ========================================================
    // EMPTY STATE
    // ========================================================

    if (!agents || agents.length === 0) {

        return (

            <div className="h-full flex items-center justify-center text-zinc-500">

                No agent insights yet.

            </div>
        );
    }

    // ========================================================
    // RENDER
    // ========================================================

    return (

        <div className="h-full overflow-y-auto p-4 space-y-4 bg-zinc-950">

            {/* ================================================= */}
            {/* TITLE */}
            {/* ================================================= */}

            <div>

                <h2 className="text-xl font-bold text-white">

                    Multi-Agent RAG Insights

                </h2>

                <p className="text-zinc-400 text-sm mt-1">

                    Retrieval-aware semantic synthesis
                    generated from graph expansion
                    and earnings-call evidence.

                </p>

            </div>

            {/* ================================================= */}
            {/* AGENTS */}
            {/* ================================================= */}

            {

                agents.map((agent, index) => (

                    <div

                        key={index}

                        className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 shadow-lg"
                    >

                        {/* ===================================== */}
                        {/* AGENT NAME */}
                        {/* ===================================== */}

                        <div className="mb-3">

                            <h3 className="text-lg font-semibold text-blue-400">

                                {agent.agent}

                            </h3>

                        </div>

                        {/* ===================================== */}
                        {/* ANALYSIS */}
                        {/* ===================================== */}

                        <div className="text-zinc-200 text-sm leading-relaxed whitespace-pre-wrap">

                            {agent.analysis}

                        </div>

                    </div>
                ))
            }

        </div>
    );
}