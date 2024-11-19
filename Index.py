import pandas as pd


# Expanding the tuples based on the new ranges and indexing method
first_entry_range_extended = range(1, 22)
second_entry_options = [True, False]
third_entry_range = range(2, 12)

# List to hold all tuples and their indexes
tuples_list_extended = []

# Existing 100 tuples
index = 1
for first in range(1, 11):
    for third in third_entry_range:
        tuples_list_extended.append(((first, False, third), index))
        index += 1

# Additional tuples up to 300 indexes
for first in range(11, 22):
    for third in third_entry_range:
        for second in second_entry_options:
            tuples_list_extended.append(((first, second, third), index))
            index += 1

# Creating a DataFrame to display results
tuples_df_extended = pd.DataFrame(tuples_list_extended, columns=["Tuple", "Index"])
tools.display_dataframe_to_user(name="Extended Indexed Tuples", dataframe=tuples_df_extended)

tuples_df_extended.head(), tuples_df_extended.tail()