+++
title = "Step 5 - Check the files format and content"
date = 2019-12-02T10:07:58-08:00
weight = 50
+++



You will be working with different data contents during this lab:
1. Server Logs data
2. Employees data
3. Invoices and Bills data

The Server Logs file has the following structure:

- requestid (number)
- host (string)
- date (string)
- hourofday (number)
- timezone (string)
- method (string)
- url (string)
- responsecode (number)
- bytessent (number)
- useragent (string)

To view a sample record in the file, execute:
```bash
head -n1 ./data/logfile_small1.csv
```
Sample log record:
```csv
1,66.249.67.3,2017-07-20,20,GMT-0700,GET,"/gallery/main.php?g2_controller=exif.SwitchDetailMode&g2_mode=detailed&g2_return=%2Fgallery%2Fmain.php%3Fg2_itemId%3D15741&g2_returnName=photo",302,5,"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
```
The Employees data file has the following structure:

- employeeid (number)
- name (string)
- title (string)
- dept (string)
- city (string)
- state (string)
- dob (string)
- hire-date (string)
- previous title (string)
- previous title end date (string)
- is a manager (string), 1 for manager employees, non-existent for others

To view a sample record in the file, execute:
```bash
head -n1 ./data/employees.csv
```
Sample employee record:
```csv
1,Onfroi Greeno,Systems Administrator,Operation,Portland,OR,1992-03-31,2014-10-24,Application Support Analyst,2014-04-12
```
