
from flask import Flask, render_template, url_for, request, session, redirect, send_from_directory
import os,sys
import base64
from werkzeug.utils import secure_filename
import tensorflow as tf
import json
# sys.path.insert(0, '/tf_files')
# import label_image 

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, '/tf_files/server/static/uploads')

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

indentified = []

@app.route("/")
def hello():
    return "Hello World!"

def label_image(data):
    # change this as you see fit
    #image_path = data

    # Read in the image_data
    #image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    image_data = data

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line 
                       in tf.gfile.GFile("/tf_files/retrained_labels.txt")]

    print len(label_lines)

    # Unpersists graph from file
    with tf.gfile.FastGFile("/tf_files/retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        
        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})
        
        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        
        return (label_lines[top_k[0]], predictions[0][top_k[0]])

        # for node_id in top_k:
        #     human_string = label_lines[node_id]
        #     score = predictions[0][node_id]
        #     print('%s (score = %.5f)' % (human_string, score))

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    
    if request.method == 'POST':
        file = request.form['image']
        imgdata = base64.b64decode(file)
        filename = 'some_image.jpg'
        prediction = label_image(imgdata)

        indentified.append(json.dumps({ 'name': prediction[0], 'score': str(prediction[1]) }))
            
        
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     fname = filename
        #     full_path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
        #     fname_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #     download_link = '/downloads/%s' % fname

    return render_template('submit.html')

@app.route('/list', methods=['GET'])
def list():

    r = json.dumps(indentified)
    indentified[:] = []
    return r

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
