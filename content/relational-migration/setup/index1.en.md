---
title : "Dev Environment"
weight : 16
---
### Login to AWS Workshop Studio Portal

On the event dashboard, click on **Open AWS console** to federate into AWS Management Console in a new tab. On the same page, click **Get started** to open the workshop instructions.
![Event dashboard](/static/images/common/workshop-studio-01.png)

In addition to the AWS console you should open your Visual Studio code server, by clicking in the `VSCodeServerURL` parameter, available from the "Event Outputs" section. When prompted for a password use the value from `VSCodeServerPassword`. 

![Event dashboard](/static/images/common/workshop-studio-02.png)

During the first 60 seconds, the environment will automatically update extensions and plugins. Any startup notification can be safely dismissed. 
 
![VS Code Setup](/static/images/common/common-vs-code-01.png)

If a terminal is not available at the bottom left side of your screen, please open a new one like the following picture indicates.

![VS Code Setup](/static/images/common/common-vs-code-02.png)

Then run the command `aws sts get-caller-identity` just to verify that your AWS credentials have been properly configured.

![VS Code Setup](/static/images/common/common-vs-code-03.png)


From within the terminal:

To keep our python files and dependencies organized lets create a python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Clone the repository containing the Chalice code and migration scripts. Run:

```bash 
cd /home/participant/workshop/LSQL
git clone https://github.com/aws-samples/aws-dynamodb-examples.git
cd aws-dynamodb-examples
cd workshops/relational-migration
```

Next, run this to install three components: Boto3 (AWS SDK for Python), Chalice, and the MySQL connector for Python.

```bash
sudo pip3 install chalice mysql-connector-python
```

From the left navigation panel, locate our project folder by clicking into ```LSQL / aws-dynamodb-examples / workshops / relational-migration```

Navigate to the `.chalice` folder under the main **relational-migration** folder. Within this folder is the ```config.json``` file that holds the MySQL connection details. A script will automatically update this file in the next step.

Return to the terminal prompt window. Run this file which, uses AWS CLI commands to find the MySQL host's IP address and S3 bucket name, then sets them as environment variables, while also updating the Chalice config.json file:

```bash
source ./setenv.sh
```

You should see output similar to this:  
![setenv.sh settings](/static/images/relational-migration/setenv.png)

Your developer desktop is now configured for testing and deployment!

