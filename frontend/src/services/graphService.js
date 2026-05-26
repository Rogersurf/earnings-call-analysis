const API_URL =
  "http://127.0.0.1:8000";

export async function fetchGraph(query) {

  try {

    const response = await fetch(

      `${API_URL}/graph/propagation?query=${encodeURIComponent(query)}`

    );

    return await response.json();

  } catch (error) {

    console.error(
      "Graph fetch error:",
      error
    );

    return null;
  }
}