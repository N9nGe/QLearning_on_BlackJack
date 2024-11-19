using Random, DataFrames, CSV
using Printf
using Dates

time_1 = now()

mutable struct QLearning
    S # state space (assumes 1:nstates)
    A # action space (assumes 1:nactions)
    Gamma # discount
    Q # action value function
    alpha # learning rate
end



# Update function for Q-learning
function update!(model::QLearning, s, a, r, sp)
    Gamma, Q, alpha = model.Gamma, model.Q, model.alpha
    Q[s, a] += alpha * (r + Gamma * maximum(Q[sp, :]) - Q[s, a])
end

# Function to train the Q-learning model using provided data
function train_qlearning(model::QLearning, data::DataFrame, num_episodes)
    for episode in 1:num_episodes
        for row in eachrow(data)
            s, a, r, sp = row.state, row.action, row.reward, row.next_state
            update!(model, s, a, r, sp)
        end
    end
end

# Function to extract the best policy from the trained Q-table
function best_policy(model::QLearning)
    policy = [argmax(model.Q[s, :]) for s in 1:model.S]
    return policy
end

## loading the data
print(pwd())
cd("c:/Users/jackr/OneDrive - Stanford/CS238FinalProject")
data = CSV.read("qlearning_blackjack_data(6)_num.csv", DataFrame)

# Initialize and train the model
num_states = 321
num_actions = 2
discount=0.95
learning_rate=0.1
Q = zeros(num_states, num_actions)
model = QLearning(num_states, num_actions, discount, Q, learning_rate)
iteration = 1000
train_qlearning(model, data, iteration)


# Get the best policy
policy = best_policy(model)
#print(policy)

######## Get Running Time #########
time_2 = now()
println("running_time small:", iteration, " iterations")
println(time_2 - time_1)
###################################
## writing the file
function small_policy(file_name::String)
    open(file_name, "w") do f  # Opens the file in write mode
        for si in 1:321
            write(f, @sprintf("%d\n", policy[si])) 
        end
    end
end

small_policy("first.policy")
print("finished")