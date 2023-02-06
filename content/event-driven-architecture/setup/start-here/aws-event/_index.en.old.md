+++
title = "At an AWS Hosted Event"
date = 2019-12-02T07:05:12-08:00
weight = 3
chapter = true
pre = "<b>Start: </b>"
+++

### Introduction

You are provided with a temporary AWS account for the duration of this workshop. Each event has accounts that are already pre-configured for participant use. This page outlines how each participant can access their dedicated AWS account in order to begin this workshop.

### Event Engine

At the start of the workshop you may have been provided with a 16-character event hash by your presenter. This code grants you permission to use a dedicated AWS account for the purposes of this workshop. At the conclusion of this workshop you will lose access to the account and its contents.

If you don’t have the 16-character event hash, please get the code from your presenter. Note that if you were given a 1-click™ URL that pre-fills the event hash, you don't need to request the hash code from your presenter.

Alternatively, you can visit the link that you should see on the note on your place - the hash is already integrated into it.

1. Connect to the Event Engine dashboard by browsing to https://dashboard.eventengine.run/. You should see a prompt similar to below.

![EE Hash](/images/event-driven-architecture/event-engine/ee-hash.png)

2. Enter the provided hash in the text box. The button on the bottom right corner changes to `Accept Terms & Login`. Click on that button to continue.

3. Next, you'll be prompted to log in. You can either provide your e-mail address to obtain a one-time-password (OTP) or use your Amazon.com retail account to log in.

![EE Login](/images/event-driven-architecture/event-engine/ee-sign-in.png)

4. On the Team Dashboard, please click `Set Team Name` and specify a team name.

![EE AWS Console](/images/event-driven-architecture/event-engine/ee-teams.png)

5. Next, in the `Modules` section, click on `Readme` and follow the hyperlink to open the leaderboard. Keep the leaderboard open in a tab to check your score throughout the workshop.

![EE AWS Console](/images/event-driven-architecture/event-engine/ee-readme.png)

6. Now you can log into the AWS Console: Please click `AWS Console` on the Team Dashboard.

7. Click `Open AWS Console` to log into the AWS Management Console. For the purposes of this workshop, you will not use your local AWS CLI or local IDE; all work will take place inside the AWS Management Console.  For this reason you do not need the AWS credentials provided in this dialog.

![EE Console Login](/images/event-driven-architecture/event-engine/ee-console-login.png)

8. If you receive an error about being logged into another AWS account, please log out of that account and return to the previous step to attempt login to the dedicated AWS account. Now that you are connected, you should see the AWS Management Console view.

![EE AWS Console](/images/event-driven-architecture/event-engine/ee-aws-console.png)

9. Verify the region in the top right of your console is `N. California`. If this is not the region selected, click the region drop down and select `US West (N. California) us-west-1` before continuing.

10. You are now logged into the AWS Management Console for an account that was created for you, and which will be available only during the workshop.

For the workshop we have pre-configured a set of resources for you to save time. Please follow the instructions of your presenter to begin the lab.

Now that you are set up, continue on to: [Exercise 1: Overview]({{< ref "event-driven-architecture/ex1overview" >}}).
