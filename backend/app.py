from flask import Flask, jsonify, request
from flask_cors import CORS
from routes.predict import predict_price

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    result = predict_price(data)
    if result is not None:
        return jsonify({'predicted_price': float(result)})  
    return jsonify({'error': 'Prediction failed'}), 500


if __name__ == '__main__':
    app.run(debug=True)
