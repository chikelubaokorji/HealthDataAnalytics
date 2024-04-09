import os
import boto3
import config
import zipfile

# kaggle environment variables
os.environ['KAGGLE_KEY'] = config.KAGGLE_KEY
os.environ['KAGGLE_USERNAME'] = config.KAGGLE_USERNAME
import kaggle


def main():
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(config.KAGGLE_DATASET, path='../datasets')

    with zipfile.ZipFile('../datasets/' + config.KAGGLE_DATASET.split('/')[1] + '.zip', 'r') as folder:
        folder.extractall(path='../datasets')
        os.remove('../datasets/' + config.KAGGLE_DATASET.split('/')[1] + '.zip')
        file_names = folder.namelist()

    s3 = boto3.resource(
        service_name=config.SERVICE_NAME,
        region_name=config.REGION_NAME,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )
    exclude_files = ['dimDiagnosisCode.csv', 'dimCptCode.csv', 'Datadictionery.csv']
    for file_name in file_names:
        if file_name not in exclude_files:
            s3.meta.client.upload_file('../datasets/' + file_name, config.BUCKET_NAME, file_name)
            print(f'Uploaded ==== {file_name}')


if __name__ == '__main__':
    main()
