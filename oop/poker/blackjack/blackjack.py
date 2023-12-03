import random
from enum import Enum
from abc import ABC, abstractmethod


class Poker_game(Enum):
    BLACKJACK = 1


class PokerDeck:
    def __init__(self, num=1) -> None:
        self.cards = self.create_deck(num)
        self.shuffle_deck()

    def create_deck(self, num):
        cards = []
        for _ in range(0, num):
            cards += self.init_deck()
        return cards

    def init_deck(self):
        # suits = ["Heart", "Diamond", "Club", "Spade"]
        ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        return ranks

    def shuffle_deck(self):
        random.shuffle(self.cards)


class DealerBase(ABC):
    def __init__(self, deck: PokerDeck, game_name: str) -> None:
        self.__deck = deck
        self.__game_name = game_name

    def deal_card(self):
        if not self.__deck:
            print("Card Deck is empty")
            return None
        return self.__deck.cards.pop()

    @property
    def game(self):
        return self.__game_name

    @abstractmethod
    def poker_game():
        pass


class BlackjackDealer(DealerBase):
    def __init__(self, deck, game_name) -> None:
        super().__init__(deck, game_name)
        self.__game_name = game_name
        self.__banker = []
        self.__gamer = []

    def poker_game(self):
        self.__banker.append(self.deal_card())
        self.__gamer.append(self.deal_card())
        self.__gamer.append(self.deal_card())
        print(f"banker's card: [{self.__banker[0]}, X]")
        print(
            f"Your card: {self.__gamer}, Total points: {self.__calculate(self.__gamer)}"
        )
        while True:
            i = input("Do you want to hit (Y/n): ").lower()
            if i == "y":
                print("hit!")
                self.__hit(self.__gamer)
                print(
                    f"Your card: {self.__gamer}, Total points: {self.__calculate(self.__gamer)}"
                )
                if self.__bust(self.__gamer) == True:
                    print("Bust!")
                    break
            if i == "n":
                print("stand")
                self.__dealer_round()
                if self.__bust(self.__banker) == True:
                    print("Bust!")
                    print("You win!")
                    break
                else:
                    if sum(self.__gamer) > sum(self.__banker):
                        print("You win!")
                    elif sum(self.__gamer) < sum(self.__banker):
                        print("You lose!")
                    else:
                        print("Draw")
                    break
            else:
                print("please enter Y/n.")

    def __hit(self, deck: list):
        deck.append(self.deal_card())
        self.__bust(deck)

    def __calculate(self, deck: list):
        m_deck = [10 if v in [11, 12, 13] else v for v in deck]
        return sum(m_deck)

    def __bust(self, deck: list):
        sum = self.__calculate(deck)
        if sum > 21:
            return True

    def __dealer_round(self):
        sum = self.__calculate(self.__banker)
        while sum < 17:
            self.__hit(self.__banker)
            print(f"banker's card: {self.__banker}")
            sum = self.__calculate(self.__banker)


class Poker:
    @staticmethod
    def start_game(game_name):
        if game_name.upper() in [game.name for game in Poker_game]:
            print(f"Welcome! Let's play {game_name}!")
            deck = PokerDeck(2)
            return BlackjackDealer(deck, game_name)
        else:
            print("please enter correct game name.")


if __name__ == "__main__":
    dealer = Poker.start_game("blackjack")
    dealer.poker_game()