# CodeBuild SNS Notifier

This solution creates an SNS notification for CodeBuild Jobs in the event that a build fails or is stopped.
## Description
* Deploys a single product in the tooling account that will trigger Cloudwatch events rule if a commit is made to a designated branch of all repositories in the designated AWS account
* Product consists of CloudWatch Event rule that is triggered for a CodeBuild Build job in the event that a build fails or is stopped
* SNS Topic and subscripton is created and Notification sent via E-mail when event occurs
