import random


class Property:
    def __init__(self, position, cost=random.randrange(150), rent=random.randrange(50), owner=None):
        self.position = position
        self.cost = cost
        self.rent = rent
        self.owner = owner

        
    def update_owner(self, owner):
        self.owner = owner


class Player:
    def __init__(self, profile):
        self.profile = profile
        self.money = 300
        self.position = 0
        self.properties = []

        
    def receive_rent(self, rent):
        self.money += rent

        
    def buy_property(self, property, board_game):
        self.money -= property.cost
        self.properties.append(property.position)
        board_game[property.position].update_owner(owner=self.profile)

        
    def roll_dice(self):
        self.position += random.randrange(1, 7)
        if self.position >= 20:
            self.position -= 20
            self.money += 100


    def play(self, board_game, players):
        if self.money >= 0:
            self.roll_dice()
            property = board_game[self.position]

            if property.owner:
                self.money -= property.rent
                if property.owner == players[0].profile:
                    players[0].receive_rent(property.rent)
                elif property.owner == players[1].profile:
                    players[1].receive_rent(property.rent)
                elif property.owner == players[2].profile:
                    players[2].receive_rent(property.rent)
                elif property.owner == players[3].profile:
                    players[3].receive_rent(property.rent)

                # Checar se ele perdeu o jogo
                if self.money <= 0:
                    for position in self.properties:
                        board_game[position].update_owner(owner=None)
                        self.properties = []

            else:
                if self.profile == 'impulsive':
                    if self.money >= property.cost and property.position not in self.properties:
                        self.buy_property(property=property, board_game=board_game)

                elif self.profile == 'demanding':
                    if self.money >= property.cost and property.position not in self.properties \
                            and property.rent > 50:
                        self.buy_property(property=property, board_game=board_game)

                elif self.profile == 'cautious':
                    reserve = self.money - property.cost
                    if self.money >= property.cost and property.position not in self.properties \
                            and reserve >= 80:
                        self.buy_property(property=property, board_game=board_game)

                elif self.profile == 'random':
                    if self.money >= property.cost and property.position not in self.properties \
                            and random.random() < .5:
                        self.buy_property(property=property, board_game=board_game)
