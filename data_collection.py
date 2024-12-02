import csv
from game_sim import *

number_of_games = 1000
data_collection = True

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


