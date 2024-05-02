import joblib
import tensorflow_decision_forests as tfdf
import pandas as pd
from google.cloud import storage
from google.oauth2 import service_account
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configura el cliente de Google Cloud Storage
credenciales = service_account.Credentials.from_service_account_file('service-account-file.json')
cliente_almacenamiento = storage.Client(credentials=credenciales)
nombre_cubo = 'testoneml'  # Nombre del bucket
cubo = cliente_almacenamiento.bucket(nombre_cubo)

# Ruta de acceso al directorio de Cloud Storage donde está almacenado el archivo del modelo exportado
ruta_modelo_cloud_storage = 'gs://testoneml/model_trained/pre_training/'

# Ruta HTTP para las solicitudes de predicción
ruta_prediccion_http = "/predict"

# Ruta HTTP para las verificaciones de estado
ruta_verificacion_estado_http = "/health"

@app.route(ruta_prediccion_http, methods=["POST"])
def prediction():
    try:
        # Obtiene los datos JSON de la solicitud
        datos_json_solicitud = request.get_json()

        # Obtiene la ruta del CSV de entrada de la solicitud o usa la predeterminada
        ruta_csv_prueba = request.args.get('test_csv_path', 'inference_dataset/test.csv')

        # Descarga el CSV de entrada de Cloud Storage
        blob_prueba = cubo.blob(ruta_csv_prueba)
        ruta_local_prueba = 'test.csv'
        blob_prueba.download_to_filename(ruta_local_prueba)

        # Carga los datos de prueba
        datos = pd.read_csv(ruta_local_prueba)

        # Carga el modelo desde Cloud Storage
        modelo_cargado = joblib.load(ruta_modelo_cloud_storage + 'trained_model.joblib')

        # Realiza predicciones con el modelo cargado
        conjunto_datos_prueba = tfdf.keras.pd_dataframe_to_tf_dataset(datos, task=tfdf.keras.Task.REGRESSION)
        predicciones = modelo_cargado.predict(conjunto_datos_prueba)

        # Convierte las predicciones a un DataFrame (opcional)
        dataframe_predicciones = pd.DataFrame(predicciones, columns=['Predicción'])

        # Devuelve las predicciones como JSON
        return jsonify({"predicciones": predicciones.tolist()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para la verificación de estado
@app.route(ruta_verificacion_estado_http, methods=["GET"])
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

