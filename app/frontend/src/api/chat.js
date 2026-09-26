const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "";


export async function sendMessage(
  question,
  k = 5
) {

  const response = await fetch(
    `${API_BASE_URL}/api/v1/chat`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({
        question,
        k
      })
    }
  );


  if (!response.ok) {

    let detail = "";

    try {
      const error = await response.json();

      detail =
        error.detail ||
        JSON.stringify(error);

    } catch {
      detail = await response.text();
    }

    throw new Error(
      detail ||
      `Request failed: ${response.status}`
    );
  }


  return response.json();
}