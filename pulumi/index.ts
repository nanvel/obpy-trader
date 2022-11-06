import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const stack = pulumi.getStack();
const config = new pulumi.Config();

// Create an AWS resource (S3 Bucket)
const bucket = new aws.s3.Bucket("obpy");

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
        Effect: "Allow",
        Action: ["dynamodb:PutItem"],
        Resource: pulumi.interpolate`${obpyTable.arn}`,
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

export const bucketName = bucket.id;
export const tableName = obpyTable.id;

// server

const ami = aws.ec2
  .getAmi({
    filters: [
      {
        name: "name",
        values: ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"],
      },
    ],
    owners: ["099720109477"],
    mostRecent: true,
  })
  .then((result) => result.id);

const group = new aws.ec2.SecurityGroup("obpySecurityGroup", {
  ingress: [
    { protocol: "tcp", fromPort: 80, toPort: 80, cidrBlocks: ["0.0.0.0/0"] },
    { protocol: "tcp", fromPort: 443, toPort: 443, cidrBlocks: ["0.0.0.0/0"] },
    { protocol: "tcp", fromPort: 22, toPort: 22, cidrBlocks: ["0.0.0.0/0"] },
  ],
  egress: [
    { protocol: "-1", fromPort: 0, toPort: 0, cidrBlocks: ["0.0.0.0/0"] },
  ],
});

const keyName = config.require("keyName");

const server = new aws.ec2.Instance("obpyServer", {
  tags: { Name: "obpyServer" },
  instanceType: aws.ec2.InstanceType.T2_Nano,
  vpcSecurityGroupIds: [group.id],
  keyName: keyName,
  ami: ami,
});

const domainName = config.require("domain");

const zoneId = aws.route53
  .getZone({
    name: domainName.split(".").slice(1).join(".") + ".",
  })
  .then((selected) => selected.zoneId);

const www = new aws.route53.Record("obpyWww", {
  zoneId: zoneId,
  name: domainName,
  type: "A",
  ttl: 300,
  records: [server.publicIp],
});

export const serverIp = server.publicIp;

// server user

const serverUser = new aws.iam.User("obpyServerUser", {
  path: "/system/",
});

const lbAccessKey = new aws.iam.AccessKey("lbAccessKey", {
  user: serverUser.name,
});

const userPolicyStatement = pulumi.interpolate`{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": ["dynamodb:Query"],
      "Effect": "Allow",
      "Resource": "${obpyTable.arn}"
    },
    {
      "Action": ["s3:GetObject"],
      "Effect": "Allow",
      "Resource": ["${bucket.arn}/*"]
    }
  ]
}`;

const serverUserPolicy = new aws.iam.UserPolicy("serverUserPolicy", {
  user: serverUser.name,
  policy: userPolicyStatement,
});
