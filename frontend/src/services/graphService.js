// ============================================================
// FILE: frontend/src/services/graphService.js
// ============================================================

import axios from "axios";

// ============================================================
// API BASE URL
// ============================================================

const API_BASE_URL = "http://localhost:8000";

// ============================================================
// QUERY GRAPH
// ============================================================

export async function fetchQueryGraph(

    query,

    top_k_chunks = 5,

    neighbors_per_chunk = 5
) {

    try {

        const response = await axios.post(

            `${API_BASE_URL}/graph/query`,

            {

                query,

                top_k_chunks,

                neighbors_per_chunk
            }
        );

        return response.data;

    } catch (error) {

        console.error(
            "Graph retrieval error:",
            error
        );

        throw error;
    }
}