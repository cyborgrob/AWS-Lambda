import boto3

# Create s3 resource and bucket object for your destination bucket
s3 = boto3.resource('s3')
bucket = s3.Bucket('YOUR_BACKUP_BUCKET')

# Create list of files you want to back up
list_of_files = ["YOUR_SAMPLE_FILES.txt"]

# Iterate through list and upload to s3. Parse file name for easier reading of uploaded objects
for file in list_of_files:
    with open(file, "r") as file_to_upload:
        parse_name_list = file.split("\\")
        obj = bucket.put_object(
            Body=file_to_upload.read(),
            Key=parse_name_list[-1]
        )
        print(obj.key + ' uploaded successfully')
