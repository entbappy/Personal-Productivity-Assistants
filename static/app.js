async function askAssistant() {
    let query = document.getElementById("query").value;
    let responseDiv = document.getElementById("response");

    if (!query.trim()) {
        responseDiv.innerHTML = "<p>Please enter a question.</p>";
        return;
    }

    responseDiv.innerHTML = "<p>Thinking...</p>";

    let response = await fetch("/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query })
    });

    let result = await response.json();
    responseDiv.innerHTML = `<p>${result.response}</p>`;
}
