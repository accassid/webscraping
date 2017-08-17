import tensorflow as tf
import socketserver as ss

def run_graph(image_data, labels, input_layer_name, output_layer_name, num_top_predictions):
	with tf.Session() as sess:
		# Feed the image_data as input to the graph.
		#   predictions  will contain a two-dimensional array, where one
		#   dimension represents the input image count, and the other has
		#   predictions per class
		softmax_tensor = sess.graph.get_tensor_by_name(output_layer_name)
		predictions, = sess.run(softmax_tensor, {input_layer_name: image_data})

		# Sort to show labels in order of confidence
		top_k = predictions.argsort()[-num_top_predictions:][::-1]
		for node_id in top_k:
			human_string = labels[node_id]
			score = predictions[node_id]
			print('%s (score = %.5f)' % (human_string, score))
		return 0


class MyServer(ss.BaseRequestHandler):
	def handle(self):
		self.data = self.request.recv(1024).strip()
		print("{} wrote:".format(self.client_address[0]))
		print(self.data)
		# just send back the same data, but upper-cased
		self.request.sendall(self.data.upper())


if __name__ == "__main__":
	HOST, PORT = "localhost", 9999

	# Create the server, binding to localhost on port 9999
	server = ss.TCPServer((HOST, PORT), MyServer)
	server.serve_forever()

