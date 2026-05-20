import API_BASE_URL from "./api";

export async function searchSemantic(query) {

    try {

        const response = await fetch(
            `${API_BASE_URL}/retrieval/search?query=${query}`
        );

        if (!response.ok) {
            throw new Error("Retrieval request failed");
        }

        return await response.json();

    } catch (error) {

        console.error(
            "Semantic retrieval error:",
            error
        );

        return null;
    }
}