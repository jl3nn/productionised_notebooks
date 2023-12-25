from flask import Flask, jsonify, request
import pandas as pd
from inference import processing as inference_processing
from training import processing as training_processing

app = Flask(__name__)

@app.route('/inference', methods=['POST'])
def inference():
    try:
        # Check if 'file' is in the request files
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        # Get the file from the request
        file = request.files['file']

        # Read the file into a DataFrame
        df = pd.read_csv(file)

        # Execute the inference processing function
        result = inference_processing(df)
        return jsonify({"result": [int(x) for x in result.tolist()]})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/training', methods=['POST'])
def training():
    try:
        # Check if 'file' is in the request files
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        # Get the file from the request
        file = request.files['file']

        # Read the file into a DataFrame
        df = pd.read_csv(file)

        # Execute the training processing function
        training_processing(df)
        return "training completed"
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
