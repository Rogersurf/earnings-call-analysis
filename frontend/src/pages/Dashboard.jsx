import React, { useState } from "react";
import { motion } from "framer-motion";

import Sidebar from "../components/layout/Sidebar";
import TopBar from "../components/layout/TopBar";

import PropagationGraph from "../components/graph/PropagationGraph";

import RightPanel from "../components/panels/RightPanel";
import BottomTimeline from "../components/panels/BottomTimeline";

import {
  initialNodes,
  initialEdges,
  agentStreamMock,
  propagationTimeline,
} from "../data/mockData";

export default function Dashboard() {

  const [selectedNode, setSelectedNode] =
    useState(null);

  return (

    <div className="min-h-screen bg-[#050816] text-white flex">

      {/* SIDEBAR */}
      <Sidebar />

      {/* MAIN */}
      <div className="flex-1 flex flex-col overflow-y-auto">

        {/* TOPBAR */}
        <TopBar />

        {/* CONTENT */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="p-6 space-y-6"
        >

          {/* ================================================= */}
          {/* HERO METRICS */}
          {/* ================================================= */}

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="grid grid-cols-5 gap-4"
          >

            <MetricCard
              title="Total Transcripts"
              value="9,069"
              subtitle="+234 today"
              border="border-cyan-500/10"
              subtitleColor="text-green-400"
            />

            <MetricCard
              title="Active Signals"
              value="128"
              subtitle="+18 detected"
              border="border-green-500/10"
              subtitleColor="text-green-400"
            />

            <MetricCard
              title="Propagation Alerts"
              value="2"
              subtitle="Critical"
              border="border-red-500/10"
              subtitleColor="text-red-400"
            />

            <MetricCard
              title="AI Confidence"
              value="87%"
              subtitle="Stable"
              border="border-blue-500/10"
              subtitleColor="text-green-400"
            />

            <MetricCard
              title="Market Sentiment"
              value="Bullish"
              subtitle="+12% this week"
              border="border-purple-500/10"
              valueColor="text-purple-400"
              subtitleColor="text-green-400"
            />

          </motion.div>

          {/* ================================================= */}
          {/* MAIN GRID */}
          {/* ================================================= */}

          <div className="grid grid-cols-12 gap-6">

            {/* GRAPH */}
            <motion.div
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.35 }}
              className="col-span-8 bg-[#0b1023] rounded-2xl border border-cyan-500/10 p-4 shadow-2xl"
            >

              <div className="flex items-center justify-between mb-4">

                <div>

                  <h2 className="text-xl font-bold">
                    Semantic Propagation Graph
                  </h2>

                  <p className="text-gray-400 text-sm">
                    Real-time economic signal propagation
                  </p>

                </div>

                <div className="flex items-center gap-2 text-green-400 text-sm">

                  <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />

                  LIVE

                </div>

              </div>

              <div className="h-[450px] rounded-xl overflow-hidden">

                <PropagationGraph
                  nodes={initialNodes}
                  edges={initialEdges}
                  onNodeClick={(event, node) =>
                    setSelectedNode(node)
                  }
                />

              </div>

            </motion.div>

            {/* RIGHT PANEL */}
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.45 }}
              className="col-span-4"
            >

              <RightPanel
                agentStream={agentStreamMock}
                selectedNode={selectedNode}
              />

            </motion.div>

          </div>

          {/* ================================================= */}
          {/* ALERTS + FEEDS */}
          {/* ================================================= */}

          <motion.div
            initial={{ opacity: 0, y: 25 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.55 }}
            className="grid grid-cols-3 gap-6"
          >

            {/* ALERTS */}
            <FeedCard
              title="Recent Alerts"
              border="border-red-500/10"
            >

              <AlertItem
                title="High Propagation Detected"
                text="AI demand signal spreading through semiconductor supply chain."
                color="text-red-400"
                border="border-red-500/20"
              />

              <AlertItem
                title="Semantic Anomaly"
                text="Unexpected divergence in energy transcripts."
                color="text-yellow-400"
                border="border-yellow-500/20"
              />

            </FeedCard>

            {/* TRANSCRIPTS */}
            <FeedCard
              title="Latest Transcripts"
              border="border-cyan-500/10"
            >

              {[
                "NVDA Q2 2025",
                "TSMC Q1 2025",
                "AMD Q1 2025",
                "Microsoft Q2 2025",
              ].map((item) => (

                <div
                  key={item}
                  className="
                    bg-[#111827]
                    rounded-xl
                    p-4
                    hover:bg-[#172036]
                    transition
                    cursor-pointer
                  "
                >

                  {item}

                </div>

              ))}

            </FeedCard>

            {/* HEATMAP */}
            <FeedCard
              title="Sector Heatmap"
              border="border-purple-500/10"
            >

              {[
                ["Semiconductors", "92%"],
                ["Cloud", "81%"],
                ["Energy", "54%"],
                ["Retail", "45%"],
              ].map(([sector, value]) => (

                <div key={sector}>

                  <div className="flex justify-between mb-1">

                    <span>
                      {sector}
                    </span>

                    <span className="text-cyan-400">
                      {value}
                    </span>

                  </div>

                  <div className="w-full h-2 bg-[#1f2937] rounded-full overflow-hidden">

                    <div
                      className="h-full bg-gradient-to-r from-cyan-400 to-purple-500"
                      style={{
                        width: value,
                      }}
                    />

                  </div>

                </div>

              ))}

            </FeedCard>

          </motion.div>

          {/* ================================================= */}
          {/* TIMELINE */}
          {/* ================================================= */}

          <motion.div
            initial={{ opacity: 0, y: 25 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.65 }}
            className="bg-[#0b1023] rounded-2xl border border-cyan-500/10 p-5"
          >

            <BottomTimeline
              events={propagationTimeline}
            />

          </motion.div>

        </motion.div>

      </div>

    </div>
  );
}

/* ===================================================== */
/* METRIC CARD */
/* ===================================================== */

function MetricCard({
  title,
  value,
  subtitle,
  border,
  valueColor = "text-white",
  subtitleColor,
}) {

  return (

    <div className={`
      bg-[#0b1023]
      ${border}
      rounded-2xl
      p-5
      border
      hover:border-cyan-400/20
      transition-all
      hover:scale-[1.02]
    `}>

      <p className="text-gray-400 text-sm">
        {title}
      </p>

      <h2 className={`text-3xl font-bold mt-2 ${valueColor}`}>
        {value}
      </h2>

      <span className={`text-sm ${subtitleColor}`}>
        {subtitle}
      </span>

    </div>
  );
}

/* ===================================================== */
/* FEED CARD */
/* ===================================================== */

function FeedCard({
  title,
  border,
  children,
}) {

  return (

    <div className={`
      bg-[#0b1023]
      rounded-2xl
      border
      ${border}
      p-5
      space-y-4
    `}>

      <h2 className="text-lg font-bold">
        {title}
      </h2>

      {children}

    </div>
  );
}

/* ===================================================== */
/* ALERT ITEM */
/* ===================================================== */

function AlertItem({
  title,
  text,
  color,
  border,
}) {

  return (

    <div className={`
      bg-[#111827]
      rounded-xl
      p-4
      border
      ${border}
    `}>

      <p className={`${color} font-semibold`}>
        {title}
      </p>

      <p className="text-sm text-gray-400 mt-1">
        {text}
      </p>

    </div>
  );
}