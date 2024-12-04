document.getElementById("create-room").addEventListener("click", () => {
    fetch("/create_room", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            alert(`Room created! ID: ${data.room_id}`);
        });
});

document.getElementById("join-room").addEventListener("click", () => {
    const roomId = document.getElementById("room-id").value;
    fetch("/join_room", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ room_id: roomId })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                alert("Joined room!");
                loadMessages(roomId);
            } else {
                alert(data.message);
            }
        });
});

document.getElementById("send").addEventListener("click", () => {
    const roomId = document.getElementById("room-id").value;
    const message = document.getElementById("message").value;
    const username = document.getElementById("username").value;

    fetch("/send_message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ room_id: roomId, username, message })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                loadMessages(roomId);
            } else {
                alert(data.message);
            }
        });
});

function loadMessages(roomId) {
    fetch("/get_messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ room_id: roomId })
    })
        .then(response => response.json())
        .then(data => {
            const messagesDiv = document.getElementById("messages");
            if (data.messages) {
                messagesDiv.innerHTML = data.messages.map(msg => `<p>${msg}</p>`).join("");
            } else {
                alert(data.message);
            }
        });
}
