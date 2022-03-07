# Account Vending
This solution is to be deployed using the service catalog tools.  Once deployed it will allow you to create new AWS
accounts using the AWS Organizations API or via the AWS Control Tower Account Factory (using AWS Service Catalog).

## Getting started
Before you can create accounts you will need to provision the prereqs-puppet-account stack into the account where you
installed the service catalog tools.  You will then need to follow either the AWS Control Tower or AWS Orgnizations
route below depending on how you would like to create accounts.

### AWS Control Tower
If you are planning on using AWS Control Tower you will need to have that enabled before this works.  Once you have it
enabled you should provision the prereqs-controltower-account stack within the account where you have Control Tower
enabled.

Once you have that provisioned you can provision the product created by the account-vending-with-aws-control-tower 
template.

### AWS Organizations
If you are planning on using AWS Control Tower you will need to have that enabled before this works.  Once you have it
enabled you should provision the prereqs-controltower-account stack within the account where you have Control Tower
enabled.

Once you have that provisioned you can provision the product created by the account-vending-with-aws-organizations 
template.