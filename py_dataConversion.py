import os
import pandas as pd

# Change directory
os.chdir("c:/Users/jackr/Downloads/CS238FinalProject")

# Load the data
data = pd.read_csv("qlearning_blackjack_data(3).csv")

# Iterate over rows and print the state with specific formatting
for _, row in data.iterrows():
    s, a, r, sp = row['state'], row['action'], row['reward'], row['next_state']
    print(s[1:3])  # Check the purpose of `s(0)`; if `s` is callable, this will work. Otherwise, adjust as needed.