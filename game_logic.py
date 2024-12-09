import random

class BlackjackGame:
    def __init__(self):
        self.deck = self._create_deck()
        self.shuffle_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.running_count = 0
        self.true_count = 0
        self.decks_remaining = 1  # Adjust based on number of decks

    def _create_deck(self):
        """Create a standard 52-card deck."""
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        return [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]

    def shuffle_deck(self):
        """Shuffle the deck."""
        random.shuffle(self.deck)

    def deal_card(self, hand):
        """Deal a card to a hand."""
        if self.deck:
            card = self.deck.pop()
            hand.append(card)
            self.update_count(card)

    def update_count(self, card):
        """Update the running count based on the Hi-Lo system."""
        rank = card['rank']
        if rank in ['2', '3', '4', '5', '6']:
            self.running_count += 1
        elif rank in ['10', 'Jack', 'Queen', 'King', 'Ace']:
            self.running_count -= 1

        # Update true count
        self.decks_remaining = max(1, len(self.deck) // 52)
        self.true_count = self.running_count / self.decks_remaining

    def calculate_hand_value(self, hand):
        """Calculate the total value of a hand."""
        value = 0
        aces = 0
        for card in hand:
            rank = card['rank']
            if rank in ['Jack', 'Queen', 'King']:
                value += 10
            elif rank == 'Ace':
                aces += 1
                value += 11
            else:
                value += int(rank)

        # Adjust for aces if value exceeds 21
        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value

    def reset_game(self):
        """Reset the game for a new round."""
        self.deck = self._create_deck()
        self.shuffle_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.running_count = 0
        self.true_count = 0
