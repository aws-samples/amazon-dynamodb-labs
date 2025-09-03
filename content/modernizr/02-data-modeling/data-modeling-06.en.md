---
title: "2.6 Migration Contract"
menuTitle: "Migration Contract"
date: 2025-09-02T16:43:04-05:00
weight: 37
chapter: false
---

## The Migration Contract: Your Modernization Blueprint

The Migration Contract represents the culmination of all previous analysis and design work. This JSON artifact serves as the definitive mapping specification that translates your existing MySQL schema into the optimized DynamoDB structure. Think of it as a detailed transformation blueprint that precisely defines how each piece of data moves from the relational model to the NoSQL implementation.

The contract encapsulates critical information including source table mappings, data transformation logic, attribute conversions, and relationship restructuring. Every subsequent stage of the modernization workflow depends on this contract, making its accuracy paramount to project success.

## Initiating Contract Generation

Execute the contract generation process with this command:

```shell
Thanks. Please mark tasks 3 as completed, and continue with the task 4.1 `prompts/02-dynamodb-data-modeling/tasks.m`
```

## Understanding Contract Architecture

The Migration Contract implements a sophisticated transformation engine that supports multiple data conversion patterns. The system includes built-in validation guardrails that ensure the generated JSON adheres to strict specification requirements, preventing arbitrary or invalid transformations.

Explore the `contracts` folder to understand the supported transformation patterns, validation rules, and architectural constraints. This reference documentation provides comprehensive details on how the contract functions as both a specification document and an execution engine for the data migration process.

![Data model](/static/images/modernizr/2/stage02-23.png)

## Contract Quality Assurance

The contract generation process may require iterative refinement depending on the complexity of your data model and the AI system's interpretation of requirements. Success depends on meticulous validation of the generated contract against your established specifications.

## Common Validation Issues and Solutions

During contract generation, monitor for these frequent issues that require manual correction:

::alert[DO NOT Blindly copy and paste the following prompts! They are examples of previous executions, you might not need them! please pay attention to the information in your `migrationContract.json` ]{type="error"}

### Naming Convention Violations

AI systems sometimes deviate from specified naming conventions, creating custom table or attribute names instead of using the standardized schema:

```bash
You will need to validate the creation of the migration contract, I see you have defined your own table names, and you didn't used the table names I have provided, same for the GSIs I specifically asked for generic names for the GIS and the PK and SK to avoid issues or hardcoded values. To give you an example in the migration contract artifacts/stage-02/migrationContract.json the first table `UserOrdersCart` should be called `Users`, the partition key should be PK and the sort tkey SK, Please re-read the data_model and update my migration contract
```

### Invalid Transformation Methods

The system may generate non-existent transformation functions instead of using the supported contract specifications:

```bash
I noticed you have a made up transformation called `json-parse` it should be `json-construction` The format of that attribute is a map so you need to use JSON contruction, can you please update that attribute name?  and validate you have no created other made up methods? you need to follow the specifications as directed in the  `contracts` folder
```

## Contract Validation Protocol

Thoroughly review the generated `migrationContract.json` for:

- **Schema Consistency**: Verify all table names, attribute names, and GSI references match your data model specifications
- **Transformation Validity**: Ensure all transformation methods exist in the contracts specification
- **Data Type Mapping**: Confirm MySQL data types are correctly mapped to DynamoDB equivalents
- **Relationship Preservation**: Validate that entity relationships are properly represented in the NoSQL structure

## Backup and Recovery Strategy

Given the critical nature of this artifact, the workshop provides a verified migration contract as a fallback option. This ensures project continuity even if the AI-generated contract contains errors.

### Recovery Process

If your generated contract contains significant issues:

1. Rename your current `artifacts/stage-02` folder to `artifacts/stage-02-workshop`
2. Copy the `core-outputs/stage-02` folder to the `artifacts` directory
3. Compare the provided artifacts with your generated versions to identify differences
4. Use the comparison analysis to improve future contract generation sessions

This backup strategy ensures you can proceed with the workshop while learning from any discrepancies between AI-generated and verified outputs.
