from __future__ import annotations
from enum import Enum
from copy import deepcopy
import random
"""
    Structura enum pentru jucatori folosita pentru a specifica randul jucatorului in functia minimax, 
    dar si pentru a specifica ce simbol sa puna pe tabla in functie de jucator
"""
class Player(Enum):
    MAX = 1
    MIN = 2

"""
    Clasa care reprezinta starea jocului, adica tabla de joc. 
    Ea contine o matrice 3x3 care reprezinta tabla de joc.
"""
class State:
    def __init__(self, board: list[list[str]]) -> None:
        self.board = board
    
    # Functie care primeste o pozitie pe tabla si un simbol, 
    # si returneaza o noua stare a jocului cu simbolul pus pe acea pozitie
    def apply_move(self, row: int, col: int, elem: str) -> State:
        if self.board[row][col] == ' ':
            new_board = [r[:] for r in self.board]
            new_board[row][col] = elem
            return State(new_board)
            
    def get_next_states(self, player: Player) -> list[State]:
        next_states = []
        symbol = 'X' if player == Player.MAX else '0'

        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    next_states.append(self.apply_move(row, col, symbol))
        
        return next_states

    @staticmethod
    def generate_initial_state() -> State:
        return State([[' ' for _ in range(3)] for _ in range(3)])
    

    @staticmethod
    def generate_random_state() -> State:
        board = [[' ' for _ in range(3)] for _ in range(3)]

        elems_on_board = random.randint(0,4) * 2
        while elems_on_board:
            elems_on_board -= 1
            while True:
                row = random.randint(0, 2)
                col = random.randint(0, 2)
                
                if board[row][col] != ' ':
                    continue
                
                if elems_on_board % 2 == 0:
                    board[row][col] = '0'
                else:
                    board[row][col] = 'X'
                break

        return State(board)
    
    def get_winner(self) -> str | None:
        # verifica liniile
        for row in self.board:
            if row[0] != ' ' and row[0] == row[1] == row[2]:
                return row[0]
        
        # verifica coloanele
        for col in range(3):
            if self.board[0][col] != ' ' and self.board[0][col] == self.board[1][col] == self.board[2][col]:
                return self.board[0][col]
        
        # verifica diagonalele
        if self.board[0][0] != ' ' and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0]
        if self.board[0][2] != ' ' and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[0][2]
        
        return None
    
    def is_final(self) -> bool:
        if self.get_winner() is not None:
            return True
        return all(cell != ' ' for row in self.board for cell in row)
        
    
    def __str__ (self) -> str:
        return '\n'.join([' | '.join(row) for row in self.board])

    def score(self, depth) -> int:
        winner = self.get_winner()
        if winner == 'X': return 100 + depth
        if winner == '0': return -100 - depth
        return 0
    
class MinimaxAgent:
    def __init__(self, max_depth: int) -> None:
        self.max_depth = max_depth

    def minimax(self, state: State, depth: int, player: Enum):
        if state.is_final() or depth == 0:
            return state.score(depth), None
        
        if player == Player.MAX:
            best_score = float('-inf')
            best_next_state = None

            for next_state in state.get_next_states(Player.MAX):
                score, _ = self.minimax(next_state, depth - 1, Player.MIN)
                if score > best_score:
                    best_score = score
                    best_next_state = next_state
            return best_score, best_next_state
        else:
            best_score = float('inf')
            best_next_state = None

            for next_state in state.get_next_states(Player.MIN):
                score, _ = self.minimax(next_state, depth - 1, Player.MAX)
                if score < best_score:
                    best_score = score
                    best_next_state = next_state
            return best_score, best_next_state

if __name__ == "__main__":
    initial_state = State.generate_random_state()
    print(initial_state)
    
    agent = MinimaxAgent(9)
    score, next_move = agent.minimax(initial_state, agent.max_depth, Player.MAX)
    
    print(score)
    print(next_move)