---
title: "1.3 Stage Artifacts"
menuTitle: "Stage Artifacts"
date: 2025-09-02T10:43:04-05:00
weight: 33
chapter: false
---

Each stage generates "Artifacts" deliverables that will be used in the future stages across the solution, this project works sequentially, where you will see how artifacts from initial stages are re-used. Every stage will create a new folder `stage-xx` where all the artifacts will be stored. In addition another file `xx-working_log.md` will be generated, this file is used by the LLM to keep track of the work that has been done so far, consider it as a notepad, or scratch pad. 

::alert[If you execute this workshop from scratch (as available in `/clean-start` folder) it will take ~11.5 hours to complete, where the most of its time will be spent in application re-factoring (stages 3, 4 and 5). For simplicity and to streamline the duration of this workshop you will have these steps already completed for you.]{type="info"}

# Stage-01 artifacts

Let's start exploring the artifacts available for the first stage `stage-01`. This stage is focused on capturing the data that is available from the source database and application backend logic. We use the MySQL MCP server to understand table structure, constraints and data, The MySQL query logs, to identify the data velocity and finally we explore the application logic to capture all the access patterns that we will need to modernize. 

![Artifacts](/static/images/modernizr/1/workflow-artifacts-01.png)

DynamoDB is all about application access patterns that we need to support, how the data in your application will be using the DynamoDB tables. The secret to DynamoDB data modelling is to store the data exactly in the format your application will consume it, while working with different entities if you happen to have some. 

Open the files available in the `stage-01` folder, familiarize with them and understand in detail the current application access patterns, remember this is the application logic that you will need to support in the modernized application. 

- `01_1_API_access_patterns.md` - This file should be your primary source of information, it contains an analysis of the backend code, it should contain at the end a numbered list of 48 different application access patterns! You can also learn more about this project by reading the README available in the front end folder `frontend/README.md` It contains a description of which patters requires authentication and a quick explanation on how to execute the API calls. 
- `01_2_mysql_log_analysis.md` - This file is the MySQL log analysis, it contains a description of how many times some access patterns were detected, we run a small load test to simulate some traffic, and capture meaningful information, please notice the load test does not capture 100% of the application access patterns with the logs. If you plan to use a similar approach for your modrnization process, you need to enable the logs for a period of time that allows you to capture most of your traffic, however you should keep in mind there might be some application access patters that might not be covered, since the API endpoints might not have enough traffic to be collected during the test. 
- `01_3_table_structure_analysis.md` - Uses the MySQL MCP server to explore table structure and identify table contraints, relationships and data format. 

