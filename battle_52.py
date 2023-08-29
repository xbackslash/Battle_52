import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Initialize Pygame Mixer
pygame.mixer.init()

# Load the background music
background_music = pygame.mixer.Sound("Battle_52.mp3")
win_sound = pygame.mixer.Sound('Battle_52_Win.mp3')

# Set the volume (0.0 to 1.0, adjust as needed)
background_music.set_volume(0.25)
win_sound.set_volume(0.5)

# Play the background music on a loop
background_music.play(-1)

# Constants for the window size
WIDTH = 1280
HEIGHT = 720
square_size = 50
padding = 20
hp_padding = 20
hp_offset = 175

# Scale factor for graphics
SCALE_FACTOR = 2  # You can adjust this factor to scale the graphics as needed

# Constants for the scaled square size and other dimensions
scaled_square_size = 50 * SCALE_FACTOR
scaled_padding = 20 * SCALE_FACTOR
scaled_hp_padding = 20 * SCALE_FACTOR
scaled_hp_offset = 175 * SCALE_FACTOR

# Scale up the graphics by applying the SCALE_FACTOR
scaled_font_size = 24 * SCALE_FACTOR

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle 52")

# Colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (169, 169, 169)

# Define card attributes
class Card:
    def __init__(self, name, suit, value, face):
        self.name = name
        self.suit = suit
        self.value = value
        self.face = face
        self.width = 100
        self.height = 150
        self.x = 0
        self.y = 0

    def __str__(self):
        return f"{self.name} of {self.suit}"

    def draw(self, x=None, y=None):
        if x is not None and y is not None:
            self.x = x
            self.y = y

        # Draw the scaled white card rectangle
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

        # Draw the card value in the upper left corner
        font = pygame.font.Font(None, 24)
        value_text = font.render(str(self.name), True, BLACK)
        value_rect = value_text.get_rect(topleft=(self.x + 10, self.y + 10))
        screen.blit(value_text, value_rect)

        # Determine suit color
        suit_color = RED if self.suit in ["Hearts", "Diamonds"] else BLACK

        # Draw the suit in text just under the value
        suit_text = font.render(str(self.suit[0]), True, suit_color)
        suit_rect = suit_text.get_rect(topleft=(self.x + 10, self.y + 40))
        screen.blit(suit_text, suit_rect)

# Define the scaled Deck class
class Deck:
    def __init__(self):
        self.suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.card_values = [("Ace", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6), ("7", 7), ("8", 8), ("9", 9), ("10", 10), ("Jack", 11), ("Queen", 12), ("King", 13)]
        self.cards = [Card(name, suit, value, False) for suit in self.suits for name, value in self.card_values]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None

# Create decks for the player and the opponent (AI)
player_deck = Deck()
opponent_deck = Deck()
player_deck.shuffle()
opponent_deck.shuffle()

# Create hands for the player and the opponent
player_hand = [player_deck.draw() for _ in range(5)]
opponent_hand = [opponent_deck.draw() for _ in range(5)]

# Create discard piles for the player and the opponent
player_discard_pile = []
opponent_discard_pile = []

# Initialize play message variables
play_message = ""
message_timer = 0

# Function to display play message
def display_play_message(x_pos):
    font = pygame.font.Font(None, 30)
    text = font.render(play_message, True, WHITE)
    text_rect = text.get_rect(center=(x_pos, HEIGHT // 2))
    screen.blit(text, text_rect)

# Function to display game over message
def display_game_over_message(winner):
    font = pygame.font.Font(None, 100)
    if winner == 'AI':
        text = font.render(f"{winner} Wins!", True, RED)
    else:
        text = font.render(f"{winner} Win!", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 - 75))
    screen.blit(text, text_rect)
    font = pygame.font.Font(None, 30)
    replay_text = font.render("Play Again? (Y/N)", True, WHITE)
    replay_rect = replay_text.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2))
    screen.blit(replay_text, replay_rect)

# Function to display text in the center of the screen
def display_text_centered(text_list):
    font = pygame.font.Font(None, 30)
    text_surfaces = [font.render(line, True, WHITE) for line in text_list]
    text_rects = [text.get_rect(center=(WIDTH // 2, (i + 1) * 50)) for i, text in enumerate(text_surfaces)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and text_rects[-1].collidepoint(pygame.mouse.get_pos()):
                return

        screen.fill((0, 0, 0))

        for text_surface, text_rect in zip(text_surfaces, text_rects):
            screen.blit(text_surface, text_rect)

        pygame.display.flip()

# Function to display rules and handle back button
def display_rules():
    rules_text = [
        "Rules of the Game:",
        "- You and your AI opponent each have a deck of 52 cards.",
        "- Your goal is to make the AI run out of cards first.",
        "- Each turn, you can choose and play one card from your hand.",
        "- Your AI opponent will also play a card from their hand.",
        "- The AI will then discard cards from the top of his deck equal to",
        "  the value of the card you played. You do the same based on the AI card.",
        "- Values: A = 1, 2 = 2, 3 = 3, 4 = 4, ..., 10 = 10, J = 11, Q = 12 and K = 13.",
        "- You win when your opponent's HP reaches 0 before yours.",
        "- If both players' HP reaches 0 at the same time, the AI wins.",
        "- Good Luck, Have Fun!"
    ]

    back_button = pygame.Rect(25, 25, 100, 40)
    font = pygame.font.Font(None, 30)
    back_text = font.render("Back", True, WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(pygame.mouse.get_pos()):
                    return

        screen.fill((0, 0, 0))

        for i, line in enumerate(rules_text):
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, (i + 1) * 50))
            screen.blit(text_surface, text_rect)

        pygame.draw.rect(screen, RED, back_button)
        screen.blit(back_text, (back_button.x + 10, back_button.y + 10))

        pygame.display.flip()

# Function to display the credits screen
def credits_screen():
    credits_text = [
        "Credits:",
        "- Programming: xbackslash",
        "- Artwork: xbackslash",
        "- Music: 'Battle_52' by xbackslash",
        "",  # Add an empty line for spacing
        "Special Thanks:",
        "- OpenAI for ChatGPT",
        "- Pygame Community",
        "",  # Add an empty line for spacing
        "Thank You!",  # Your special message
    ]

    back_button = pygame.Rect(10, 10, 100, 40)
    font = pygame.font.Font(None, 30)
    back_text = font.render("Back", True, WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return  # Return to the main menu

        screen.fill((0, 0, 0))

        # Display the credits text
        for i, line in enumerate(credits_text):
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, (i + 1) * 50))
            screen.blit(text_surface, text_rect)

        # Create a back button
        pygame.draw.rect(screen, RED, back_button)
        screen.blit(back_text, (back_button.x + 10, back_button.y + 10))

        pygame.display.flip()

# Function to display the main menu
def main_menu():
    while True:
        screen.fill((0, 0, 0))

        # Create a title text
        title_font = pygame.font.Font(None, int(72 * SCALE_FACTOR))
        title_text = title_font.render("Battle 52", True, RED)
        title_text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        # Create a white-bordered version of the title text
        title_text_border = title_font.render("Battle 52", True, WHITE, BLACK)
        title_text_border_rect = title_text_border.get_rect(center=(WIDTH // 2 + 3, HEIGHT // 4 + 3))  # Slightly offset for the border effect

        # Create Ace of Spades card
        ace_spades = Card("Ace", "Spades", 1, False)
        ace_spades.x = 100
        ace_spades.y = HEIGHT // 3
        ace_spades.height = 150 * SCALE_FACTOR
        ace_spades.width = 100 * SCALE_FACTOR
        ace_spades.draw()

        # Create Ace of Hearts card
        ace_hearts = Card("Ace", "Hearts", 1, False)
        ace_hearts.x = 950
        ace_hearts.y = HEIGHT // 3
        ace_hearts.height = 150 * SCALE_FACTOR
        ace_hearts.width = 100 * SCALE_FACTOR
        ace_hearts.draw()

        # Create scaled Play button
        play_button = pygame.Rect(WIDTH // 2 - 75 * SCALE_FACTOR, HEIGHT // 2 - 50 * SCALE_FACTOR, 150 * SCALE_FACTOR, 50 * SCALE_FACTOR)
        pygame.draw.rect(screen, GREY, play_button)
        font = pygame.font.Font(None, int(36 * SCALE_FACTOR))
        play_text = font.render("Play", True, BLACK)
        play_text_rect = play_text.get_rect(center=play_button.center)

        # Create scaled Rules button
        rules_button = pygame.Rect(WIDTH // 2 - 75 * SCALE_FACTOR, HEIGHT // 2 + 10 * SCALE_FACTOR, 150 * SCALE_FACTOR, 50 * SCALE_FACTOR)
        pygame.draw.rect(screen, GREY, rules_button)
        rules_text = font.render("Rules", True, BLACK)
        rules_text_rect = rules_text.get_rect(center=rules_button.center)

        # Create scaled Exit button
        exit_button = pygame.Rect(WIDTH // 2 - 75 * SCALE_FACTOR, HEIGHT // 2 + 70 * SCALE_FACTOR, 150 * SCALE_FACTOR, 50 * SCALE_FACTOR)
        pygame.draw.rect(screen, GREY, exit_button)
        exit_text = font.render("Exit", True, BLACK)
        exit_text_rect = exit_text.get_rect(center=exit_button.center)
        
        # Create a Credits button
        credits_button = pygame.Rect(WIDTH - 175 * SCALE_FACTOR, HEIGHT - 60 * SCALE_FACTOR, 150 * SCALE_FACTOR, 50 * SCALE_FACTOR)
        pygame.draw.rect(screen, GREY, credits_button)
        credits_text = font.render("Credits", True, BLACK)
        credits_text_rect = credits_text.get_rect(center=credits_button.center)

        # Blit the title text and its border
        screen.blit(title_text_border, title_text_border_rect)
        screen.blit(title_text, title_text_rect)

        # Blit the Ace of Spades and Ace of Hearts cards
        ace_spades.draw()
        ace_hearts.draw()

        # Blit the button texts
        screen.blit(play_text, play_text_rect)
        screen.blit(rules_text, rules_text_rect)
        screen.blit(exit_text, exit_text_rect)
        # Blit the Credits button text
        screen.blit(credits_text, credits_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return "Play"
                elif rules_button.collidepoint(event.pos):
                    return "Rules"
                elif credits_button.collidepoint(event.pos):
                    return "Credits"
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# Function to run the game loop
def game_loop():
    player_deck = Deck()
    opponent_deck = Deck()
    player_deck.shuffle()
    opponent_deck.shuffle()
    player_hand = [player_deck.draw() for _ in range(5)]
    opponent_hand = [opponent_deck.draw() for _ in range(5)]
    player_discard_pile = []
    opponent_discard_pile = []
    play_message = ""
    message_timer = 0
    player_turn = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for card_index, card in enumerate(player_hand):
                    if card.x <= mouse_x <= card.x + card.width and card.y <= mouse_y <= card.y + card.height:
                        selected_card = player_hand.pop(card_index)
                        selected_card.draw(490, 275)
                        player_discard_pile.append(selected_card)
                        new_card = player_deck.draw()
                        if new_card:
                            new_card.draw(card.x, card.y)
                            player_hand.append(new_card)
                        opponent_discard_count = selected_card.value
                        for _ in range(opponent_discard_count):
                            opponent_card = opponent_deck.draw()
                            if opponent_card:
                                opponent_card.draw(50, 275)
                                opponent_discard_pile.append(opponent_card)
                        if play_message == "" or message_timer == 0:
                            play_message = f"You played {selected_card.name} of {selected_card.suit}"
                        message_timer = 180  # Set the desired duration
                        player_turn = False

            if not player_turn:
                # Choose a random card from the opponent's hand with value >= 5
                valid_opponent_cards = [card for card in opponent_hand if card.value >= 5]
                if valid_opponent_cards:
                    selected_card = random.choice(valid_opponent_cards)
                else:
                    # If no valid cards, choose a random card from the entire hand
                    selected_card = random.choice(opponent_hand)

                selected_card_index = opponent_hand.index(selected_card)
                selected_card = opponent_hand.pop(selected_card_index)

                selected_card.draw(50, 275)
                opponent_discard_pile.append(selected_card)
                opponent_discard_count = selected_card.value
                for _ in range(opponent_discard_count):
                    player_card = player_deck.draw()
                    if player_card:
                        player_card.draw(490, 275)
                        player_discard_pile.append(player_card)
                new_ai_card = opponent_deck.draw()
                if new_ai_card:
                    opponent_hand.append(new_ai_card)
                if play_message == "" or message_timer == 0:
                    play_message = f"AI played {selected_card.name} of {selected_card.suit}"
                    message_timer = 180  # Set the desired duration
                player_turn = True

        screen.fill((0, 0, 0))

        player_x = 50
        player_y = HEIGHT - padding - Card("A", "H", 1, False).height
        for card in player_hand:
            card.draw(player_x, player_y)
            player_x += card.width + 10

        opponent_x = 50
        opponent_y = padding
        for card in opponent_hand:
            card.draw(opponent_x, opponent_y)
            opponent_x += card.width + 10

        player_discard_x = 485
        player_discard_y = 270
        pygame.draw.rect(screen, GREY, (player_discard_x, player_discard_y, Card("A", "H", 1, False).width + 10, Card("A", "H", 1, False).height + 10))
        font = pygame.font.Font(None, 24)
        discard_text = font.render("Discard", True, BLACK)
        discard_rect = discard_text.get_rect(center=(player_discard_x + (Card("A", "H", 1, False).width + 10) // 2, player_discard_y + (Card("A", "H", 1, False).height + 10) // 2))
        screen.blit(discard_text, discard_rect)

        opponent_discard_x = 45
        opponent_discard_y = 270
        pygame.draw.rect(screen, GREY, (opponent_discard_x, opponent_discard_y, Card("A", "H", 1, False).width + 10, Card("A", "H", 1, False).height + 10))
        discard_text = font.render("AI Discard", True, BLACK)
        discard_rect = discard_text.get_rect(center=(opponent_discard_x + (Card("A", "H", 1, False).width + 10) // 2, opponent_discard_y + (Card("A", "H", 1, False).height + 10) // 2))
        screen.blit(discard_text, discard_rect)

        font = pygame.font.Font(None, 30)
        player_hp_text = font.render(f"Your Deck: {len(player_deck.cards)}", True, WHITE)
        player_hp_rect = player_hp_text.get_rect(midleft=(WIDTH - hp_padding - hp_offset, HEIGHT - padding - Card("A", "H", 1, False).height / 2))
        screen.blit(player_hp_text, player_hp_rect)

        opponent_hp_text = font.render(f"AI Deck: {len(opponent_deck.cards)}", True, WHITE)
        opponent_hp_rect = opponent_hp_text.get_rect(midleft=(WIDTH - hp_padding - hp_offset, padding + Card("A", "H", 1, False).height / 2))
        screen.blit(opponent_hp_text, opponent_hp_rect)

        for card in player_discard_pile:
            card.draw(card.x, card.y)

        for card in opponent_discard_pile:
            card.draw(card.x, card.y)

        if message_timer > 0:
            message_timer -= 1
            if message_timer == 0:
                play_message = ""

        if len(player_deck.cards) == 0:
            display_game_over_message("AI")
            pygame.display.flip()
            pygame.time.wait(3000)
            return "GameOver"
        elif len(opponent_deck.cards) == 0:
            display_game_over_message("You")
            win_sound.play()
            pygame.display.flip()
            pygame.time.wait(3000)
            return "GameOver"

        pygame.display.flip()

# Main game loop
while True:
    menu_choice = main_menu()

    if menu_choice == "Play":
        result = game_loop()
        if result == "GameOver":
            replay = False
            while not replay:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            replay = True
                        elif event.key == pygame.K_n:
                            pygame.quit()
                            sys.exit()

    elif menu_choice == "Rules":
        display_rules()
        
    elif menu_choice == 'Credits':
        credits_screen()

    elif menu_choice == "Exit":
        pygame.quit()
        sys.exit()
