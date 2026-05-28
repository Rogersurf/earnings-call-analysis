// ============================================================
// FILE:
// frontend/src/components/intelligence/PropagationPanel.jsx
// ============================================================

import React from "react";

// ============================================================
// COMPONENT
// ============================================================

export default function PropagationPanel({

    propagationTargets = [],

    signalDetails = [],
}) {

    // ========================================================
    // EMPTY STATE
    // ========================================================

    if (
        propagationTargets.length === 0
    ) {

        return (

            <div className="
                h-full
                flex
                items-center
                justify-center
                text-zinc-500
                text-sm
                border-t
                border-zinc-800
                bg-zinc-950
            ">

                No propagation intelligence yet.

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
            border-t
            border-zinc-800
            bg-zinc-950
            p-4
        ">

            {/* ================================================= */}
            {/* TITLE */}
            {/* ================================================= */}

            <div className="mb-6">

                <h2 className="
                    text-lg
                    font-bold
                    text-white
                ">

                    Propagation Intelligence

                </h2>

                <p className="
                    text-zinc-400
                    text-sm
                    mt-1
                ">

                    Business-aware semantic
                    propagation signals extracted
                    from retrieval evidence.

                </p>

            </div>

            {/* ================================================= */}
            {/* TARGETS */}
            {/* ================================================= */}

            <div className="mb-8">

                <h3 className="
                    text-sm
                    uppercase
                    tracking-wide
                    text-cyan-400
                    mb-4
                ">

                    Propagation Targets

                </h3>

                <div className="space-y-3">

                    {

                        propagationTargets.map(

                            (
                                target,
                                index
                            ) => {

                                const [
                                    name,
                                    score
                                ] = target;

                                return (

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

                                        <div className="
                                            flex
                                            items-center
                                            justify-between
                                        ">

                                            <div>

                                                <div className="
                                                    text-white
                                                    font-semibold
                                                ">

                                                    {name}

                                                </div>

                                                <div className="
                                                    text-zinc-500
                                                    text-xs
                                                    mt-1
                                                ">

                                                    Semantic
                                                    propagation
                                                    target

                                                </div>

                                            </div>

                                            <div className="
                                                text-cyan-400
                                                font-bold
                                                text-lg
                                            ">

                                                {
                                                    Number(
                                                        score
                                                    ).toFixed(2)
                                                }

                                            </div>

                                        </div>

                                    </div>
                                );
                            }
                        )
                    }

                </div>

            </div>

            {/* ================================================= */}
            {/* SIGNAL DETAILS */}
            {/* ================================================= */}

            <div>

                <h3 className="
                    text-sm
                    uppercase
                    tracking-wide
                    text-violet-400
                    mb-4
                ">

                    Detected Signals

                </h3>

                <div className="space-y-3">

                    {

                        signalDetails

                            .slice(0, 10)

                            .map(

                                (
                                    signal,
                                    index
                                ) => (

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

                                        {/* ================= */}
                                        {/* TOP */}
                                        {/* ================= */}

                                        <div className="
                                            flex
                                            items-center
                                            justify-between
                                            mb-3
                                        ">

                                            <div>

                                                <div className="
                                                    text-white
                                                    font-semibold
                                                ">

                                                    {
                                                        signal.signal
                                                    }

                                                </div>

                                                <div className="
                                                    text-zinc-500
                                                    text-xs
                                                    mt-1
                                                ">

                                                    {
                                                        signal.company
                                                    }

                                                    {" • "}

                                                    {
                                                        signal.ticker
                                                    }

                                                </div>

                                            </div>

                                            <div className="
                                                text-violet-400
                                                font-semibold
                                            ">

                                                {
                                                    Number(
                                                        signal.weighted_score
                                                    ).toFixed(2)
                                                }

                                            </div>

                                        </div>

                                        {/* ================= */}
                                        {/* TARGET */}
                                        {/* ================= */}

                                        <div className="
                                            flex
                                            items-center
                                            gap-2
                                            flex-wrap
                                        ">

                                            <div className="
                                                px-3
                                                py-1
                                                rounded-lg
                                                bg-cyan-500/10
                                                text-cyan-300
                                                text-xs
                                            ">

                                                {
                                                    signal.target
                                                }

                                            </div>

                                            <div className="
                                                px-3
                                                py-1
                                                rounded-lg
                                                bg-violet-500/10
                                                text-violet-300
                                                text-xs
                                            ">

                                                Signal Strength:
                                                {" "}
                                                {
                                                    signal.signal_strength
                                                }

                                            </div>

                                        </div>

                                    </div>
                                )
                            )
                    }

                </div>

            </div>

        </div>
    );
}