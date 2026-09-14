const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const chatBox = document.getElementById("chat-box");


function addMessage(message, className) {

    const messageElement = document.createElement("div");

    messageElement.classList.add("message", className);

    messageElement.textContent = message;

    chatBox.appendChild(messageElement);

    chatBox.scrollTop = chatBox.scrollHeight;
}


async function sendMessage() {

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }


    // Show user's message
    addMessage(message, "user-message");

    // Clear input
    messageInput.value = "";


    try {

        const response = await fetch(
            "http://127.0.0.1:8000/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message
                })
            }
        );


        const data = await response.json();


        // Show Gemini's response
        addMessage(
            data.response,
            "bot-message"
        );


    } catch (error) {

        console.error(error);

        addMessage(
            "Something went wrong. Please try again.",
            "bot-message"
        );
    }
}


sendButton.addEventListener(
    "click",
    sendMessage
);


messageInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {
            sendMessage();
        }

    }
);