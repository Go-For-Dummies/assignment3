#!/usr/local/bin/python3
#/usr/bin/python3
# Set the path to your python3 above
from pathlib import Path

from gtp_connection import GtpConnection
from board_util import GoBoardUtil
from simple_board import SimpleGoBoard
from simulation import SimUtil
from weighting import WeightUtil
from ucb import run_ucb
from rr import round_robin

# Move Selection Policies ###
ROUND_ROBIN = 'rr'
UCB = 'ucb'

MOVE_POLICIES = {
    ROUND_ROBIN, UCB
}
#############################
# Simulation Policies #######
RANDOM = 'random'
PATTERN = 'pattern'

SIMULATION_POLICIES = {
    RANDOM, PATTERN
}
#############################


class Nogo():

    def __init__(self, move_selection='rr', simulation_policy='random'):
        """
        NoGo player that selects moves randomly 
        from the set of legal moves.
        Passe/resigns only at the end of game.

        """
        self.name = "NoGoAssignment3"
        self.version = 1.0
        self.weight_util = WeightUtil(Path('weights'))
        self._move_selection = move_selection
        self._simulation_policy = simulation_policy
        self.n_sim = 10

    @property
    def move_selection(self): 
        return self._move_selection

    @property
    def simulation_policy(self): 
        return self._simulation_policy

    @move_selection.setter
    def move_selection(self, move_selection):
        if move_selection not in MOVE_POLICIES:
            raise AttributeError(
                f'move selection method not implemented: {move_selection}')
        self._move_selection = move_selection

    @simulation_policy.setter
    def simulation_policy(self, simulation_policy):
        if simulation_policy not in SIMULATION_POLICIES:
            raise AttributeError(
                f'simulation policy method not implemented: {simulation_policy}')
        self._simulation_policy = simulation_policy
    
    def get_move(self, board, color):
        """
        Run one-ply MC simulations to get a move to play.
        """
        cboard = board.copy()
        emptyPoints = board.get_empty_points()
        moves = GoBoardUtil.generate_legal_moves(cboard, color)
        if not moves:
            return None
        moves.append(None)
        best = None
        if self.move_selection == UCB:
            C = 0.4  # sqrt(2) is safe, this is more aggressive
            best = run_ucb(self, cboard, C, moves, color)
        elif self.move_selection == ROUND_ROBIN:
            best = round_robin(self, cboard, moves, color)
        return best

    def simulate(self, board, move, color):
        cboard = board.copy()
        cboard.play_move(move, color)
        if self.simulation_policy == RANDOM: 
            result = SimUtil.randomSimulation(cboard)
        elif self.simulation_policy == PATTERN: 
            result = SimUtil.probabilitySimulation(cboard, self.weight_util)
        return result


def run():
    """
    start the gtp connection and wait for commands.
    """
    board = SimpleGoBoard(7)
    con = GtpConnection(Nogo(), board)
    con.start_connection()


if __name__ == '__main__':
    run()
