// ============================================================
// FILE: frontend/src/pages/RetrievalChat.jsx
// ============================================================

import React, {

    useState

} from "react";

import RetrievalPanel
    from "../components/retrieval/RetrievalPanel";

import SemanticGraph from "../components/graph/SemanticGraph";

import NodeDetailsPanel from "../components/graph/NodeDetailsPanel";

import {

    fetchQueryGraph

} from "../services/graphService";

import AgentPanel from "../components/agents/AgentPanel";

import {

    fetchAgentInsights

} from "../services/agentService";

// ============================================================
// COMPONENT
// ============================================================

export default function RetrievalChat() {

    // ========================================================
    // STATE
    // ========================================================

    const [query, setQuery] = useState("");

    const [loading, setLoading] = useState(false);

    const [selectedNode, setSelectedNode] = useState(null);

    const [graphData, setGraphData] = useState({

        nodes: [],
        edges: [],
        themes: []
    });

    const [agentInsights, setAgentInsights] = useState([]);

    // ========================================================
    // SEARCH
    // ========================================================

    async function handleSearch() {

        if (!query.trim()) {
            return;
        }

        try {

            setLoading(true);

            // ====================================================
            // GRAPH QUERY
            // ====================================================

            const data = await fetchQueryGraph(

                query,

                5,

                5
            );

            setGraphData({

                nodes: data.nodes || [],

                edges: data.edges || [],

                themes: data.themes || []
            });

            // ====================================================
            // AGENT QUERY
            // ====================================================

            const agentResponse =
                await fetchAgentInsights(
                    query
                );

            setAgentInsights(

                agentResponse.agents || []
            );

        } catch (error) {

            console.error(error);

        } finally {

            setLoading(false);
        }
    }

    // ========================================================
    // NODE CLICK
    // ========================================================

    function handleNodeClick(event, node) {

        setSelectedNode(node);
    }

    // ========================================================
    // RENDER
    // ========================================================

    return (

        <div className="
            w-full
            h-screen
            bg-zinc-950
            text-white
            flex
            flex-col
        ">

            {/* ================================================= */}
            {/* TOP BAR */}
            {/* ================================================= */}

            <div className="
                p-4
                border-b
                border-zinc-800
                flex
                gap-3
            ">

                <input

                    type="text"

                    placeholder="
                        Search semantic propagation...
                    "

                    value={query}

                    onChange={(e) =>
                        setQuery(e.target.value)
                    }

                    className="
                        flex-1
                        bg-zinc-900
                        border
                        border-zinc-700
                        rounded-lg
                        px-4
                        py-3
                        outline-none
                    "
                />

                <button

                    onClick={handleSearch}

                    className="
                        px-6
                        py-3
                        rounded-lg
                        bg-blue-600
                        hover:bg-blue-700
                        transition
                    "
                >

                    {loading
                        ? "Loading..."
                        : "Search"}

                </button>

            </div>

            {/* ================================================= */}
            {/* THEMES */}
            {/* ================================================= */}

            <div className="
                px-4
                py-2
                border-b
                border-zinc-800
                flex
                gap-2
                flex-wrap
            ">

                {graphData.themes.map(

                    (theme) => (

                        <div

                            key={theme}

                            className="
                                px-3
                                py-1
                                rounded-full
                                bg-zinc-800
                                text-sm
                                text-zinc-300
                            "
                        >

                            {theme}

                        </div>
                    )
                )}

            </div>

            {/* ================================================= */}
            {/* MAIN LAYOUT */}
            {/* ================================================= */}

            <div className="
                flex-1
                flex
                overflow-hidden
            ">

                {/* ============================================= */}
                {/* GRAPH */}
                {/* ============================================= */}

                <div className="flex-1 p-4">

                    <SemanticGraph

                        nodes={graphData.nodes}

                        edges={graphData.edges}

                        onNodeClick={handleNodeClick}
                    />

                </div>

                <div className="
                    w-[420px]
                    min-w-[420px]
                    flex
                    flex-col
                    border-l
                    border-zinc-800
                ">

                    {/* ================================================ */}
                    {/* NODE DETAILS */}
                    {/* ================================================ */}

                    <div className="
                        h-[35%]
                        border-b
                        border-zinc-800
                        overflow-hidden
                    ">

                        <NodeDetailsPanel

                            selectedNode={selectedNode}
                        />

                    </div>

                    {/* ============================================ */}
                    {/* RETRIEVAL EVIDENCE */}
                    {/* ============================================ */}

                    <div className="
                        h-[30%]
                        border-b
                        border-zinc-800
                        overflow-hidden
                    ">

                        <RetrievalPanel

                            nodes={graphData?.nodes || []}
                        />

                    </div>

                    {/* ============================================ */}
                    {/* AGENTS */}
                    {/* ============================================ */}

                    <div className="
                        h-[35%]
                        overflow-hidden
                    ">

                        <AgentPanel

                            agents={agentInsights}
                        />

                    </div>

                </div>

            </div>

        </div>
    );
}