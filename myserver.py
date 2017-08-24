import tensorflow as tf
from flask import Flask, request, jsonify, abort
app = Flask(__name__)

input_layer_name = "DecodeJpeg/contents:0"
output_layer_name = "final_result:0"

def load_graph(filename):
	"""Unpersists graph from file as default graph."""
	with tf.gfile.FastGFile(filename, 'rb') as f:
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(f.read())
		tf.import_graph_def(graph_def, name='')

labels = [line.rstrip() for line in tf.gfile.GFile("my_labels.pb")]
load_graph("my_graph.pb")

def run_graph(image_data, num_top_predictions):
	global input_layer_name
	global output_layer_name
	global labels
	with tf.Session() as sess:
		# Feed the image_data as input to the graph.
		#   predictions  will contain a two-dimensional array, where one
		#   dimension represents the input image count, and the other has
		#   predictions per class
		softmax_tensor = sess.graph.get_tensor_by_name(output_layer_name)
		predictions, = sess.run(softmax_tensor, {input_layer_name: image_data})

		# Sort to show labels in order of confidence
		top_k = predictions.argsort()[-num_top_predictions:][::-1]
		results = []
		for node_id in top_k:
			human_string = labels[node_id]
			score = predictions[node_id]
			score_print = '%s (score = %.5f)' % (human_string, score)
			results.append((human_string, score, score_print))
		return results


@app.route("/")
def hello():
	return "Hello world!"


@app.route("/get_prediction")
def get_prediction():
	if "image" not in request.files:
		abort(400, "Couldn't find an image file.")
	results = run_graph(request.files["image"], 5)
	return jsonify(results)

if __name__ == '__main__':
	app.run(host='0.0.0.0')
	

