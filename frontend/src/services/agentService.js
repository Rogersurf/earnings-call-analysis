// ============================================================
// FILE: frontend/src/services/agentService.js
// ============================================================

import axios from "axios";

// ============================================================
// API URL
// ============================================================

const API_URL =
    "http://localhost:8000";

// ============================================================
// FETCH AGENT INSIGHTS
// ============================================================

export async function fetchAgentInsights(

    query
) {

    try {

        const response = await axios.post(

            `${API_URL}/agents/query`,

            {
                query
            }
        );

        return response.data;

    } catch (error) {

        console.error(

            "Agent service error:",

            error
        );

        throw error;
    }
}