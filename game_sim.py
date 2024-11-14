import random
import csv
number_of_games = 10000

# Initialize the deck with 52 cards (4 of each number)
def initialize_deck():
    return [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4  # 4 of each card value (Ace = 11)

# Draw a random card from the deck without replacement
def draw_card(deck):
    card = random.choice(deck)
    deck.remove(card)  # Remove the drawn card from the deck to avoid duplicates
    return card

# Check if the hand contains an Ace and adjust value if necessary
def adjust_for_ace(hand):
    total = sum(hand)
    ace_present = 11 in hand
    while total > 21 and ace_present:
        # Only replace if there is currently an Ace (11) in hand
        if 11 in hand:
            hand[hand.index(11)] = 1  # Adjust Ace from 11 to 1
        total = sum(hand)
        ace_present = 11 in hand  # Update ace presence flag
    return total, ace_present

# Define the dealer's play logic
def dealer_play(deck, visible_card):
    hand = [visible_card, draw_card(deck)]
    total, _ = adjust_for_ace(hand)
    while total < 17:  # Dealer continues drawing until total is 17 or more
        hand.append(draw_card(deck))
        total, _ = adjust_for_ace(hand)
    return total

# Play a single game and record state transitions
def play_game():
    transitions = []
    deck = initialize_deck()  # Initialize a fresh deck at the start of each game

    # Initialize hands
    agent_hand = [draw_card(deck), draw_card(deck)]
    dealer_hand = [draw_card(deck), draw_card(deck)]
    dealer_visible_card = dealer_hand[0]
    
    agent_total, agent_has_ace = adjust_for_ace(agent_hand)
    
    while True:
        # Current state without dealer_visible_ace
        state = (agent_total, agent_has_ace, dealer_visible_card)
        
        # Randomly choose an action (for data generation; Q-learning will learn the best policy)
        action = random.choice(['hit', 'stand'])
        
        # State transition and reward
        if action == 'hit':
            agent_hand.append(draw_card(deck))
            agent_total, agent_has_ace = adjust_for_ace(agent_hand)
            next_state = (agent_total, agent_has_ace, dealer_visible_card)
            
            if agent_total > 21:  # Agent busts
                reward = -2 if dealer_visible_card != 11 else -1
                transitions.append((state, action, reward, 'terminal'))
                break
            else:
                reward = 0  # No reward until the end of the game
                transitions.append((state, action, reward, next_state))
        
        elif action == 'stand':
            dealer_total = dealer_play(deck, dealer_visible_card)
            
            if dealer_total > 21 or agent_total > dealer_total:
                reward = 2 if dealer_visible_card == 11 else 1
            elif agent_total < dealer_total:
                reward = -2 if dealer_visible_card != 11 else -1
            else:
                reward = 0.5 if dealer_visible_card == 11 else 0
            
            transitions.append((state, action, reward, 'terminal'))
            break

    return transitions

# Generate multiple games and save to CSV
def generate_data(num_games=1000):
    all_transitions = []
    for _ in range(num_games):
        game_data = play_game()
        all_transitions.extend(game_data)
    
    with open('qlearning_blackjack_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['state', 'action', 'reward', 'next_state'])
        for transition in all_transitions:
            writer.writerow(transition)

# Run data generation
generate_data(number_of_games)
