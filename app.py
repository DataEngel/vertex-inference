import joblib
import tensorflow_decision_forests as tfdf
import pandas as pd
import os
import google.cloud.storage as gs
import numpy as np

# Función para cargar el modelo desde Google Cloud Storage
def load_model_from_gcs(model_file_name):
    # Ruta del archivo de modelo en GCS
    aip_storage_uri = os.environ['AIP_STORAGE_URI']  # gs-path to directory with model artifacts
    aip_storage_uri = aip_storage_uri.replace('gs://', '')

    if aip_storage_uri.endswith('/'):
        aip_storage_uri = aip_storage_uri[:-1]
    first_slash = aip_storage_uri.find('/')
    if first_slash > 0:
        bucket_name = aip_storage_uri[:first_slash]
        model_path = aip_storage_uri[first_slash+1:]

    storage_client = gs.Client()
    bucket = storage_client.get_bucket(bucket_name)

    # Descargar el archivo binario del modelo desde GCS
    blob = bucket.get_blob(f"{model_path}/{model_file_name}")
    local_file_name = f"{model_file_name}.joblib"
    blob.download_to_filename(local_file_name)

    # Cargar el modelo desde el archivo binario
    loaded_model = joblib.load(local_file_name)
    return loaded_model

# Función para leer el archivo CSV directamente desde Google Cloud Storage
def read_csv_from_gcs(file_name):
    # Ruta del archivo CSV en GCS
    aip_storage_uri = os.environ['AIP_STORAGE_URI']  # gs-path to directory with model artifacts
    aip_storage_uri = aip_storage_uri.replace('gs://', '')

    if aip_storage_uri.endswith('/'):
        aip_storage_uri = aip_storage_uri[:-1]
    first_slash = aip_storage_uri.find('/')
    if first_slash > 0:
        bucket_name = aip_storage_uri[:first_slash]
        csv_path = aip_storage_uri[first_slash+1:]

    storage_client = gs.Client()
    bucket = storage_client.get_bucket(bucket_name)

    # Descargar el archivo CSV desde GCS
    blob = bucket.get_blob(f"{csv_path}/{file_name}")
    return pd.read_csv(blob.download_as_text(), index_col=None)

# Función para guardar las predicciones en un archivo en Google Cloud Storage
def save_predictions_to_gcs(predictions, output_file_name):
    # Ruta del archivo de salida en GCS
    aip_storage_uri = os.environ['AIP_STORAGE_URI']  # gs-path to directory with model artifacts
    aip_storage_uri = aip_storage_uri.replace('gs://', '')

    if aip_storage_uri.endswith('/'):
        aip_storage_uri = aip_storage_uri[:-1]
    first_slash = aip_storage_uri.find('/')
    if first_slash > 0:
        bucket_name = aip_storage_uri[:first_slash]
        output_path = aip_storage_uri[first_slash+1:]

    storage_client = gs.Client()
    bucket = storage_client.get_bucket(bucket_name)

    # Guardar las predicciones en un archivo CSV en GCS
    output_data = pd.DataFrame(predictions, columns=["Prediction"])
    output_blob = bucket.blob(f"{output_path}/{output_file_name}")
    output_blob.upload_from_string(output_data.to_csv(index=False), content_type='text/csv')

# Cargar el modelo desde Google Cloud Storage
loaded_model = load_model_from_gcs("houses_trained_model")

# Leer el archivo CSV directamente desde Google Cloud Storage
test_data = read_csv_from_gcs("test.csv")

# Hacer inferencias con el modelo cargado
test_ds = tfdf.keras.pd_dataframe_to_tf_dataset(test_data, task=tfdf.keras.Task.REGRESSION)
predictions = loaded_model.predict(test_ds)

# Guardar las predicciones en un archivo en Google Cloud Storage
save_predictions_to_gcs(predictions, "predictions.csv")
