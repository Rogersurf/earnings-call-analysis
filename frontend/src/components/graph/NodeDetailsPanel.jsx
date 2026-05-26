// ============================================================
// FILE: frontend/src/components/graph/NodeDetailsPanel.jsx
// ============================================================

import React from "react";

// ============================================================
// COMPONENT
// ============================================================

export default function NodeDetailsPanel({

    selectedNode
}) {

    // ========================================================
    // EMPTY STATE
    // ========================================================

    if (!selectedNode) {

        return (

            <div className="
                w-full
                h-full
                bg-zinc-900
                border-l
                border-zinc-800
                p-6
                text-zinc-500
            ">

                <h2 className="text-lg font-semibold mb-4">
                    Node Intelligence
                </h2>

                <p>
                    Click a node to inspect
                    semantic details.
                </p>

            </div>
        );
    }

    const data = selectedNode.data;

    // ========================================================
    // RENDER
    // ========================================================

    return (

        <div className="
            w-full
            h-full
            bg-zinc-900
            border-l
            border-zinc-800
            p-6
            overflow-y-auto
        ">

            {/* ============================================= */}
            {/* HEADER */}
            {/* ============================================= */}

            <div className="mb-6">

                <h2 className="
                    text-2xl
                    font-bold
                    text-white
                ">

                    {data.company}

                </h2>

                <p className="
                    text-zinc-400
                    mt-1
                ">

                    {data.ticker}

                </p>

            </div>

            {/* ============================================= */}
            {/* METADATA */}
            {/* ============================================= */}

            <div className="space-y-4">

                <div>

                    <p className="
                        text-zinc-500
                        text-sm
                        mb-1
                    ">

                        Sector

                    </p>

                    <p className="text-white">

                        {data.sector || "Unknown"}

                    </p>

                </div>

                <div>

                    <p className="
                        text-zinc-500
                        text-sm
                        mb-1
                    ">

                        Semantic Similarity

                    </p>

                    <p className="text-white">

                        {data.similarity?.toFixed(3)}

                    </p>

                </div>

            </div>

            {/* ============================================= */}
            {/* THEMES */}
            {/* ============================================= */}

            <div className="mt-8">

                <h3 className="
                    text-white
                    font-semibold
                    mb-3
                ">

                    Themes

                </h3>

                <div className="
                    flex
                    flex-wrap
                    gap-2
                ">

                    {(data.themes || []).map(

                        (theme) => (

                            <div

                                key={theme}

                                className="
                                    px-3
                                    py-1
                                    rounded-full
                                    bg-zinc-800
                                    text-zinc-300
                                    text-sm
                                "
                            >

                                {theme}

                            </div>
                        )
                    )}

                </div>

            </div>

            {/* ============================================= */}
            {/* CHUNK */}
            {/* ============================================= */}

            <div className="mt-8">

                <h3 className="
                    text-white
                    font-semibold
                    mb-3
                ">

                    Semantic Chunk

                </h3>

                <div className="
                    bg-zinc-950
                    border
                    border-zinc-800
                    rounded-xl
                    p-4
                    text-zinc-300
                    text-sm
                    leading-relaxed
                ">

                    {data.chunk}

                </div>

            </div>

        </div>
    );
}