from game_logic import BlackjackGame

if __name__ == "__main__":
    game = BlackjackGame()

    # Deal cards to player and dealer
    game.deal_card(game.player_hand)
    game.deal_card(game.dealer_hand)

    print("Player Hand:", game.player_hand)
    print("Dealer Hand:", game.dealer_hand)
    print("Player Hand Value:", game.calculate_hand_value(game.player_hand))
    print("Dealer Hand Value:", game.calculate_hand_value(game.dealer_hand))
    print("Running Count:", game.running_count)
    print("True Count:", game.true_count)
