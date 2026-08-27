const messageInput = document.getElementById("message");
const sendButton = document.getElementById("send-button");
const responseBox = document.getElementById("response");


sendButton.addEventListener("click", async () => {
    const message = messageInput.value.trim();

    if (!message) {
        responseBox.textContent = "Please enter a request.";
        return;
    }

    responseBox.textContent = "Processing...";

    try {
        const response = await fetch("/agent/message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message: message,
            }),
        });

        const data = await response.json();

        renderResponse(data);

    } catch (error) {
        responseBox.textContent =
            `Request failed: ${error.message}`;
    }
});


function renderResponse(data) {

    if (data.type === "policy_answer") {

        const renderedMarkdown = marked.parse(data.answer);

        const safeHtml = DOMPurify.sanitize(
            renderedMarkdown
        );

        responseBox.innerHTML = `
            <div class="result-row">
                <span class="label">Type:</span>
                <span class="value">Policy Answer</span>
            </div>

            <div class="status-message success-status">
                ✓ Completed successfully
            </div>

            <div class="answer">
                ${safeHtml}
            </div>
        `;

        return;
    }


    if (data.type === "tool_result") {

        if (data.error) {
            result = `
                <div class="error-detail">
                    <span class="detail-label">Reason</span>
                    <span class="detail-value">${data.error}</span>
                </div>
            `;
        } else if (data.result) {
            result = Object.entries(data.result)
                .map(([key, value]) => `
                    <div class="detail-row">
                        <span class="detail-label">
                            ${formatLabel(key)}
                        </span>

                        <span class="detail-value">
                            ${value}
                        </span>
                    </div>
                `)
                .join("");
        } else {
            result = `
                <div class="detail-empty">
                    No result returned.
                </div>
            `;
        }

        const status = data.error
            ? `
                <div class="status-message error-status">
                    ✕ Request failed
                </div>
            `
            : `
                <div class="status-message success-status">
                    ✓ Completed successfully
                </div>
            `;

        responseBox.innerHTML = `
            <div class="result-row">
                <span class="label">Type:</span>
                <span class="value">Tool Result</span>
            </div>

            <div class="result-row">
                <span class="label">Tool:</span>
                <span class="value">${data.tool}</span>
            </div>

            ${status}

            <div class="result-data">
                ${result}
            </div>
        `;

        return;
    }


    responseBox.textContent = JSON.stringify(
        data,
        null,
        2
    );
}

function formatLabel(key) {
    return key
        .replaceAll("_", " ")
        .replace(/\b\w/g, char => char.toUpperCase())
        .replace(/\bId\b/g, "ID");
}