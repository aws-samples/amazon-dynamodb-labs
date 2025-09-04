---
title: "Stage 6 and 7: Infra and Data movement"
date: 2025-09-02T15:41:04-05:00
weight: 30
chapter: true
---

## Moving the data from MySQL to DynamoDB

At this point, we have created the dual database layer that allows our application to connect to DynamoDB and MySQL, we have configured the connectivity to DynamoDB, and we have refactored the entire application implementing the applicaton access patterns we need to support. What we need to do is to gradually move the data from one database to the other. There are several approaches you can follow in this regards, however we have choosen to use a Dual Write approach, where we will be sending data gradually to the DynamoDB table. This process consists of 5 different stages. 

## Phase 1: MySQL Only (Baseline State)

This phase represents your application's current operational state, serving as the foundation for the migration process. The dual abstraction layer is active, but all database operations route exclusively to MySQL. This configuration validates that your abstraction layer functions correctly without introducing any changes to existing data flows.

**Key Characteristics:**
- **Data Flow**: All read and write operations target MySQL exclusively
- **Performance Baseline**: Establish current system performance metrics for comparison
- **Risk Level**: Minimal - no changes to existing data operations
- **Validation Focus**: Confirm abstraction layer doesn't introduce performance overhead

**Operational Considerations:**
During this phase, implement comprehensive monitoring to establish baseline performance metrics. These measurements become reference points for evaluating the success of subsequent migration phases. Monitor response times, throughput rates, error frequencies, and resource utilization patterns to create a complete performance profile of your current system.

The abstraction layer validation ensures that the additional software layer doesn't negatively impact application performance or introduce unexpected behavior changes. This phase provides confidence that your migration infrastructure is solid before introducing DynamoDB operations.

## Phase 2: Dual Writes + MySQL Reads (Shadow Mode)

This phase introduces DynamoDB writes while maintaining MySQL as the exclusive read source. This "shadow mode" operation allows comprehensive testing of your DynamoDB implementation without affecting user-facing functionality, providing a safe environment to validate data transformations and identify integration issues.

**Shadow Mode Benefits:**
- **Risk Mitigation**: User experience remains unchanged as all reads come from MySQL
- **Data Validation**: Compare write operations between databases to ensure transformation accuracy
- **Performance Testing**: Evaluate DynamoDB write performance under real traffic patterns  
- **Error Detection**: Identify and resolve integration issues without user impact

**Implementation Strategy:**
Configure your dual database abstraction layer to write to both MySQL and DynamoDB simultaneously while routing all read operations to MySQL. Implement comprehensive logging to track any discrepancies between successful MySQL writes and failed DynamoDB operations. This logging provides debugging information for resolving integration issues.

**Parallel Data Migration Process:**
While shadow mode operates, execute a ETL (Extract, Transform, Load) process to migrate existing MySQL data to DynamoDB. This bulk migration uses your migration contract specifications to transform historical data according to your new NoSQL data model. The ETL process should validate data integrity and provide detailed reports on migration success rates and any encountered issues.

Monitor dual write success rates carefully, aiming for near-perfect parity between MySQL and DynamoDB write operations. Any persistent discrepancies indicate issues with your migration contract implementation or DynamoDB integration that must be resolved before proceeding.

## Phase 3: Dual Operations with MySQL Primary (Validation Phase)

This phase expands functionality to include reads from both databases while maintaining MySQL as the authoritative source. This configuration enables comprehensive validation of DynamoDB data accuracy and query performance while preserving the ability to fall back to MySQL for any inconsistencies.

**Dual Read Implementation:**
- **Primary Response**: MySQL provides the official response to user requests
- **Validation Query**: DynamoDB executes parallel queries for comparison
- **Consistency Checking**: System compares responses and logs discrepancies
- **Fallback Logic**: Any DynamoDB errors automatically fall back to MySQL results

**Performance Analysis:**
This phase provides the first opportunity to compare query performance between MySQL and DynamoDB under real traffic conditions. Monitor response times, throughput capabilities, and resource utilization for both systems. These metrics inform capacity planning decisions and help identify optimization opportunities.

**Data Consistency Validation:**
Implement automated comparison logic that validates data consistency between MySQL and DynamoDB responses. Log any discrepancies for analysis, paying particular attention to:
- **Data Transformation Accuracy**: Ensure migration contract transformations preserve data integrity
- **Timing Issues**: Identify any eventual consistency issues in DynamoDB reads
- **Query Logic Equivalence**: Verify that DynamoDB queries return functionally equivalent results

**Developer Confidence Building:**
This phase serves as a critical confidence-building period for development teams. Seeing consistent, accurate results from DynamoDB builds trust in the new system and provides validation that the migration effort is proceeding successfully.

## Phase 4: DynamoDB Primary with MySQL Fallback (Performance Validation)

This phase represents a significant milestone: DynamoDB becomes the primary data source while maintaining MySQL as a safety net. Users receive DynamoDB responses by default, with automatic fallback to MySQL if DynamoDB operations fail or return inconsistent results.

**Primary Source Transition:**
- **Default Response Source**: DynamoDB provides primary responses to user requests
- **Performance Monitoring**: Track DynamoDB response times and accuracy under full load
- **Automatic Fallback**: MySQL serves as backup for any DynamoDB failures
- **Confidence Building**: Validate that DynamoDB can handle production traffic reliably

**Rollback Preparedness:**
Maintain dual write operations during this phase to ensure MySQL data remains current for potential rollback scenarios. This configuration provides maximum safety while allowing real-world validation of DynamoDB performance and reliability.

**Critical Metrics Monitoring:**
Focus monitoring efforts on:
- **Response Time Comparison**: Measure DynamoDB performance against MySQL baseline
- **Error Rate Analysis**: Track any increase in application errors or timeouts
- **User Experience Impact**: Monitor user-facing performance metrics and satisfaction indicators
- **Capacity Utilization**: Ensure DynamoDB capacity settings handle production traffic appropriately

**Performance Optimization:**
Use real traffic patterns to identify optimization opportunities in your DynamoDB configuration. Adjust capacity settings, optimize query patterns, or refine GSI usage based on actual performance data rather than theoretical projections.

## Phase 5: DynamoDB Only (Complete Migration)

The final phase represents complete migration success: DynamoDB handles all database operations independently. MySQL writes cease, and the application operates entirely on the modern NoSQL infrastructure.

**Migration Completion Criteria:**
- **Performance Validation**: DynamoDB consistently meets or exceeds MySQL performance benchmarks
- **Reliability Confirmation**: Error rates remain within acceptable thresholds over extended periods
- **Feature Parity**: All application functionality works correctly with DynamoDB
- **Operational Readiness**: Support teams are trained and confident with DynamoDB operations

**Legacy System Decommissioning:**
Plan careful decommissioning of MySQL infrastructure:
- **Data Archival**: Preserve historical MySQL data according to compliance requirements
- **Monitoring Cleanup**: Remove MySQL-specific monitoring and alerting
- **Code Cleanup**: Remove dual database abstraction layer complexity
- **Documentation Updates**: Update operational procedures and system documentation

**Success Metrics:**
- **Performance Improvement**: Document quantifiable improvements in response times, throughput, or scalability
- **Operational Efficiency**: Measure improvements in operational overhead and maintenance requirements
- **Cost Optimization**: Calculate cost savings from improved resource utilization
- **Development Velocity**: Assess improvements in development team productivity with modern data access patterns

**Long-term Monitoring:**
Maintain enhanced monitoring during the initial post-migration period to quickly identify and resolve any issues that emerge in the fully migrated system. This vigilance ensures stable operation and builds confidence in the migration's long-term success.

## Migration Control Panel 

To simplify all of this process we created an Admin portal that allows you to control the migration phases using feature flags.

![Migration control panel](/static/images/modernizr/6/stage06-01.png)

This process will consist of 3 different actions:

1. Using the `migrationContract.json` generate MySQL views, and use MySQL mcp server to create them. 
2. Using the DynamoDB MCP server create the respective DynamoDB tables that are specified in the `migrationContract.json`
3. Create the Glue ETL scripts and run them to move the data from MySQL to DynamoDB using the Data processing MCP server (Glue MCP Server).


