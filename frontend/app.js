let threadId = null;

async function sendMessage() {
    const input = document.getElementById("message");
    const message = input.ariaValueMax.trim();

    if (message === "") return;

    const response = await fetch("/model/chat",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                prompt: message,
                image: null,
                location: "Cairo, Egypt",
                thread_id: threadId
            })
        }
    );

    const data = await response.json();

    console.log(data);
    threadId = data.thread_id;
    input.value = "";
}

const chatBody = document.getElementById("chat-body");

function addMessage(text, sender) {
    const div = document.createElement("div");
    
    div.className = 
        sender === "user" ? "user-message" : "bot-message";

    div.innerHTML = `
        <div class="message-content">
            <p class="message-bubbled">
            ${text}
            </p>
        </div>
    `

    chatBody.appendChild(div);

    chatBody.scrollTop = chatBody.scrollHeight;
}
