import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";

const stack = pulumi.getStack();

// Create an AWS resource (S3 Bucket)
const bucket = new aws.s3.Bucket("obpy");

// Export the name of the bucket
export const bucketName = bucket.id;

const obpyHandlerRole = new aws.iam.Role("obpyHandlerRole", {
  assumeRolePolicy: {
    Version: "2012-10-17",
    Statement: [
      {
        Action: "sts:AssumeRole",
        Principal: {
          Service: "lambda.amazonaws.com",
        },
        Effect: "Allow",
        Sid: "",
      },
    ],
  },
});

const obpyHandlerPolicy = new aws.iam.Policy("obpyHandlerPolicy", {
  policy: {
    Version: "2012-10-17",
    Statement: [
      {
        Effect: "Allow",
        Action: [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ],
        Resource: "*",
      },
      {
        Action: ["s3:GetObject"],
        Effect: "Allow",
        Resource: [pulumi.interpolate`${bucket.arn}/*`],
      },
    ],
  },
});

new aws.iam.PolicyAttachment("obpyHandlerRoleAttachment", {
  roles: [obpyHandlerRole.name],
  policyArn: obpyHandlerPolicy.arn,
});

const obpyHandlerFunc = new aws.lambda.Function("obpyHandlerFunc", {
  code: new pulumi.asset.AssetArchive({
    ".": new pulumi.asset.FileArchive("./app"),
  }),
  runtime: "python3.9",
  handler: "lambda_function.lambda_handler",
  role: obpyHandlerRole.arn,
});

bucket.onObjectCreated("obpyHandler", obpyHandlerFunc);

const obpyTable = new aws.dynamodb.Table("obpyTable", {
  attributes: [
    {
      name: "ExchangeSymbol",
      type: "S",
    },
    {
      name: "TsStart",
      type: "N",
    },
  ],
  billingMode: "PAY_PER_REQUEST",
  hashKey: "ExchangeSymbol",
  rangeKey: "TsStart",
  readCapacity: 0,
  tags: {
    Environment: stack,
    Name: "obpy-table",
  },
  writeCapacity: 0,
});

export const obpyTableName = obpyTable.id;
