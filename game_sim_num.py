import random
import csv
import pandas as pd

number_of_games = 1000
data_collection = True

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
        action = random.choice([1, 2]) # hit = 1 , stand = 2
        
        # State transition and reward
        if action == 1:
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
        
        elif action == 2:
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
def generate_data(num_games = 1000):
    all_transitions = []
    all_transitions_num = []
    state_mappings = []

    for _ in range(num_games):
        game_data = play_game()
        all_transitions.extend(game_data)
    
    with open('blackjack_data_for_qlearning.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['state', 'action', 'reward', 'next_state'])
        for transition in all_transitions:
            writer.writerow(transition)

    # Expanding the tuples based on the new ranges and indexing method
    # convert to list
    all_transitions_num = all_transitions
    # first_entry_range_extended = range(1, 22)
    
    second_entry_options = [True, False]
    third_entry_range = range(2, 12)

    # List to hold all tuples and their indexes
    tuples_list_extended = []

    # Existing 100 tuples
    index = 1
    for first in range(4, 11):
        for third in third_entry_range:
            tuples_list_extended.append(((first, False, third), index))
            state_mappings.append(((first, False, third), index))
            index += 1

    # Additional tuples up to 300 indexes
    for first in range(11, 22):
        for third in third_entry_range:
            for second in second_entry_options:
                tuples_list_extended.append(((first, second, third), index))
                state_mappings.append(((first, second, third), index))
                index += 1

    # Creating a DataFrame to display results
    # tuples_df_extended = pd.DataFrame(tuples_list_extended, columns=["Tuple", "Index"])
    # all_transitions_num[0][0] = 1
    # print(all_transitions_num[0])
    for i in range(len(all_transitions_num)):
        all_transitions_num[i] = list(all_transitions_num[i])
        for k in range(len(tuples_list_extended)):
            if all_transitions_num[i][0] == tuples_list_extended[k][0]:
                # print("true")
                all_transitions_num[i][0] = tuples_list_extended[k][1]
                
            if all_transitions_num[i][3] == tuples_list_extended[k][0]:
                all_transitions_num[i][3] = tuples_list_extended[k][1]
        if all_transitions_num[i][3] == 'terminal':
                all_transitions_num[i][3] = 291

    state_mapping_file_path = 'state_mappings_with_numbers.csv'
    with open(state_mapping_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['State', 'Number'])
        for state, number in state_mappings:
            writer.writerow([state, number])
    
    with open('blackjack_data_for_qlearning_num.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['state', 'action', 'reward', 'next_state'])
        for transition in all_transitions_num:
            writer.writerow(transition)


   

if __name__ == '__main__':
    if data_collection == True:
        # Run data generation
        generate_data(number_of_games)


