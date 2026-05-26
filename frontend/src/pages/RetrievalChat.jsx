import { useState } from "react";

import {
  searchSemantic
} from "../services/retrievalService";

import {
  fetchGraph
} from "../services/graphService";

import PropagationGraph from
  "../components/graph/PropagationGraph";

export default function RetrievalChat() {

  // ==================================================
  // STATES
  // ==================================================

  const [query, setQuery] =
    useState("");

  const [results, setResults] =
    useState([]);

  const [graphData, setGraphData] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  // ==================================================
  // HANDLE SEND
  // ==================================================

  async function handleSend() {

    if (!query.trim()) return;

    setLoading(true);

    try {

      // ----------------------------------------------
      // RETRIEVAL RESULTS
      // ----------------------------------------------

      const retrievalData =
        await searchSemantic(query);

      if (retrievalData?.results) {

        setResults(
          retrievalData.results
        );
      }

      // ----------------------------------------------
      // GRAPH EXPANSION
      // ----------------------------------------------

      const graph =
        await fetchGraph(query);

      if (graph?.results) {

        setGraphData(
          graph.results
        );
      }

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);
    }
  }

  // ==================================================
  // UI
  // ==================================================

  return (

    <div
      className="
        min-h-screen
        bg-black
        text-white
        p-8
      "
    >

      {/* ========================================= */}
      {/* TITLE */}
      {/* ========================================= */}

      <h1
        className="
          text-4xl
          font-bold
          mb-8
        "
      >
        Semantic Intelligence Platform
      </h1>

      {/* ========================================= */}
      {/* INPUT */}
      {/* ========================================= */}

      <div
        className="
          flex
          gap-4
          mb-10
        "
      >

        <input

          type="text"

          value={query}

          onChange={(e) =>
            setQuery(e.target.value)
          }

          placeholder="
            Explore semantic narratives...
          "

          className="
            flex-1
            bg-zinc-900
            border
            border-zinc-700
            rounded-2xl
            px-6
            py-4
            text-white
            outline-none
          "
        />

        <button

          onClick={handleSend}

          className="
            bg-cyan-500
            hover:bg-cyan-400
            text-black
            font-bold
            px-8
            rounded-2xl
          "
        >
          Search
        </button>

      </div>

      {/* ========================================= */}
      {/* LOADING */}
      {/* ========================================= */}

      {loading && (

        <p
          className="
            text-zinc-400
            mb-6
          "
        >
          Building semantic graph...
        </p>
      )}

      {/* ========================================= */}
      {/* RETRIEVAL RESULTS */}
      {/* ========================================= */}

      <div
        className="
          grid
          gap-6
        "
      >

        {results.map((result, idx) => (

          <div

            key={idx}

            className="
              bg-zinc-900
              border
              border-zinc-800
              rounded-3xl
              p-6
            "
          >

            <div
              className="
                flex
                justify-between
                items-center
                mb-4
              "
            >

              <h2
                className="
                  text-xl
                  font-bold
                "
              >
                {result.company}
                {" "}
                ({result.ticker})
              </h2>

              <span
                className="
                  text-cyan-400
                  text-sm
                "
              >
                Similarity:
                {" "}
                {result.similarity
                  ?.toFixed(3)}
              </span>

            </div>

            <p
              className="
                text-zinc-300
                leading-relaxed
              "
            >
              {result.chunk_text}
            </p>

          </div>
        ))}

      </div>

      {/* ========================================= */}
      {/* GRAPH */}
      {/* ========================================= */}

      {graphData && (

        <div
          className="
            h-[700px]
            mt-12
            border
            border-cyan-500/20
            rounded-3xl
            overflow-hidden
          "
        >

          <PropagationGraph

            nodes={graphData.nodes}

            edges={graphData.edges}

          />

        </div>
      )}

    </div>
  );
}