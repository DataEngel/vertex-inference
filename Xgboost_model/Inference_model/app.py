import xgboost as xgb
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Carga el modelo de XGBoost desde un archivo
model = xgb.Booster()
model.load_model('model.bst')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Captura los datos de entrada desde la solicitud POST
        input_data = request.json

        # Convierte el JSON de entrada a una matriz numpy
        data = np.array(input_data["instances"])

        # Crea un DMatrix para la predicción
        dmatrix = xgb.DMatrix(data)

        # Realiza la predicción usando el modelo cargado
        predictions = model.predict(dmatrix)

        # Devuelve las predicciones en formato JSON
        result = {"predictions": predictions.tolist()}
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/health_check')
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

