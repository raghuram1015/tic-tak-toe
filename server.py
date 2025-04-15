from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# Game state
current_player = 'X'
board = ["", "", "", "", "", "", "", "", ""]
game_active = True

# Function to check for a winner
def check_winner():
    global game_active
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]

    for pattern in win_patterns:
        a, b, c = pattern
        if board[a] and board[a] == board[b] and board[a] == board[c]:
            return {"winner": board[a]}

    if "" not in board:
        return {"draw": True}
    
    return {"ongoing": True}

# Function to reset the game
def reset_game():
    global board, game_active, current_player
    board = ["", "", "", "", "", "", "", "", ""]
    game_active = True
    current_player = 'X'
    return {"status": "reset"}

# Serve static files
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

# Handle moves
@app.route('/move', methods=['POST'])
def move():
    global current_player, board, game_active
    
    if not game_active:
        return jsonify({"error": "Game is not active"}), 400
    
    data = request.json
    index = data.get('index')
    player = data.get('player')
    
    if player != current_player:
        return jsonify({"error": "Not your turn"}), 400
    
    if not isinstance(index, int) or index < 0 or index > 8:
        return jsonify({"error": "Invalid index"}), 400
    
    if board[index] != "":
        return jsonify({"error": "Cell already taken"}), 400
    
    # Update board
    board[index] = current_player
    
    # Check for winner or draw
    result = check_winner()
    
    if "winner" in result or "draw" in result:
        game_active = False
    else:
        # Switch player
        current_player = 'O' if current_player == 'X' else 'X'
    
    return jsonify({
        "board": board,
        "currentPlayer": current_player,
        "gameActive": game_active,
        **result
    })

# Reset endpoint
@app.route('/reset', methods=['POST'])
def reset():
    return jsonify(reset_game())

if __name__ == '__main__':
    app.run(debug=True)
