import boto3


def lambda_handler(event, context):
    # From the event JSON, extracts the bucket and file name. The event is when an object is uploaded to S3,
    # as specified using the 'Triggers' interface in the AWS console
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    obj_key = event['Records'][0]['s3']['object']['key']
    destination_bucket = 'YOUR_DESTINATION_BUCKET'

    # Copy object from source bucket to destination bucket
    s3 = boto3.resource('s3')
    copy_source = {
        'Bucket': source_bucket,
        'Key': obj_key,
    }
    bucket = s3.Bucket(destination_bucket)
    bucket.copy(copy_source, obj_key)

    # Publish to the SNS topic and print confirmation
    sns = boto3.resource('sns')
    topic = sns.Topic('YOUR_SNS_TOPIC')
    message = 'The backup to the destination bucket has been completed successfully.'
    subject = 'Backup Completed'
    resp = topic.publish(
        Message=message,
        Subject=subject,
    )
    message_id = resp['MessageId']
    print("MessageId: {}".format(message_id))
