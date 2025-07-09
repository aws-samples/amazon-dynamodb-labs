# Amazon DynamoDB Labs / Amazon DynamoDB Immersion Day
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

#### Internal maintainer: sync changes to internal copy of this repo
This public repo is pushed to the internal repo in workshop studio using a combination of rsync (we assume you are on macOS) and git. The file `sync.sh` copies the source files to the WS repo folder, and after that you follow the internal README.md to complete the sync.
1. Run sync.sh to sync the public repo to the amazon-dynamodb-immersion-day repo. e.g. `./sync.sh  -d /Users/$USER/workspace/amazon-dynamodb-immersion-day` . Choose y to sync the files.
2. Change into the directory for amazon-dynamodb-immersion-day (the workshop studio version), open README.md, and follow the instructions there to git add and push the changes internally. Note that some assets, specifically the LEDA central account resources, are only authored on the internal repo, and they have a separate set of commands to push updates because they are assets that must be in a special S3 bucket owned by WS.

## License
This project is licensed under the Apache-2.0 License.
