import tflearn
import tensorflow as tf
import numpy as np

# Define the input shape
input_shape = [None, 5]

# Define the number of neurons in each layer
n_neurons_1 = 32
n_neurons_2 = 16

num_actions = 1

# Create a placeholder for the input data
state_ph = tf.placeholder(dtype=tf.float32, shape=input_shape)

# Define the fully connected layers
net = tflearn.fully_connected(state_ph, n_neurons_1, activation='relu')
net = tflearn.fully_connected(net, n_neurons_2, activation='relu')
logits = tflearn.fully_connected(net, num_actions, activation='linear')

# Define the output layer
policy = tf.nn.softmax(logits)

# Define the old policy
old_policy = tf.placeholder(dtype=tf.float32, shape=[None, num_actions])

# Define the action and advantage placeholders
action_ph = tf.placeholder(dtype=tf.int32, shape=[None])
advantage_ph = tf.placeholder(dtype=tf.float32, shape=[None])

# Define the probability of the selected actions under the current policy
indices = tf.stack([tf.range(tf.shape(action_ph)[0]), action_ph], axis=1)
probs = tf.gather_nd(policy, indices)

# Define the probability of the selected actions under the old policy
old_probs = tf.gather_nd(old_policy, indices)

# Define the ratio between the current and old probabilities
ratio = probs / old_probs

# Define the clipped surrogate loss
clip_range = 0.2
unclipped_loss = ratio * advantage_ph
clipped_loss = tf.clip_by_value(ratio, 1 - clip_range, 1 + clip_range) * advantage_ph
surrogate_loss = -tf.reduce_mean(tf.minimum(unclipped_loss, clipped_loss))

# Define the optimizer and training operation
optimizer = tf.train.AdamOptimizer(learning_rate=0.001)
train_op = optimizer.minimize(surrogate_loss)

# Create the session
sess = tf.Session()
sess.run(tf.global_variables_initializer())


def rollout(env, policy, num_steps):
    states = []
    actions = []
    rewards = []
    next_states = []
    dones = []

    state = env.reset()
    for t in range(num_steps):
        # Choose an action using the current policy
        action_probs = sess.run(policy, feed_dict={state_ph: state.reshape(1, -1)})
        action = np.random.choice(np.arange(len(action_probs.ravel())), p=action_probs.ravel())

        # Take a step in the environment
        next_state, reward, done, _ = env.step(action)

        # Save the transition
        states.append(state)
        actions.append(action)
        rewards.append(reward)
        next_states.append(next_state)
        dones.append(done)

        # Update the current state
        state = next_state

        # Stop the rollout if the episode is done
        if done:
            break

    return states, actions, rewards, next_states, dones

num_epochs = 600


def compute_gae(rewards, values, next_values, dones, gamma, lam):
    deltas = np.array(rewards) + gamma * np.array(next_values) * (1 - np.array(dones)) - np.array(values)
    advantages = np.zeros_like(deltas)
    advantage = 0
    for t in reversed(range(len(deltas))):
        advantage = deltas[t] + gamma * lam * (1 - np.array(dones)[t]) * advantage
        advantages[t] = advantage
    return advantages

def evaluate(env, policy, num_episodes=5):
    rewards = []
    for _ in range(num_episodes):
        state = env.reset()
        done = False
        total_reward = 0
        while not done:
            action_probs = sess.run(policy, feed_dict={state_ph: state.reshape(1, -1)})
            action = np.argmax(action_probs)
            state, reward, done, _ = env.step(action)
            total_reward += reward
        rewards.append(total_reward)
    return rewards

def update_old_policy():
    sess.run(update_old_pi_op)



# Train the policy network using PPO
for i in range(num_epochs):
    # Generate rollouts using the current policy
    states, actions, rewards, next_states, dones = rollout(env, policy, num_steps)

    # Compute advantages using the Generalized Advantage Estimation (GAE) algorithm
    values = sess.run(value_preds, feed_dict={state_ph: np.array(states)})
    next_values = sess.run(value_preds, feed_dict={state_ph: np.array(next_states)})
    advantages = compute_gae(rewards, values, next_values, dones, gamma, lam)

    # Update the policy and value function using the rollouts
    for j in range(num_batches):
        indices = np.random.randint(0, len(states), batch_size)
        batch_states = states[indices]
        batch_actions = actions[indices]
        batch_advantages = advantages[indices]
        batch_old_probs = old_probs_vals[indices]
        sess.run(train_op, feed_dict={state_ph: batch_states, action_ph: batch_actions,
                                      advantage_ph: batch_advantages, old_probs_ph: batch_old_probs})

    # Evaluate the new policy
    eval_rewards = evaluate(env, policy)
    print(f"Epoch {i}, average reward: {np.mean(eval_rewards)}")

    # Update the old policy with the new policy
    sess.run(update_old_policy)
