// ============================================================
// FILE: frontend/src/components/graph/SemanticGraph.jsx
// ============================================================

import React from "react";

import ReactFlow, {

    Background,
    Controls,
    MiniMap

} from "reactflow";

import "reactflow/dist/style.css";
import dagre from "dagre";

// ============================================================
// DAGRE LAYOUT
// ============================================================

const dagreGraph = new dagre.graphlib.Graph();

dagreGraph.setDefaultEdgeLabel(
    () => ({})
);

const nodeWidth = 220;

const nodeHeight = 80;

// ============================================================
// AUTO LAYOUT
// ============================================================

function getLayoutedElements(

    nodes,

    edges
) {

    dagreGraph.setGraph({

        rankdir: "LR",

        nodesep: 80,

        ranksep: 180
    });

    // ========================================================
    // NODES
    // ========================================================

    nodes.forEach((node) => {

        dagreGraph.setNode(

            node.id,

            {

                width: nodeWidth,

                height: nodeHeight
            }
        );
    });

    // ========================================================
    // EDGES
    // ========================================================

    edges.forEach((edge) => {

        dagreGraph.setEdge(

            edge.source,

            edge.target
        );
    });

    // ========================================================
    // LAYOUT
    // ========================================================

    dagre.layout(dagreGraph);

    // ========================================================
    // APPLY POSITIONS
    // ========================================================

    const layoutedNodes = nodes.map(

        (node) => {

            const nodeWithPosition =
                dagreGraph.node(node.id);

            node.position = {

                x:
                    nodeWithPosition.x,

                y:
                    nodeWithPosition.y
            };

            return node;
        }
    );

    return {

        nodes: layoutedNodes,

        edges
    };
}

// ============================================================
// FORMAT NODES
// ============================================================

function formatNodes(nodes) {

    return nodes.map((node, index) => ({

        id: String(node.id),

        position: {

            x: index * 250,

            y:
                node.type === "source"
                    ? 100
                    : 400,
        },

        data: {

            ...node.data,

            label: `
        ${node.data.company}
        (${node.data.ticker})
            `
        },

        style: {

            background: "#18181b",

            color: "white",

            border: "1px solid #3f3f46",

            borderRadius: "12px",

            padding: "10px",

            width: 180,

            fontSize: "12px",
        }
    }));
}

// ============================================================
// FORMAT EDGES
// ============================================================

function formatEdges(edges) {

    return edges.map((edge) => ({

        id: edge.id,

        source: String(edge.source),

        target: String(edge.target),

        animated: false,

        style: {

            stroke: "#52525b",

            strokeWidth: 1.5
        }
    }));
}

// ============================================================
// COMPONENT
// ============================================================

export default function SemanticGraph({

    nodes = [],

    edges = [],

    onNodeClick
}) {

    const formattedNodes =
        formatNodes(nodes);

    const formattedEdges =
        formatEdges(edges);

    const layouted =
        getLayoutedElements(

            formattedNodes,

            formattedEdges
        );

    console.log(
        "GRAPH NODES:",
        formattedNodes
    );

    console.log(
        "GRAPH EDGES:",
        formattedEdges
    );

    return (

        <div className="w-full h-full bg-black rounded-xl">

            <ReactFlow

                nodes={layouted.nodes}

                edges={layouted.edges}

                onNodeClick={onNodeClick}

                fitView
            >

                <Background />

                <Controls />

                <MiniMap />

            </ReactFlow>

        </div>
    );
}