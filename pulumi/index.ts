import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";

// Create an AWS resource (S3 Bucket)
const bucket = new aws.s3.Bucket("obpy");

// Export the name of the bucket
export const bucketName = bucket.id;


// const docsHandlerRole = new aws.iam.Role("docsHandlerRole", {
//     assumeRolePolicy: {
//        Version: "2012-10-17",
//        Statement: [{
//           Action: "sts:AssumeRole",
//           Principal: {
//              Service: "lambda.amazonaws.com",
//           },
//           Effect: "Allow",
//           Sid: "",
//        }],
//     },
//  });
//  new aws.iam.RolePolicyAttachment("zipTpsReportsFuncRoleAttach", {
//     role: docsHandlerRole,
//     policyArn: aws.iam.ManagedPolicies.AWSLambdaExecute,
//  });
//
//
// const docsHandlerFunc = new aws.lambda.Function("docsHandlerFunc", {
//     // Upload the code for our Lambda from the "./app" directory:
//     code: new pulumi.asset.AssetArchive({
//        ".": new pulumi.asset.FileArchive("./app"),
//     }),
//     runtime: "nodejs12.x",
//     role: docsHandlerRole.arn,
//  });
//
//
// bucket.onObjectCreated("docsHandler", docsHandlerFunc);
