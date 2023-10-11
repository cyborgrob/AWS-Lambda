# Serverless AWS Rekognition Function
This function will automatically process an image using the AWS Rekognition service to detect faces and objects. The face and object data is converted into JSON format and stored in a designated destination bucket. The function will then publish to an SNS topic with details about the objects detected in the image.

Triggers for the source s3 bucket can be configured in the AWS console - specify the bucket and image (suffix) types. When an image is uploaded to the source bucket, the function will automatically execute.
