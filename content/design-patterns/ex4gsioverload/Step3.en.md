+++
title = "Step 3 - Query the Employees table using the GSI with overloaded attributes"
date = 2019-12-02T10:50:04-08:00
weight = 3
+++


You can query all the employees based in WA state using the sample Python script:

The *query_employees.py* script has the following code to query table using the GSI overloading:
```py
if attribute == 'name':
    ke = Key('GSI_1_PK').eq('master') & Key('GSI_1_SK').eq(value)
else:
    ke = "GSI_1_PK = :f"
    ke = Key('GSI_1_PK').eq(attribute + "#" + value)

response = table.query(
    IndexName='GSI_1',
    KeyConditionExpression=ke
    )
```

Run this command:
```bash
python query_employees.py employees state 'WA'
```
You will see an output like:
```txt
List of employees with WA in the attribute state:
    Employee name: Alice Beilby - hire date: 2014-12-03
    Employee name: Alla Absalom - hire date: 2015-06-25
    Employee name: Alvan Heliar - hire date: 2016-05-15
    Employee name: Anders Galtone - hire date: 2015-12-22
    Employee name: Ashil Hutchin - hire date: 2015-02-11
  ...
  Employee name: Sula Prattin - hire date: 2014-01-11
    Employee name: Vittoria Edelman - hire date: 2014-10-01
    Employee name: Willie McCuthais - hire date: 2015-05-27
Total of employees: 46. Execution time: 0.13477110862731934 seconds
```
You can try a different State changing the last parameter of the command above, like:
```bash
python query_employees.py employees state 'TX'
```
**The list of States with some data is in the sample data is: AZ, CA, CO, IL, IN, MA, MD, MI, NC, NY, OR, PA, TN, TX, and WA**

Using the same query, you can query the employees by job title. Run the following command as an example:
```bash
python query_employees.py employees current_title 'Software Engineer'
```
You will get the result:
```txt
 List of employees with Software Engineer in the attribute current_title:
    Employee name: Alice Beilby - hire date: 2014-11-03
    Employee name: Anetta Byrne - hire date: 2017-03-15
    Employee name: Ardis Panting - hire date: 2015-08-06
    Employee name: Chris Randals - hire date: 2016-10-27
    Employee name: Constantine Barendtsen - hire date: 2016-06-10
    Employee name: Eudora Janton - hire date: 2015-01-05
    Employee name: Florella Allsep - hire date: 2015-03-31
    Employee name: Horatius Trangmar - hire date: 2013-10-21
    Employee name: Korey Daugherty - hire date: 2016-11-03
    Employee name: Lenka Luquet - hire date: 2014-10-01
    Employee name: Leonora Hyland - hire date: 2016-06-14
    Employee name: Lucretia Ruffell - hire date: 2015-07-04
    Employee name: Malcolm Adiscot - hire date: 2014-04-17
    Employee name: Melodie Sebire - hire date: 2013-08-27
    Employee name: Menard Ogborn - hire date: 2014-06-27
    Employee name: Merwyn Petters - hire date: 2014-06-19
    Employee name: Niels Buston - hire date: 2014-10-30
    Employee name: Noelani Studde - hire date: 2015-03-30
Total of employees: 18. Execution time: 0.11937260627746582 seconds
```
You can try a different title, for example:
```bash
python query_employees.py employees current_title 'IT Support Manager'
```
**The list of the titles is**: *Application Developer,Application Support Analyst,Applications Engineer,Associate Developer,Chief Technology Officer (CTO) ,Chief Information Officer (CIO) ,Computer and Information Systems Manager,Computer Systems Manager,Customer Support Administrator,Customer Support Specialist,Data Center Support Specialist,Data Quality Manager,Database Administrator,Desktop Support Manager,Desktop Support Specialist,Developer,Director of Technology,Front End Developer,Help Desk Specialist,Help Desk Technician,Information Technology Coordinator,Information Technology Director,Information Technology Manager,IT Support Manager,IT Support Specialist,IT Systems Administrator,Java Developer,Junior Software Engineer,Management Information Systems Director,.NET Developer,Network Architect,Network Engineer,Network Systems Administrator,Programmer,Programmer Analyst,Security Specialist,Senior Applications Engineer,Senior Database Administrator,Senior Network Architect,Senior Network Engineer,Senior Network System Administrator,Senior Programmer,Senior Programmer Analyst,Senior Security Specialist,Senior Software Engineer,Senior Support Specialist,Senior System Administrator,Senior System Analyst,Senior System Architect,Senior System Designer,Senior Systems Analyst,Senior Systems Software Engineer,Senior Web Administrator,Senior Web Developer,Software Architect,Software Developer,Software Engineer,Software Quality Assurance Analyst,Support Specialist,Systems Administrator,Systems Analyst,System Architect,Systems Designer,Systems Software Engineer,Technical Operations Officer,Technical Support Engineer,Technical Support Specialist,Technical Specialist,Telecommunications Specialist,Web Administrator,Web Developer,Webmaster*

And using the same query, you can query the employees by name:
```bash
python query_employees.py employees name 'Dale Marlin'
```
You will get the result:
```txt
 List of employees with Dale Marlin in the attribute name:
    Employee name: Dale Marlin - hire date: 2014-10-19
Total of employees: 1. Execution time: 0.1274700164794922 seconds
```

*Congratulations, you have completed this exercise!*
