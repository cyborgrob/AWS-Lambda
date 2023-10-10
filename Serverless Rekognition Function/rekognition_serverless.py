import boto3
import json

# Creates Rekognition client
rekog_client = boto3.client('rekognition')
# Creates s3 bucket resource
s3_bucket = boto3.resource('s3')
# Creates a bucket object from the resource for the destination bucket
bucket = s3_bucket.Bucket('YOUR_DESTINATION_BUCKET')
# Creates an SNS topic resource mapped to the topic of our choice
sns = boto3.resource('sns')
topic = sns.Topic('YOUR_SNS_TOPIC')
topicArn = 'SNS_ARN'


def lambda_handler(event, context):
    # Get source bucket and image name from event details
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    image_name = event['Records'][0]['s3']['object']['key']

    labels_resp = rekog_client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': image_name,
            }
        }
    )

    labels_list = [item['Name'] for item in labels_resp['Labels']]

    faces_resp = rekog_client.detect_faces(
        Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': image_name,
            }
        },
        Attributes=['AGE_RANGE', 'EMOTIONS', 'GENDER']
    )

    label_data = json.dumps(labels_resp)
    face_data = json.dumps(faces_resp)

    bucket.put_object(
        Body=label_data,
        Key=image_name + '-Label-Data'
    )

    bucket.put_object(
        Body=face_data,
        Key=image_name + '-Face-Data'
    )

    topic.publish(
        Message=f"""
        The image {image_name} has been processed successfully.

        Here is a list of objects detected:
        {labels_list}      
        """,
        Subject="Image Processed Successfully",
        TopicArn=topicArn,
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f'{image_name} processed successfully.')
    }
