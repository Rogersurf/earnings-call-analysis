import { useState } from "react"

import {
  semanticSearch,
} from "../../services/researchService"


export default function SemanticSearch({
  onResults,
}) {

  const [query, setQuery] =
    useState("")

  const [loading, setLoading] =
    useState(false)

  async function handleSearch() {

    if (!query.trim()) return

    setLoading(true)

    try {

      const results =
        await semanticSearch(query)

      onResults(results)

    } catch (error) {

      console.error(error)

    } finally {

      setLoading(false)
    }
  }

  return (

    <div className="flex gap-4 w-full">

      <input
        className="border rounded p-2 w-full"
        placeholder="Search semantic propagation..."
        value={query}
        onChange={(e) =>
          setQuery(e.target.value)
        }
      />

      <button
        onClick={handleSearch}
        className="bg-black text-white px-4 py-2 rounded"
      >
        {loading
          ? "Loading..."
          : "Search"}
      </button>

    </div>
  )
}