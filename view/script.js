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
