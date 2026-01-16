const socket = new WebSocket("ws://localhost:8001");

socket.addEventListener("open", (event) => {
  console.log("Połączono z serwerem!");
  document.getElementById("status").innerText = "Połączono!";
  document.getElementById("status").style.color = "green";

  socket.send(JSON.stringify({ action: "HELLO", msg: "Cześć serwerze!" }));
});

socket.addEventListener("message", (event) => {
  console.log("Wiadomość z serwera:", event.data);
});

const layout = [
  "JAGODA....",
  ".....E....",
  ".EEEEE....",
  ".....C.L..",
  "AAAAAASS..",
  ".....R.C..",
  ".AAAAAAAA",
  ".....E....",
  ".MUTEX....",
  "..........",
];

document.addEventListener("DOMContentLoaded", () => {
  const boardDiv = document.getElementById("board");

  for (let r = 0; r < 10; r++) {
    for (let c = 0; c < 10; c++) {
      const input = document.createElement("input");

      input.id = `cell-${r}-${c}`;

      input.maxLength = 1;

      if (layout[r][c] === ".") {
        input.className = "black-cell";
        input.disabled = true;
      }

      boardDiv.appendChild(input);
    }
  }
});
