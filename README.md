# Cloudformation Mobile Notification Service

Cloudformation Mobile Notification Service is an orchestrated service that allows you to build and deploy your own service to deploy the code using Amazon API Gateway, AWS Lambda and CloudFormation. You can use this to send sms and whatsapp messages to the consumers using Twilio.


##### Twilio Configurations

Twilio is a tool to manage and simplify the communication issues. Twilio provides developer tools through PaaS model, or software-based platform which enables customers to easily add voice, messaging and video to their apps. It provides you with an API to send calls or SMS to any number.
In our service we used it for -
- Send WhatsApp messages
- Send SMS

You can register and get your twilio credentials here.
This credentials are to be specified in notification_sender/config.py file.

##### Steps to deploy

1. First, we need to configure aws credentials in aws_config.py file.
    ```
    REGION         = "us-east-2"
    STACK_NAME     = "NotificationService"
    BUCKET_NAME    = "cloudformation-templates-2021"
    BUCKET_PREFEIX = "api-deployment"
    CF_TEMPLATE    = "deploy-lambda-template.json"
    ACCESS_KEY     = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    SECRET_KEY     = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ```
2. Once the configurations are in place, run the deploy script using
    ```
    python deploy.py
    ```

![alt text](https://public-bucket-20210415.s3.us-east-2.amazonaws.com/Untitled.png "Title")

This script will zip the code from notification_sender and copy it to s3.
Once copied, it starts the execution of cloudformation template to provision Lambda and API Gateway.
The deploy script will also print the URL where it is deployed.

You can try this url to access this service as below -
![alt text](https://public-bucket-20210415.s3.us-east-2.amazonaws.com/Screenshot+2021-04-15+at+3.15.15+PM.png "Title")
You can change the msg_type to "sms", if you want to send the message as sms.


##### Automated Service Deployment CloudFormation Template

Altough we are deploy a mobile notification service in this app, the cloudformation template is designed in such a way that it can be used to deploy any other custom service.
