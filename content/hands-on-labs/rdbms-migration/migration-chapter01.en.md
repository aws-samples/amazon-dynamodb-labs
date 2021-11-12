+++
title = "Create an Key Pair"
menuTitle = "Create Key Pair"
date = 2021-04-25T07:33:04-05:00
weight = 15

+++
In this step, you will generate an EC2 key pair that you will use to connect to the EC2 instance.

  1. Sign in to your AWS Account [AWS Console](https://console.aws.amazon.com/) using an account with administrative privileges
  2. Select N. Virginia Region (us-east-1)
   ![Final Deployment Architecture](/images/migration1.jpg)
  3. Click [here](https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#KeyPairs:) to navigate to the Key Pair section in the EC2 console. Ensure you are in the same region as you chose in the previous step. Then, click on the Create Key Pair button
   ![Final Deployment Architecture](/images/migration3.jpg)
  4. Name the key pair rdbmsmigration, and then click Create. At this point, your browser will download a file named DMSKeyPair.pem. Save this file. You will need it to complete the tutorial.
   ![Final Deployment Architecture](/images/migration4.jpg)
