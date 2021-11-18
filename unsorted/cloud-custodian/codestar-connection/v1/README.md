** CodeStar Connection

The AWS::CodeStarConnections::Connection resource can be used to connect external source providers with services like AWS CodePipeline.

Only the following external sources are supported:

- Bitbucket
- GitHub
- GitHubEnterpriseServer

A connection created through CloudFormation is in PENDING status by default. You can make its status AVAILABLE by updating the connection in the console.

**Resources**

The product.template.yaml creates the following resources:

- CodeStarConnection - The CodeStar Connection resource

Once the CloudFormation template has successfully been created, perform the following steps to complete the connection:

1. Navigate to the CodePipeline Console. On the left-hand menu, click "Settings" and then "Connections". You should see your CodeStar Connection in a "Pending" status.
2. Click the radio button next to your connection, and click "Update pending connection". This should open a window for you to connect your third party repository provider to your connection.
3. Complete the steps required in the pop up window.
4. Once complete, your connection should show as "Available" in the CodePipeline console.
