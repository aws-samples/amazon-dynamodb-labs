# Amazon DynamoDB Labs

### Setup:

#### Install Hugo:
On a mac:

`brew install hugo`

On Linux:
  - Download from the releases page: https://github.com/gohugoio/hugo/releases/tag/v0.46
  - Extract and save the executable to `/usr/local/bin`

#### Clone this repo:
From wherever you checkout repos:
`git clone git@github.com:aws-samples/amazon-dynamodb-labs.git` (or your fork)

#### Clone the theme submodule:
`cd amazon-dynamodb-labs`

`git submodule init; git submodule update`


#### Run Hugo locally:
To run hugo in development:
`hugo serve -D`

`hugo` will build your content locally and output to `./public/`


#### View Hugo locally:
Visit http://localhost:1313/ to see the site.

#### Making Edits:
As you save edits to a page, the site will live-reload to show your changes.

#### Auto deploy:

Within minutes of a commit to the master branch, a build and deploy using the default hugo grav learn theme will kick off. You can review your change at the following address.

https://master.amazon-dynamodb-labs.com

## License
This project is licensed under the Apache-2.0 License.
