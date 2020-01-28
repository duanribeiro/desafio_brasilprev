# -*- coding: utf-8 -*-
import json
from bson.json_util import dumps
from flask_restplus import Resource, Namespace
from app.game.models import Player, Property
import pandas as pd

api = Namespace('game', 'Game Endpoint')

@api.route('/')
class Game(Resource):
    @api.doc(responses={
        200: 'Success',
        400: 'Bad Request',
        422: 'Unprocessable Entity',
    })
    def get(self):
        """
        Main logic of the game
        """
        final_output = []
        PROFILES = ['impulsive', 'demanding', 'cautious', 'random']
        SIMULATION_TIMES = 301
        ROUNDS = 1001
        SIZE_BOARDGAME = 20

        for simulation in range(1, SIMULATION_TIMES):
            players = [Player(profile=profile) for profile in PROFILES]
            board_game = [Property(position=i) for i in range(SIZE_BOARDGAME)]

            for round in range(1, ROUNDS):
                players[0].play(board_game=board_game, players=players)
                players[1].play(board_game=board_game, players=players)
                players[2].play(board_game=board_game, players=players)
                players[3].play(board_game=board_game, players=players)

                is_game_over = [player.profile for player in players if player.money < 0]
                if len(is_game_over) > 2:
                    winner = [profile for profile in PROFILES if profile not in is_game_over]

                    final_output.append({
                        'simulation': simulation,
                        'round': round,
                        'how_game_end': 'Normal Victory',
                        'winner': winner[0]
                    })
                    break

            if round == ROUNDS - 1:
                if players[0].money > players[1].money and  \
                    players[0].money > players[2].money and \
                    players[0].money > players[3].money:
                    winner = players[0].profile
                if players[1].money > players[0].money and  \
                    players[1].money > players[2].money and \
                    players[1].money > players[3].money:
                    winner = players[1].profile
                if players[2].money > players[1].money and  \
                    players[2].money > players[0].money and \
                    players[2].money > players[3].money:
                    winner = players[2].profile
                else:
                    winner = players[3].profile

                final_output.append({
                    'simulation': simulation,
                    'round': round,
                    'how_game_end': 'Boring Victory',
                    'winner': winner
                })

        # Normalmente não uso o Pandas devido ao consumo excessivo de memória, mas ele facilita a manipulação dos dados.
        result = pd.DataFrame(final_output)
        timeout = len(result[result['how_game_end'] == 'Boring Victory'])
        mean_round = result['round'].mean()
        winners_profile = result['winner'].value_counts().to_dict()

        for key, value in winners_profile.items():
            winners_profile[key] = (value / SIMULATION_TIMES) * 100
        most_winner = result['winner'].value_counts().sort_values().index[-1]

        return {
            'Quantas partidas terminam por time out': timeout,
            'Quantos turnos em media demora uma partida': mean_round,
            'Qual a porcentagem de vitorias por comportamento dos jogadores': winners_profile,
            'Qual o comportamento que mais vence': most_winner
        }