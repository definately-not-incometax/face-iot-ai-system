const socket = io("http://192.168.0.197:5000");

const logsDiv = document.getElementById("logs");
const status = document.getElementById("status");

socket.on("connect", () => {
    status.innerText = "🟢 Connected to server";
});

socket.on("disconnect", () => {
    status.innerText = "🔴 Disconnected";
});

socket.on("new_event", (data) => {
    const div = document.createElement("div");
    div.className = "event";

    div.innerHTML = `
        <strong>${data.name}</strong><br/>
        Time: ${new Date().toLocaleTimeString()}
    `;

    logsDiv.prepend(div);
});