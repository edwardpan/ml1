from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

mnist = input_data.read_data_sets(".", one_hot=True, reshape=False)

save_file = "./model.ckpt"
learning_rate = 0.001
training_epochs = 20
batch_size = 128
display_step = 1

n_input = 784
n_classes = 10

n_hidden_layer = 256

weights = {
    "hidden_layer": tf.Variable(tf.random_normal([n_input, n_hidden_layer]), name="weights_0"),
    "out": tf.Variable(tf.random_normal([n_hidden_layer, n_classes]), name="weights_1")
}
biases = {
    "hidden_layer": tf.Variable(tf.random_normal([n_hidden_layer]), name="biases_0"),
    "out": tf.Variable(tf.random_normal([n_classes]), name="biases_1")
}

x = tf.placeholder(tf.float32, [None, 28, 28, 1])
y = tf.placeholder(tf.float32, [None, n_classes])

x_flat = tf.reshape(x, [-1, n_input])

layer_1 = tf.add(tf.matmul(x_flat, weights["hidden_layer"]), biases["hidden_layer"])
layer_1_out = tf.nn.relu(layer_1)

logits = tf.add(tf.matmul(layer_1_out, weights["out"]), biases["out"])

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=y))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cost)

correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

init = tf.global_variables_initializer()
saver = tf.train.Saver()

with tf.Session() as session:
    session.run(init)
    print(session.run(weights["hidden_layer"]))

    for epoch in range(training_epochs):
        total_batch = int(mnist.train.num_examples/batch_size)
        if mnist.train.num_examples % batch_size > 0:
            total_batch += 1
        for i in range(total_batch):
            batch_x, batch_y = mnist.train.next_batch(batch_size)
            session.run(optimizer, feed_dict={x: batch_x, y: batch_y})

        if epoch % 10 == 0:
            valid_accuracy = session.run(accuracy, feed_dict={x: mnist.validation.images, y: mnist.validation.labels})
            print("Epoch {:<3} - Validation Accuracy: {}".format(epoch, valid_accuracy))

    print(session.run(weights["hidden_layer"]))
    saver.save(session, save_file)
    print("Trained Model Saved.")