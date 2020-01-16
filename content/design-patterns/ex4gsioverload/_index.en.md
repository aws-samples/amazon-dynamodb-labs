+++
title = "GSI key overloading"
date = 2019-12-02T10:17:33-08:00
weight = 5
chapter = true
pre = "<b>Exercise 4: </b>"
+++


You can create 20 GSIs for a DynamoDB table. But sometimes, the application may need to support multiple access patterns, more than the currently allowed limit of GSIs per table. The GSI Key Overloading design pattern is enabled by designating and re-using an attribute name (column header) across different items types and storing a value in that attribute depending on the context of the item type. So when you create a GSI on that attribute, you are indexing for multiple access patterns, each for a different item type, and have used only 1 GSI. For example, consider the Employees table - an employee can contain items of type "metadata" (for employee details), "employee-title" (all the job titles that the employee has held), or "employee-location" (all the office buildings/locations the employee has worked).

The access patterns required for this scenario are:

- query all employees of a state
- query all employees with one specific current title
- query all employees who had ever one specific title
- query employees by name

The following figure presents the design of the table. The attribute called *PK* has the employee ID, prefixed by the letter 'e'. The hash sign is used as a separator between the entity type identifier ('e') and the actual employee ID. The attribute 'SK' is overloaded, and has either current title, previous title, or the keyword 'master' which denotes the primary item for the employee that holds most of their important attributes. The *GSI_1_PK* attribute includes the title or the name of the employee. The re-use of a given GSI for multiple entity types like employees, employee locations, and employee titles lets us simplify our management of the DynamoDB table because we only need to monitor and pay for one GSI as opposed to three separate indexes.

**Figure - Sample design for the Employees table using the GSI overloading pattern**
![Sample design for the Employees table using the GSI overloading pattern](/images/awsconsole4.png)
