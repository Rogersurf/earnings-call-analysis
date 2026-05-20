import API_BASE_URL from "./api";

export async function fetchAgentExplanation(query) {

    try {

        const response = await fetch(
            `${API_BASE_URL}/agents/explain?query=${query}`
        );

        if (!response.ok) {
            throw new Error("Agent request failed");
        }

        return await response.json();

    } catch (error) {

        console.error(
            "Agent explanation error:",
            error
        );

        return null;
    }
}