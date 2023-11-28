# Amazon DynamoDB Labs
The repo for https://catalog.workshops.aws/dynamodb-labs/en-US , formerly https://amazon-dynamodb-labs.com

### Dev:

#### Local development
You can make code changes and markdown changes, but in order to test the build you need to be an Amazon employee with access to preview_build to compile the documentation and run the site locally. [Amazon employees click here for instructions](https://tiny.amazon.com/16x21plc5).

#### Clone this repo:
We suggest you make a fork. From wherever you are you can checkout the repo:

`git clone git@github.com:aws-samples/amazon-dynamodb-labs.git` (or your fork)

#### Making edits:
Amazon employees only: Make changes, run preview_build, check localhost:8080 to see the site locally

Everyone else: make changes, make a pull request, and wait for the automations to run. They will tell you if you have errors in your changes.

#### Pull requests
Make a pull request with changes. PRs will be automatically checked to make sure their markdown and other files are correct and without error using an automatic GitHub action. With each commit in a PR, the action will run to verify.

#### On merge to master

On merge to master, a GitHub action will deploy the assets to amazon-dynamodb-labs.com and verify the build to ensure the markdown and other files are correctly formatted. From there, a maintainer must manually pull the changes and push to https://catalog.workshops.aws/dynamodb-labs/en-US

## License
This project is licensed under the Apache-2.0 License.
