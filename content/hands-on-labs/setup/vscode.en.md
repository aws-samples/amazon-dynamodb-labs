---
title: "Launch Visual Studio Code"
date: 2021-04-21T07:33:04-05:00
weight: 13
---

In addition to the AWS console you should open your Visual Studio code server, by clicking in the `VSCodeServerURL` parameter, available from the "Event Outputs" section. When prompted for a password use the value from `VSCodeServerPassword`. 

:image[Event dashboard]{src="/static/images/common/workshop-studio-02.png" disableZoom=true width=750}

Continue with the steps as listed in the section :link[Launch Visual Studio Code]{href="/hands-on-labs/setup/vscode"}.  

During the first 60 seconds, the environment will automatically update extensions and plugins. Any startup notification can be safely dismissed. 

:image[VS Code Setup]{src="/static/images/common/common-vs-code-01.png" disableZoom=true width=1000}

If a terminal is not available at the bottom left side of your screen, please open a new one, as shown in the picture below:

:image[VS Code Setup]{src="/static/images/common/common-vs-code-02.png" disableZoom=true width=900}

To verify that your AWS credentials have been properly configured, run the command `aws sts get-caller-identity` 

:image[VS Code Setup]{src="/static/images/common/common-vs-code-03.png" disableZoom=true width=1000}