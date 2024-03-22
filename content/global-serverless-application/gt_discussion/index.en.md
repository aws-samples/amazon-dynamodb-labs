---
title : "Global Tables Discussion Topics"
weight : 50
---

Below are some discussion topics for people who’ve finished the development work or would like 
to discuss interesting aspects of Global Tables with a DynamoDB specialist.


## What are Global Tables?
* Global tables build on the global Amazon DynamoDB footprint to provide you with a fully managed, multi-Region, and multi-active database that delivers fast, local, read and write performance for massively scaled, global applications. Global tables replicate your DynamoDB tables automatically across your choice of AWS Regions.
* Global tables eliminate the difficult work of replicating data between Regions and resolving update conflicts, enabling you to focus on your application's business logic. In addition, global tables enable your applications to stay highly available even in the unlikely event of isolation or degradation of an entire Region.
* You can set up global tables in the AWS Management Console or AWS CLI. No application changes are required because global tables use existing DynamoDB APIs. There are no upfront costs or commitments for using global tables, and you pay only for the resources provisioned.

## How am I charged for using Global Tables?
* A write to a traditional DynamoDB table is priced in Write Units (where if you write a 5 KB item it incurs a charge of 5 Write Units). A write to a global table is priced in Replicated Write Capacity Units (rWCUs, for provisioned tables) or Replicated Write Request Units (rWRUs, for on-demand tables). 
* Replicated write units include the cost of the streaming infrastructure needed to manage the replication. For on-demand tables in us-east-1 the price is $1.875 per replicated million write units instead of $1.25 per million. For Provisioned it’s $0.000975 per rWCU-hour instead of $0.00065 per WCU-hour. Cross-region data transfer fees do apply.
* Replicated Write Unit charges are incurred in every Region where the item is directly written or replicate written. 
* Writing to a Global Secondary Index (GSI) is considered a local write and uses regular Write Units.
* There is no Reserved Capacity available for rWCUs at this time. Purchasing Reserved Capacity may still be beneficial for tables with GSIs consuming write units.
## What’s the main difference between GTv1 (2017) and GTv2 (2019)?
* DynamoDB has two version of Global Tables. Both are still supported, but we suggest you use GTv2 (2019) or upgrade when you can. All discussion other than this question here refers to GTv2 behaviors.
* With GTv2 the source and target tables are maintained together and kept aligned automatically (for throughput, TTL settings, auto-scaling settings, etc).
* With GTv2 the metadata attributes required to control replication are now hidden, preventing any accidental (or intentional) writing of them which would cause issues with the replication.
* Customer Managed Key (CMK) encryption is only available on GTv2.
* More Regions are supported with GTv2.
* GTv2 lets you add/remove Regions to an existing table.
* GTv2 is generally more cost effective.
## How would I upgrade from Global Tables v1 to v2?
* It’s a push-button on the Console. It’s a live upgrade that should finish in less than an hour.
* https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/V2globaltables_upgrade.html
## How is read and write throughput managed for Global Tables?
* The write capacity must be the same on all table instances across Regions. With GTv2 the write capacity is automatically kept in sync by the GT infrastructure, so a write capacity change to one table replicates to the others. The table must support auto scaling or be in on-demand mode.
* Read capacity is allowed to differ because reads may not be equal across Regions. When adding a global replica to a table the capacity of the source Region is propagated. After creation you can adjust the read capacity, which is not transferred to the other side. Read capacity can be adjusted for each region's global secondary index as well through [provisioned throughput overrides](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_ReplicaGlobalSecondaryIndex.html#DDB-Type-ReplicaGlobalSecondaryIndex-ProvisionedThroughputOverride).
## What Regions does Global Tables support?
* As of today, GTv2 supports more than 32 Regions. The latest list can be seen in the drop-down on the Console when choosing a Region in which to add a replica.
## How are GSIs handled with Global Tables?
* With GTv2, you create a GSI in one Region, and it’s automatically replicated to the other Region(s) as well as automatically backfilled.
* Write capacity must be the same on each index copy, but you can override the read capacity on a per-region basis.
## How do I delete a global table?
* You can delete a replica table the same as any other, which will stop replication to that Region and delete the table copy kept in that Region. You cannot however ask to sever the replication and have copies of the table exist as independent entities.
* There’s also a rule you can’t delete a source table quickly after it’s used to initiate a new Region. If you try you get the error: “Replica cannot be deleted because it has acted as a source Region for new replica(s) being added to the table in the last 24 hours..”
## How are conflicting writes handled with Global Tables?
* Conflicts can arise if applications update the same item in different Regions at about the same time. To help ensure eventual consistency, DynamoDB global tables use a last writer wins reconciliation between concurrent updates, in which DynamoDB makes a best effort to determine the last writer. With this conflict resolution mechanism, all the replicas will agree on the latest update and converge toward a state in which they all have identical data.
There are several ways to avoid conflicts, such as using an IAM policy to only allow writes to the table in one region, 
routing users to only one region and keeping the other as an idle standby, routing odd users to one region and even users to another region, 
avoiding the use of non-idempotent updates such as Bookmark = Bookmark + 1 in favor of static updates such as Bookmark=25.
* For more information, review our best practice guide [on request routing in with global tables](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-global-table-design.prescriptive-guidance.request-routing.html).
## What are best practices for deploying Global Tables? How can I automate deployment?
* In AWS CloudFormation, each global table is controlled by a single stack, in a single Region, regardless of the number of replicas. When you deploy your template, CloudFormation will create/update all replicas as part of a single stack operation. You should not deploy the same `AWS::DynamoDB::GlobalTable` resource in multiple Regions. Doing so will result in errors, and is unsupported. If you deploy your application template in multiple Regions, you can use conditions to only create the resource in a single Region. Alternatively, you can choose to define your `AWS::DynamoDB::GlobalTable` resources in a stack separate from your application stack, and make sure it is only deployed to a single Region.
* https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html
* A DynamoDB table is `AWS::DynamoDB::Table` and a global table is `AWS::DynamoDB::GlobalTable`, which essentially makes them two different resources in regards to CFN. One approach then is to create all tables that might ever be global by using the GlobalTable construct, keep them as standalone tables initially, and later add Regions if needed.
* If you have a regular table and you want to convert it while using CloudFormation, here is the recipe: Set the deletion policy to retain, remove the table from the stack, convert the table to a Global Table in the console, then import the global table as a new resource to the stack.
* Note that cross-account replication is not supported at this time (mid-2024).
## How do I monitor Global Tables?
* Using Amazon CloudWatch you can observe a metric `ReplicationLatency` which tracks the elapsed time between when an item is written to a replica table and when that item appears in another replica in the global table. It’s expressed in milliseconds and is emitted for every source- and destination-Region pair.
* The latencies you will observe depends on many things including the distance between your chosen Regions. It’s common to see latencies in the 0.5 to 2.5 second range for Regions within the same geographic area.
* This is the only CloudWatch metric provided by Global Tables v2.
## How is Time To Live (TTL) handled with Global Tables v2?
* TTL is a feature where you can specify an attribute name whose value (as a number in seconds since epoch) indicates the time of expiration for the item. After that time DynamoDB can delete the item without incurring write costs.
* With Global Table, you configure TTL in one Region, and the setting is auto replicated to the other Region(s).
* When an item is deleted via a TTL rule, that work is performed without consuming Write Units on the source table, but the target table(s) do incur Replicated Write Unit costs. Be aware that if the source and target table have very low Provisioned write capacity, this may cause throttling as the TTL deletes require write capacity.
## How do DynamoDB Streams interact with Global Tables?
* Each global table produces an independent stream based on all its writes, wherever they started from. You can choose to consume the DynamoDB stream in one Region or in all Regions (independently). If you should want local writes processed but not replicated writes, you can add your own `region` attribute to each item that identifies the writing Region, then use a Lambda event filter to only invoke the Lambda for writes in the local Region.
## How do Global Tables handle transactions?
* Transactional operations provide ACID guarantees ONLY within the Region where the write is made originally. Transactions are not supported across Regions in global tables. For example, if you have a global table with replicas in the US East (Ohio) and US West (Oregon) Regions and perform a TransactWriteItems operation in the US East (Ohio) Region, you may observe partially completed transactions in US West (Oregon) Region as changes are replicated. Changes will only be replicated to other Regions once they have been committed in the source Region.
## How do Global Tables interact with the DynamoDB Accelerator cache (DAX)?
* Global Tables “write around” DAX by updating DynamoDB directly, so DAX will not be aware it’s holding stale data. The DAX cache will only be refreshed when the cache’s TTL expires.
## Do tags on tables propagate?
* No, they do not automatically propagate.
## Should I backup tables in all Regions or just one?
* The answer depends on the purpose of the backup. If it’s to ensure data durability, that’s a feature intrinsic to the DynamoDB service. If it’s about keeping a snapshot for historic records (such as for regulatory requirements) then backing up in one Region should suffice. The backed up data can be replicated to multiple Regions via AWS Backup. If it’s about recovering erroneously deleted or modified data, then PITR in one Region should suffice.

## What’s the best practice for using Global Tables as part of handling a potential Region outage?
* Have (or be able to quickly create) independent copies of your execution stack in alternative Regions, each accessing its local DynamoDB endpoint. Use Route53 or Global Accelerator to route to the nearest healthy Region, or have the client aware of the multiple endpoints it might use. Use health checks in each Region that will be able to determine reliably if there’s any issue with the stack, including if DynamoDB is degraded. For example, don’t just ping that the DynamoDB endpoint is up, actually do a call that ensures a full successful database flow. Should the health check fail, traffic can route to other Regions (by updating the DNS entry with Route53, by having Global Accelerator route differently, or by having the client choose a different endpoint). Global Tables have a good RPO (recovery point objective) because the data is continuously syncing and a good RTO (recovery time objective) because both Regions always keep a table ready for both read and write traffic.
* Note that DynamoDB is a core service on which other services frequently build their control plane operations, thus it’s unlikely you’ll encounter a scenario where DynamoDB has degraded service in a Region while other services are unimpacted.
* Read [Evacuating a Region with global tables](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-global-table-design.prescriptive-guidance.evacuation.html) in our developer docs for more information.
