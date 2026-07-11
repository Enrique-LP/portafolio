import json
import urllib.request
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
DEST_BUCKET = "xideralaws-curso-enrique2026"


def lambda_handler(event, context):
    # TODO implement
    years = [2023, 2024, 2025]
    months = [f"{m:02d}" for m in range(1, 13)]

    extracted_files = []
    failed_files = []

    print(f"Iniciando extracción masiva hacia el bucket: {DEST_BUCKET}")

    for year in years:
        for month in months:
            file_name = f"yellow_tripdata_{year}-{month}.parquet"
            source_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{file_name}"

            s3_key = f"nyc_taxi_raw/year={year}/month={month}/{file_name}"
            print(f"Procesando: {file_name}...")

            try:
                with urllib.request.urlopen(source_url) as response:
                    s3.put_object(
                        Bucket=DEST_BUCKET,
                        Key=s3_key,
                        Body=response.read(),
                        ContentType="application/x-parquet"
                    )
                print(f" Successfully uploaded to s3://{DEST_BUCKET}/{s3_key}")
                extracted_files.append(file_name)
            except ClientError as e:
                print(f" Error de AWS S3 al guardar {file_name}: {str(e)}")
                failed_files.append({"file": file_name, "error": str(e)})
            except Exception as e:
                print(f" Saltando/Error con {file_name}: {str(e)}")
                failed_files.append({"file": file_name, "error": str(e)})
            
    return {
        'statusCode': 200,
        'body': json.dumps({
            'mensaje': 'Proceso de extracción masiva finalizado',
            'bucket_destino': DEST_BUCKET,
            'archivos_exitosos': len(extracted_files),
            'archivos_fallidos_o_no_disponibles': len(failed_files),
            'detalle_exitosos': extracted_files
        })
    }