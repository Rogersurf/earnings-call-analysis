const API_BASE =
  "http://192.168.1.158:8000"


export async function semanticSearch(
  query,
  topK = 10,
) {

  const response = await fetch(
    `${API_BASE}/research/query?query=${encodeURIComponent(query)}&top_k=${topK}`
  )

  if (!response.ok) {

    throw new Error(
      "Semantic search failed"
    )
  }

  return response.json()
}


export async function graphSearch(
  query,
  topK = 10,
) {

  const response = await fetch(
    `${API_BASE}/research/graph?query=${encodeURIComponent(query)}&top_k=${topK}`
  )

  if (!response.ok) {

    throw new Error(
      "Graph search failed"
    )
  }

  return response.json()
}