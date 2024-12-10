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
        self.decks_remaining = max(1, len(self.deck) / 52)  # Ensure at least 1 deck remains
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

    def simulate_outcome(self, player_hand, dealer_hand, action="stand"):
        """Simulate the outcome of a game for a given action (stand or hit)."""
        # Calculate player's hand value
        player_value = self.calculate_hand_value(player_hand)
        if action == "hit":
            # Simulate hitting by adding a card to the player's hand
            if self.deck:
                new_card = self.deck[-1]  # Peek at the next card
                player_hand.append(new_card)
                player_value = self.calculate_hand_value(player_hand)

        if player_value > 21:
            return "lose"  # Player busts

        # Simulate dealer's turn
        dealer_value = self.calculate_hand_value(dealer_hand)
        while dealer_value < 17:
            if self.deck:
                new_card = self.deck.pop()
                dealer_hand.append(new_card)
                dealer_value = self.calculate_hand_value(dealer_hand)

        # Determine the outcome
        if dealer_value > 21 or player_value > dealer_value:
            return "win"
        elif dealer_value == player_value:
            return "tie"
        else:
            return "lose"

    def simulate_many_outcomes(self, player_hand, dealer_hand, simulations=1000, action="stand"):
        """Simulate multiple outcomes and return win, loss, and tie counts."""
        win_count = 0
        tie_count = 0
        loss_count = 0

        for _ in range(simulations):
            # Clone hands and shuffle deck to maintain integrity of the actual game state
            simulated_deck = self.deck[:]
            simulated_player_hand = player_hand[:]
            simulated_dealer_hand = dealer_hand[:]
            random.shuffle(simulated_deck)

            # Simulate the outcome
            if action == "hit":
                if simulated_deck:
                    new_card = simulated_deck.pop()
                    simulated_player_hand.append(new_card)

            player_value = self.calculate_hand_value(simulated_player_hand)
            if player_value > 21:
                loss_count += 1
                continue

            dealer_value = self.calculate_hand_value(simulated_dealer_hand)
            while dealer_value < 17 and simulated_deck:
                new_card = simulated_deck.pop()
                simulated_dealer_hand.append(new_card)
                dealer_value = self.calculate_hand_value(simulated_dealer_hand)

            if dealer_value > 21 or player_value > dealer_value:
                win_count += 1
            elif player_value == dealer_value:
                tie_count += 1
            else:
                loss_count += 1

        return win_count, loss_count, tie_count
