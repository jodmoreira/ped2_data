from google.cloud import storage
import logging

# Configurando log
log = logging.getLogger()

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client.from_service_account_json('politica-em-dados-8c65c6185d17.json')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    log.info(f"File {source_file_name} stored at {destination_blob_name}.")
