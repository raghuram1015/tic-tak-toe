document.addEventListener("DOMContentLoaded", () => {
  // Game state
  let currentPlayer = "X"
  let board = ["", "", "", "", "", "", "", "", ""]
  let gameActive = true

  // DOM elements
  const cells = document.querySelectorAll(".cell")
  const statusDisplay = document.getElementById("status")
  const resetButton = document.getElementById("reset-button")

  // Win patterns (same as in Python code)
  const winPatterns = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8], // Rows
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8], // Columns
    [0, 4, 8],
    [2, 4, 6], // Diagonals
  ]

  // Initialize game
  function initGame() {
    cells.forEach((cell) => {
      cell.addEventListener("click", () => cellClick(cell))
    })

    resetButton.addEventListener("click", resetGame)
    updateStatus()
  }

  // Handle cell click
  function cellClick(cell) {
    const index = Number.parseInt(cell.getAttribute("data-index"))

    if (board[index] !== "" || !gameActive) {
      return
    }

    // Update board state
    board[index] = currentPlayer
    cell.textContent = currentPlayer
    cell.classList.add(currentPlayer.toLowerCase())

    // Check for win or draw
    if (checkWinner()) {
      gameActive = false
      statusDisplay.textContent = `Player ${currentPlayer} wins!`
      highlightWinningCells()
      return
    }

    if (isDraw()) {
      gameActive = false
      statusDisplay.textContent = "It's a draw!"
      return
    }

    // Switch player
    currentPlayer = currentPlayer === "X" ? "O" : "X"
    updateStatus()
  }

  // Check for winner
  function checkWinner() {
    return winPatterns.some((pattern) => {
      const [a, b, c] = pattern
      return board[a] !== "" && board[a] === board[b] && board[a] === board[c]
    })
  }

  // Find winning pattern
  function getWinningPattern() {
    for (const pattern of winPatterns) {
      const [a, b, c] = pattern
      if (board[a] !== "" && board[a] === board[b] && board[a] === board[c]) {
        return pattern
      }
    }
    return null
  }

  // Highlight winning cells
  function highlightWinningCells() {
    const winningPattern = getWinningPattern()
    if (winningPattern) {
      winningPattern.forEach((index) => {
        cells[index].style.backgroundColor = "#c8e6c9"
      })
    }
  }

  // Check for draw
  function isDraw() {
    return !board.includes("")
  }

  // Update status display
  function updateStatus() {
    statusDisplay.textContent = `Player ${currentPlayer}'s turn`
  }

  // Reset game
  function resetGame() {
    currentPlayer = "X"
    board = ["", "", "", "", "", "", "", "", ""]
    gameActive = true

    cells.forEach((cell) => {
      cell.textContent = ""
      cell.classList.remove("x", "o")
      cell.style.backgroundColor = ""
    })

    updateStatus()
  }

  // Python backend communication
  async function sendMoveToBackend(index) {
    try {
      const response = await fetch("/move", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ index, player: currentPlayer }),
      })

      if (response.ok) {
        const data = await response.json()
        return data
      }
    } catch (error) {
      console.error("Error communicating with backend:", error)
    }
    return null
  }

  // Initialize the game
  initGame()
})
