import API_BASE_URL from "./api";

export async function fetchPropagationGraph() {

    try {

        const response = await fetch(
            `${API_BASE_URL}/graph/propagation`
        );

        if (!response.ok) {
            throw new Error("Graph request failed");
        }

        return await response.json();

    } catch (error) {

        console.error(
            "Graph retrieval error:",
            error
        );

        return null;
    }
}