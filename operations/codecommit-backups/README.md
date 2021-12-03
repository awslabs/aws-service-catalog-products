# CodeCommit backups

This solution backs up CodeCommit repositories to an S3 bucket in the event of a commit to the main/Main or master/Master branch of a codecommit repo. If setting parameter pScheduleBackups to 'true' will also create  a schedule for backups (daily at 12PM by default, via a Cloudwatch Rule with schedule and a Lambda function)

## Description

* Deploys a single product in the tooling account that will trigger Cloudwatch events rule if a commit is made to a designated branch of all repositories in the designated AWS account
* Triggers a Codebuild project
* Clones the repo and exports to an S3 bucket
