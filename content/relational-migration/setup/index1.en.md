---
title : "Dev Environment"
weight : 16
---

[AWS Cloud9](https://aws.amazon.com/cloud9/) is a cloud-based integrated development environment (IDE) that lets you write, run, and debug code with just a browser. AWS Cloud9 includes a code editor, debugger, and terminal. It also comes prepackaged with essential tools for popular programming languages and the AWS Command Line Interface (CLI) preinstalled so that you don’t have to install files or configure your laptop for this lab. Your AWS Cloud9 environment will have access to the same AWS resources as the user with which you signed in to the AWS Management Console.

### To set up your AWS Cloud9 development environment:

1. Choose **Services** at the top of the page, and then choose **Cloud9** under **Developer Tools**.

2. There would be an environment ready to use under **Your environments**.

3. Click on **Open IDE**, your IDE should open with a welcome note.

You should now see your AWS Cloud9 environment. You need to be familiar with the three areas of the AWS Cloud9 console shown in the following screenshot:

![Cloud9 Environment](/static/images/zetl-cloud9-environment.png)

- **File explorer**: On the left side of the IDE, the file explorer shows a list of the files in your directory.

- **File editor**: On the upper right area of the IDE, the file editor is where you view and edit files that you’ve selected in the file explorer.

- **Terminal**: On the lower right area of the IDE, this is where you run commands to execute code samples.


From within the terminal:

2. Run the command ```aws sts get-caller-identity``` just to verify that your AWS credentials have been properly configured.

3. Clone the repository containing the Chalice code and migration scripts. Run:

```bash 
cd ~/environment
git clone https://github.com/aws-samples/aws-dynamodb-examples.git
cd aws-dynamodb-examples
git checkout :param{key="lsql_git_commit"}
```


*This checkout command ensures you are using a specific, tested version of the repository*

```bash
cd workshops/relational-migration
```

4. Next, run this to install three components: Boto3 (AWS SDK for Python), Chalice, and the MySQL connector for Python.

```bash
pip3 install chalice mysql-connector-python
export PATH="/home/ubuntu/.local/bin:$PATH"
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

