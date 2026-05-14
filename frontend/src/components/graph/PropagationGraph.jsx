import React, { useMemo } from "react";

import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  MarkerType,
} from "reactflow";

import "reactflow/dist/style.css";

/* ====================================================== */
/* NODE COLORS */
/* ====================================================== */

const nodeColors = {
  company: "#00e5ff",
  sector: "#a855f7",
  signal: "#ff6b6b",
};

/* ====================================================== */
/* CUSTOM NODE STYLE */
/* ====================================================== */

function styleNodes(nodes) {

  return nodes.map((node) => {

    const color =
      nodeColors[node.type] || "#00e5ff";

    return {

      ...node,

      style: {

        background:
          "rgba(10,15,30,0.92)",

        color: "white",

        border: `1px solid ${color}`,

        borderRadius: "18px",

        padding: 12,

        width: 180,

        boxShadow: `
          0 0 25px ${color}33,
          inset 0 0 20px rgba(255,255,255,0.02)
        `,

        backdropFilter: "blur(12px)",

        fontSize: "13px",

        fontWeight: 600,

        letterSpacing: "0.03em",
      },

      data: {
        ...node.data,
        label: (
          <div className="space-y-1">

            <div
              className="font-bold"
              style={{ color }}
            >
              {node.data.label}
            </div>

            {node.data.sector && (
              <div className="text-[11px] text-gray-400">
                {node.data.sector}
              </div>
            )}

            {node.data.signal && (
              <div
                className="text-[11px]"
                style={{ color }}
              >
                {node.data.signal}
              </div>
            )}

          </div>
        ),
      },
    };
  });
}

/* ====================================================== */
/* CUSTOM EDGES */
/* ====================================================== */

function styleEdges(edges) {

  return edges.map((edge) => ({

    ...edge,

    animated: true,

    type: "smoothstep",

    markerEnd: {
      type: MarkerType.ArrowClosed,
      color: edge.style?.stroke || "#00e5ff",
    },

    style: {

      stroke:
        edge.style?.stroke || "#00e5ff",

      strokeWidth: 2.2,

      filter: `
        drop-shadow(0 0 10px ${
          edge.style?.stroke || "#00e5ff"
        })
      `,
    },

    labelStyle: {
      fill: "#94a3b8",
      fontSize: 11,
    },

  }));
}

/* ====================================================== */
/* MAIN COMPONENT */
/* ====================================================== */

export default function PropagationGraph({
  nodes,
  edges,
  onNodeClick,
}) {

  const styledNodes =
    useMemo(() => styleNodes(nodes), [nodes]);

  const styledEdges =
    useMemo(() => styleEdges(edges), [edges]);

  return (

    <div className="relative w-full h-full rounded-3xl overflow-hidden bg-[#050816] border border-cyan-500/10">

      {/* ========================================= */}
      {/* CYBER BACKGROUND */}
      {/* ========================================= */}

      <div className="absolute inset-0">

        {/* RADIAL GLOW */}
        <div className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-cyan-500/10 blur-[120px] rounded-full" />

        <div className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-violet-500/10 blur-[120px] rounded-full" />

      </div>

      {/* ========================================= */}
      {/* FLOW HEADER */}
      {/* ========================================= */}

      <div className="absolute top-5 left-5 z-20 bg-[#0b1023]/80 backdrop-blur-xl border border-cyan-500/10 rounded-2xl px-5 py-3">

        <div className="flex items-center gap-3">

          <div className="w-3 h-3 rounded-full bg-green-400 animate-pulse" />

          <div>

            <div className="text-sm font-bold text-white">
              Semantic Propagation Active
            </div>

            <div className="text-xs text-gray-400">
              Realtime multi-sector inference
            </div>

          </div>

        </div>

      </div>

      {/* ========================================= */}
      {/* LEGEND */}
      {/* ========================================= */}

      <div className="absolute bottom-5 left-5 z-20 bg-[#0b1023]/80 backdrop-blur-xl border border-cyan-500/10 rounded-2xl px-5 py-4 space-y-3">

        <Legend color="#00e5ff" label="Company" />
        <Legend color="#a855f7" label="Sector" />
        <Legend color="#ff6b6b" label="Signal" />

      </div>

      {/* ========================================= */}
      {/* REACT FLOW */}
      {/* ========================================= */}

      <ReactFlow
        nodes={styledNodes}
        edges={styledEdges}
        fitView
        onNodeClick={onNodeClick}
        proOptions={{
          hideAttribution: true,
        }}
      >

        {/* GRID */}
        <Background
          gap={28}
          size={1}
          color="#132038"
        />

        {/* MINIMAP */}
        <MiniMap
          pannable
          zoomable
          style={{
            backgroundColor: "#0b1023",
            border:
              "1px solid rgba(0,255,255,0.1)",
            borderRadius: 16,
          }}
          nodeColor={(node) =>
            nodeColors[node.type] || "#00e5ff"
          }
        />

        {/* CONTROLS */}
        <Controls
          style={{
            background: "#0b1023",
            border:
              "1px solid rgba(0,255,255,0.1)",
            borderRadius: 16,
            overflow: "hidden",
          }}
        />

      </ReactFlow>

    </div>
  );
}

/* ====================================================== */
/* LEGEND */
/* ====================================================== */

function Legend({ color, label }) {

  return (

    <div className="flex items-center gap-3">

      <div
        className="w-3 h-3 rounded-full"
        style={{
          background: color,
          boxShadow: `0 0 10px ${color}`,
        }}
      />

      <span className="text-sm text-gray-300">
        {label}
      </span>

    </div>
  );
}