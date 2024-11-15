---
title : "Dev Environment"
weight : 16
---

### Launch Cloud9 Developer Desktop

1. Begin by navigating to [AWS Cloud9 Console](https://console.aws.amazon.com/cloud9/home) or just type in *Cloud9* to the search box.

Notice the DynamoDBC9 instance, followed by an **Open** link under the Cloud9 IDE column.
   Click **Open** to launch AWS Cloud9 environment.
   You can close the Welcome page and find the command terminal at the bottom. Feel free to increase screen area,
   and navigate to Window - New Terminal at any time, to open a new terminal window.

From within the terminal:

2. Run the command ```aws sts get-caller-identity``` just to verify that your AWS credentials have been properly configured.

3. Clone the repository containing the Chalice code and migration scripts. Run:

```bash 
git clone https://github.com/aws-samples/aws-dynamodb-examples.git
git checkout cea34bc520512c70091aba2995de0e99a31d1078
```

*This checkout command ensures you are using a specific, tested version of the repository*

```bash
cd aws-dynamodb-examples/workshops/relational-migration
```

4. Next, run this to install three components: Boto3 (AWS SDK for Python), Chalice, and the MySQL connector for Python.

```bash
sudo python3 -m pip install boto3 chalice mysql-connector-python
```

5. From the left navigation panel, locate our project folder by
   clicking into ```aws-dynamodb-examples / workshops / relational-migration```

6. Find the gear icon near the top of the left nav panel, and click "show hidden files" .
   You may now see a folder called ```.chalice``` under the main **relational-migration** folder.
   Within this folder is the ```config.json``` file that holds the MySQL connection details.
   A script will automatically update this file in the next step.

7. Return to the terminal prompt window. Run this file which
   uses AWS CLI commands to find the MySQL host's IP address and S3 bucket name, then sets them as
   environment variables, while also updating the Chalice config.json file:

```bash
source ./setenv.sh
```

You should see output similar to this:
![setenv.sh settings](/static/images/relational-migration/setenv.png)

Your developer desktop is now configured for testing and deployment!

