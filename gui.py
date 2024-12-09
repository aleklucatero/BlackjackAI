import tkinter as tk
from PIL import Image, ImageTk
from game_logic import BlackjackGame

class BlackjackGUI:
    def __init__(self):
        self.game = BlackjackGame()
        self.root = tk.Tk()
        self.root.title("Blackjack AI")

        # Game state
        self.chips = 1000  # Initial chips
        self.bet = 100     # Initial bet
        self.game_over = False
        self.bet_locked = False  # Indicates whether the bet is locked

        # Load card images
        self.card_images = self.load_card_images()

        # Create UI elements
        self.create_widgets()

        # Start the game
        self.root.mainloop()

    def load_card_images(self):
        """Load card images from the assets folder."""
        images = {}
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        for suit in suits:
            for rank in ranks:
                filename = f"assets/{rank}_of_{suit}.png"
                images[f"{rank}_of_{suit}"] = ImageTk.PhotoImage(Image.open(filename).resize((100, 150)))
        images["back"] = ImageTk.PhotoImage(Image.open("assets/blue.png").resize((100, 150)))
        images["chip"] = ImageTk.PhotoImage(Image.open("assets/chip.png").resize((50, 50)))
        return images

    def create_widgets(self):
        """Create GUI widgets."""
        # Dealer Section
        self.dealer_title = tk.Label(self.root, text="Dealer's Hand", font=("Arial", 14))
        self.dealer_title.pack(pady=5)
        self.dealer_frame = tk.Frame(self.root)
        self.dealer_frame.pack()
        self.dealer_canvas = tk.Canvas(self.dealer_frame, width=500, height=200, bg="green")
        self.dealer_canvas.pack()
        self.dealer_value_label = tk.Label(self.root, text="Dealer's Value: ?", font=("Arial", 12))
        self.dealer_value_label.pack()

        # Player Section
        self.player_title = tk.Label(self.root, text="Player's Hand", font=("Arial", 14))
        self.player_title.pack(pady=5)
        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack()
        self.player_canvas = tk.Canvas(self.player_frame, width=500, height=200, bg="green")
        self.player_canvas.pack()
        self.player_value_label = tk.Label(self.root, text="Player's Value: ?", font=("Arial", 12))
        self.player_value_label.pack()

        # Chips Display with Image
        self.chips_frame = tk.Frame(self.root)
        self.chips_frame.pack(pady=10)
        self.chip_image_label = tk.Label(self.chips_frame, image=self.card_images["chip"])
        self.chip_image_label.pack(side="left")
        self.chips_label = tk.Label(self.chips_frame, text=f"{self.chips}", font=("Arial", 14), fg="blue")
        self.chips_label.pack(side="left", padx=10)

        # Bet Adjustment Section
        self.bet_frame = tk.Frame(self.root)
        self.bet_frame.pack(pady=10)
        tk.Label(self.bet_frame, text="Bet Amount:", font=("Arial", 12)).pack(side="left")
        self.bet_label = tk.Label(self.bet_frame, text=f"{self.bet}", font=("Arial", 12), fg="green")
        self.bet_label.pack(side="left", padx=5)
        self.decrease_bet_button = tk.Button(self.bet_frame, text="-", command=self.decrease_bet)
        self.decrease_bet_button.pack(side="left", padx=5)
        self.increase_bet_button = tk.Button(self.bet_frame, text="+", command=self.increase_bet)
        self.increase_bet_button.pack(side="left", padx=5)

        # Controls
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(pady=20)
        self.status_label = tk.Label(self.controls_frame, text="", font=("Arial", 14))
        self.status_label.pack()
        self.deal_button = tk.Button(self.controls_frame, text="Deal", command=self.deal_hand)
        self.deal_button.pack(side="left", padx=10)
        self.hit_button = tk.Button(self.controls_frame, text="Hit", command=self.hit, state=tk.DISABLED)
        self.hit_button.pack(side="left", padx=10)
        self.stand_button = tk.Button(self.controls_frame, text="Stand", command=self.stand, state=tk.DISABLED)
        self.stand_button.pack(side="left", padx=10)
        self.reset_button = tk.Button(self.controls_frame, text="Reset Game", command=self.reset_game)
        self.reset_button.pack(side="left", padx=10)

    def decrease_bet(self):
        """Decrease the bet amount."""
        if not self.bet_locked and self.bet > 100:
            self.bet -= 100
            self.bet_label.config(text=f"{self.bet}")

    def increase_bet(self):
        """Increase the bet amount."""
        if not self.bet_locked and self.bet + 100 <= self.chips:
            self.bet += 100
            self.bet_label.config(text=f"{self.bet}")

    def deal_hand(self):
        """Start a new round and lock the bet."""
        if self.chips < self.bet:
            self.status_label.config(text="Not enough chips to play!", fg="red")
            return

        self.chips -= self.bet  # Deduct bet
        self.bet_locked = True  # Lock the bet
        self.decrease_bet_button.config(state=tk.DISABLED)
        self.increase_bet_button.config(state=tk.DISABLED)
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.status_label.config(text="", fg="black")

        # Reset and deal cards
        self.game.reset_game()
        self.game.deal_card(self.game.player_hand)  # Player gets one card
        self.game.deal_card(self.game.dealer_hand)  # Dealer shows one card
        self.game.deal_card(self.game.dealer_hand)  # Dealer keeps one card hidden
        self.game_over = False
        self.update_ui()

    def hit(self):
        """Player takes a card."""
        if not self.game_over:
            self.game.deal_card(self.game.player_hand)
            if self.game.calculate_hand_value(self.game.player_hand) > 21:
                self.game_over = True
                self.status_label.config(text="Bust! Dealer Wins!", fg="red")
            self.update_ui()

    def stand(self):
        """End the player's turn and start the dealer's turn."""
        if not self.game_over:
            # Reveal dealer's hidden card
            self.update_ui(reveal_dealer=True)

            # Dealer plays
            while self.game.calculate_hand_value(self.game.dealer_hand) < 17:
                self.game.deal_card(self.game.dealer_hand)

            # Determine the outcome
            player_total = self.game.calculate_hand_value(self.game.player_hand)
            dealer_total = self.game.calculate_hand_value(self.game.dealer_hand)
            if dealer_total > 21 or player_total > dealer_total:
                self.chips += self.bet * 2  # Win double the bet
                self.status_label.config(text="You Win!", fg="green")
            elif dealer_total == player_total:
                self.chips += self.bet  # Refund bet
                self.status_label.config(text="It's a Tie!", fg="blue")
            else:
                self.status_label.config(text="Dealer Wins!", fg="red")
            self.game_over = True
            self.reset_controls()
            self.update_ui(reveal_dealer=True)

    def reset_controls(self):
        """Reset the controls for a new round."""
        self.bet_locked = False
        self.decrease_bet_button.config(state=tk.NORMAL)
        self.increase_bet_button.config(state=tk.NORMAL)
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)

    def reset_game(self):
        """Reset the game completely."""
        self.chips = 1000
        self.bet = 100
        self.game.reset_game()
        self.game_over = False
        self.bet_locked = False
        self.status_label.config(text="", fg="black")
        self.update_ui()
        self.reset_controls()

    def update_ui(self, reveal_dealer=False):
        """Update the GUI with the current game state."""
        # Clear canvases
        self.dealer_canvas.delete("all")
        self.player_canvas.delete("all")

        # Display dealer's cards
        for i, card in enumerate(self.game.dealer_hand):
            if i == 0 or reveal_dealer:  # Show the first card or reveal all cards
                card_name = f"{card['rank'].lower()}_of_{card['suit'].lower()}"
                card_image = self.card_images.get(card_name, self.card_images["back"])
            else:
                card_image = self.card_images["back"]  # Face-down card for unrevealed state
            self.dealer_canvas.create_image(20 + i * 120, 50, anchor=tk.NW, image=card_image)

        # Display player's cards
        for i, card in enumerate(self.game.player_hand):
            card_name = f"{card['rank'].lower()}_of_{card['suit'].lower()}"
            card_image = self.card_images.get(card_name, self.card_images["back"])
            self.player_canvas.create_image(20 + i * 120, 50, anchor=tk.NW, image=card_image)

        # Update card values
        dealer_value = self.game.calculate_hand_value(self.game.dealer_hand)
        player_value = self.game.calculate_hand_value(self.game.player_hand)
        self.dealer_value_label.config(text=f"Dealer's Value: {dealer_value if reveal_dealer else '?'}")
        self.player_value_label.config(text=f"Player's Value: {player_value}")

        # Update chips and bet
        self.chips_label.config(text=f"{self.chips}")
        self.bet_label.config(text=f"{self.bet}")

if __name__ == "__main__":
    BlackjackGUI()
