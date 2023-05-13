import tensorflow as tf

# Define the input shape
input_shape = (5,)

# Define the number of neurons in each layer
n_neurons_1 = 32
n_neurons_2 = 16

# Create a placeholder for the input data
X = tf.placeholder(dtype=tf.float32, shape=[None, *input_shape], name='X')

# Define the weights and biases for each layer
W1 = tf.Variable(tf.random.normal([input_shape[0], n_neurons_1]), dtype=tf.float32)
b1 = tf.Variable(tf.random.normal([n_neurons_1]), dtype=tf.float32)
W2 = tf.Variable(tf.random.normal([n_neurons_1, n_neurons_2]), dtype=tf.float32)
b2 = tf.Variable(tf.random.normal([n_neurons_2]), dtype=tf.float32)
W3 = tf.Variable(tf.random.normal([n_neurons_2, 1]), dtype=tf.float32)
b3 = tf.Variable(tf.random.normal([1]), dtype=tf.float32)

# Define the output of each layer
layer_1 = tf.nn.relu(tf.matmul(X, W1) + b1)
layer_2 = tf.nn.relu(tf.matmul(layer_1, W2) + b2)
output = tf.matmul(layer_2, W3) + b3

# Define the loss function
y_true = tf.placeholder(dtype=tf.float32, shape=[None, 1], name='y_true')
loss = tf.reduce_mean(tf.square(y_true - output))

# Define the optimizer
optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)
