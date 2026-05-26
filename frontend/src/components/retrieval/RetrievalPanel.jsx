// ============================================================
// FILE: frontend/src/components/retrieval/RetrievalPanel.jsx
// ============================================================

import React from "react";

// ============================================================
// COMPONENT
// ============================================================

export default function RetrievalPanel({

    nodes = []
}) {

    // ========================================================
    // EXTRACT CHUNKS
    // ========================================================

    const chunks = nodes

        .filter(

            (node) =>
                node?.data?.chunk
        )

        .slice(0, 5);

    // ========================================================
    // EMPTY
    // ========================================================

    if (chunks.length === 0) {

        return (

            <div className="
                p-4
                text-zinc-500
            ">

                No retrieved evidence.

            </div>
        );
    }

    // ========================================================
    // RENDER
    // ========================================================

    return (

        <div className="
            h-full
            overflow-y-auto
            bg-zinc-950
            border-t
            border-zinc-800
            p-4
        ">

            {/* ============================================= */}
            {/* TITLE */}
            {/* ============================================= */}

            <div className="mb-4">

                <h2 className="
                    text-lg
                    font-bold
                    text-white
                ">

                    Retrieved Evidence

                </h2>

                <p className="
                    text-zinc-400
                    text-sm
                    mt-1
                ">

                    Top semantic evidence chunks
                    retrieved from earnings calls.

                </p>

            </div>

            {/* ============================================= */}
            {/* CHUNKS */}
            {/* ============================================= */}

            <div className="space-y-4">

                {

                    chunks.map(

                        (node, index) => (

                            <div

                                key={index}

                                className="
                                    bg-zinc-900
                                    border
                                    border-zinc-800
                                    rounded-xl
                                    p-4
                                "
                            >

                                {/* ===================== */}
                                {/* COMPANY */}
                                {/* ===================== */}

                                <div className="mb-2">

                                    <div className="
                                        text-blue-400
                                        font-semibold
                                    ">

                                        {

                                            node.data.company
                                        }

                                    </div>

                                    <div className="
                                        text-zinc-500
                                        text-xs
                                    ">

                                        {

                                            node.data.ticker
                                        }

                                    </div>

                                </div>

                                {/* ===================== */}
                                {/* CHUNK */}
                                {/* ===================== */}

                                <div className="
                                    text-zinc-200
                                    text-sm
                                    leading-relaxed
                                ">

                                    {

                                        node.data.chunk
                                    }

                                </div>

                            </div>
                        )
                    )
                }

            </div>

        </div>
    );
}