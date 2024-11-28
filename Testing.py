import random
import csv

# Load the policy from the file
def load_policy(policy_file):
    with open(policy_file, "r") as f:
        return [int(line.strip()) for line in f.readlines()]

# Initialize the deck
def initialize_deck():
    return [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4

# Draw a random card from the deck
def draw_card(deck):
    card = random.choice(deck)
    deck.remove(card)
    return card

# Adjust the value of Aces
def adjust_for_ace(hand):
    total = sum(hand)
    ace_present = 11 in hand
    while total > 21 and ace_present:
        if 11 in hand:
            hand[hand.index(11)] = 1
        total = sum(hand)
        ace_present = 11 in hand
    return total, ace_present

# Dealer's logic
def dealer_play(deck, visible_card):
    hand = [visible_card, draw_card(deck)]
    total, _ = adjust_for_ace(hand)
    while total < 17:
        hand.append(draw_card(deck))
        total, _ = adjust_for_ace(hand)
    return total

# Map the state to the numerical index using mappings
def map_state_to_index(state, state_mappings):
    for mapped_state, index in state_mappings:
        if state == mapped_state:
            return index
    return 291  # Terminal state index

# Simulate a game using the given policy and log details
def simulate_game(policy, state_mappings):
    deck = initialize_deck()
    agent_hand = [draw_card(deck), draw_card(deck)]
    dealer_hand = [draw_card(deck), draw_card(deck)]
    dealer_visible_card = dealer_hand[0]
    agent_total, agent_has_ace = adjust_for_ace(agent_hand)
    cumulative_reward = 0  # Track the sum of rewards over all rounds
    game_rounds = []  # Store all round details (state, state number, action, reward, next state, next state number)

    while True:
        state = (agent_total, agent_has_ace, dealer_visible_card)
        state_index = map_state_to_index(state, state_mappings)
        action = policy[state_index - 1]  # Policy uses 1-based indexing

        if action == 1:  # Hit
            agent_hand.append(draw_card(deck))
            agent_total, agent_has_ace = adjust_for_ace(agent_hand)
            if agent_total > 21:  # Bust
                reward = -2 if dealer_visible_card != 11 else -1
                next_state = "terminal"
                next_state_index = 291
                game_rounds.append((state, state_index, action, reward, next_state, next_state_index))
                cumulative_reward += reward
                break
            else:
                reward = 0  # No reward until the end of the game
                next_state = (agent_total, agent_has_ace, dealer_visible_card)
                next_state_index = map_state_to_index(next_state, state_mappings)
                game_rounds.append((state, state_index, action, reward, next_state, next_state_index))
                cumulative_reward += reward

        elif action == 2:  # Stand
            dealer_total = dealer_play(deck, dealer_visible_card)
            if dealer_total > 21 or agent_total > dealer_total:
                reward = 2 if dealer_visible_card == 11 else 1
            elif agent_total < dealer_total:
                reward = -2 if dealer_visible_card != 11 else -1
            else:
                reward = 0.5 if dealer_visible_card == 11 else 0
            next_state = "terminal"
            next_state_index = 291
            game_rounds.append((state, state_index, action, reward, next_state, next_state_index))
            cumulative_reward += reward
            break

    # Determine game result based on cumulative reward
    if cumulative_reward in [+1, +2]:
        game_result = "Win"
    elif cumulative_reward in [0, 0.5]:
        game_result = "Tie"
    else:
        game_result = "Lose"

    return cumulative_reward, game_result, game_rounds

# Test the policy, simulate games, and log results
def test_policy_and_log(policy_file, state_mapping_file, output_csv, num_games=500):
    # Load policy and state mappings
    policy = load_policy(policy_file)
    with open(state_mapping_file, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header
        state_mappings = [(eval(row[0]), int(row[1])) for row in reader]

    results = []
    for game_id in range(num_games):
        cumulative_reward, game_result, game_rounds = simulate_game(policy, state_mappings)
        for round_data in game_rounds:
            results.append({
                "Game ID": game_id + 1,
                "State Name": round_data[0],
                "State Number": round_data[1],
                "Action": round_data[2],
                "Reward": round_data[3],
                "Next State Name": round_data[4],
                "Next State Number": round_data[5],
                "Game Result": game_result
            })

    # Write results to CSV
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Game ID", "State Name", "State Number", "Action", "Reward", "Next State Name", "Next State Number", "Game Result"])
        for result in results:
            if result["Next State Number"] != 291:
                writer.writerow([
                    result["Game ID"],
                    result["State Name"],
                    result["State Number"],
                    result["Action"],
                    result["Reward"],
                    result["Next State Name"],
                    result["Next State Number"],
                ])
            else:
                writer.writerow([
                    result["Game ID"],
                    result["State Name"],
                    result["State Number"],
                    result["Action"],
                    result["Reward"],
                    result["Next State Name"],
                    result["Next State Number"],
                    result["Game Result"]
                ])


    # Print win, tie, and loss percentages
    win_count = len(set(r["Game ID"] for r in results if r["Game Result"] == "Win"))
    tie_count = len(set(r["Game ID"] for r in results if r["Game Result"] == "Tie"))
    loss_count = len(set(r["Game ID"] for r in results if r["Game Result"] == "Lose"))
    win_percentage = (win_count / num_games) * 100
    tie_percentage = (tie_count / num_games) * 100
    loss_percentage = (loss_count / num_games) * 100
    print(f"Win percentage: {win_percentage:.2f}%")
    print(f"Tie percentage: {tie_percentage:.2f}%")
    print(f"Loss percentage: {loss_percentage:.2f}%")
    return win_percentage, tie_percentage, loss_percentage

if __name__ == '__main__':
    policy_file = "blackjack.policy"
    state_mapping_file = "state_mappings_with_numbers.csv"
    output_csv = "blackjack_simulation_results.csv"
    test_policy_and_log(policy_file, state_mapping_file, output_csv, num_games=500)


