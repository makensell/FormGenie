document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("formGenie");
  const statusMessage = document.getElementById("statusMessage");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formLink = document.getElementById("formLink").value.trim();
    const responseCount = parseInt(document.getElementById("responseCount").value);
    const speed = document.getElementById("speed").value;

    // ✅ Basic validation
    if (!formLink || !formLink.includes("https://docs.google.com/forms")) {
      statusMessage.textContent = "❌ Error: Please enter a valid Google Form link.";
      return;
    }

    // ✅ Show loading message
    statusMessage.textContent = "⏳ Connecting to FormGenie backend...";

    try {
      const response = await fetch("http://127.0.0.1:5000/fill-form", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          formLink,
          responseCount,
          speed
        })
      });

      const result = await response.json();

      if (response.ok) {
        statusMessage.innerHTML = ` ${result.message}`;
      } else {
        statusMessage.textContent = `❌ Error: ${result.message || "Something went wrong."}`;
      }

    } catch (error) {
      console.error("Fetch error:", error);
      statusMessage.textContent = "❌ Failed to connect to the backend. Is the server running?";
    }
  });
});
