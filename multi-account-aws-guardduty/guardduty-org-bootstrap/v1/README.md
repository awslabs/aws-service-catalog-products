# GuardDuty Org master Bootstrap

## What will it do

**This product will:**

- Creates an IAM role in the Org Master Account to enable assumption from ALL spoke Accounts within the Organization
- The role allows a Describe-Account Action so that the email address can be taken to enable GD Detector Creation

## Where Can I use it

**You should run this Product in:**

- Organization Master

## Does it have any Dependencies

**This Product requires:**

- None

## Do other Products have a dependency on this

**Products which require an output of this Product are:**

- Security-GuardDutySpoke Product relies on this being deployed
