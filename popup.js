
document.getElementById("checkButton").addEventListener("click", async () => {
    const url = document.getElementById("urlInput").value.trim();
    const result = document.getElementById("result");

    if (!url) {
        result.textContent = "Please enter a URL";
        return;
    }

    result.textContent = "Checking...";
    result.className = "";

    try {
        const response = await fetch("http://127.0.0.1:5000/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Request failed");
        }

        result.textContent = data.result;
        result.className = data.result.toLowerCase();

    } catch (error) {
        result.textContent = "Backend connection failed";
        result.className = "scam";
    }
});
