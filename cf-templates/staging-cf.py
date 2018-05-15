from troposphere import Ref, Template, Parameter, Output, Join, GetAtt, Base64
from troposphere.iam import InstanceProfile, PolicyType as IAMPolicy, Role
from awacs.aws import Action, Allow, Policy, Principal, Statement
from awacs.sts import AssumeRole
import troposphere.ec2 as ec2

t = Template()

sg = ec2.SecurityGroup("MernSg")
sg.GroupDescription = "Allow access to ports 80, 443 and 22 to the web server"
sg.SecurityGroupIngress = [
    ec2.SecurityGroupRule(IpProtocol = "tcp", FromPort = "22", ToPort = "22", CidrIp = "0.0.0.0/0"),
    ec2.SecurityGroupRule(IpProtocol = "tcp", FromPort = "80", ToPort = "80", CidrIp = "0.0.0.0/0"),
    ec2.SecurityGroupRule(IpProtocol = "tcp", FromPort = "443", ToPort = "443", CidrIp = "0.0.0.0/0"),

]

t.add_resource(sg)

keypair = t.add_parameter(Parameter(
    "KeyName",
    Description = "Name of the SSH key pair that will be used to access the instance",
    Type = "String"
))
instance = ec2.Instance("Staging")
instance.ImageId = "ami-f90a4880"
instance.InstanceType = "t2.micro"
instance.SecurityGroups = [Ref(sg)]
instance.KeyName = Ref(keypair)
ud = Base64(Join("\n",
    [
        "#!/bin/bash",
        "sudo apt-get install -y python-minimal",
        "sudo apt-get install -y ruby"
    ]))

instance.UserData = ud

principal = Principal("Service", ["ec2.amazonaws.com"])
statement = Statement(Effect=Allow, Action=[AssumeRole], Principal=principal)
policy = Policy(Statement=[statement])
role = Role("Role", AssumeRolePolicyDocument=policy)
t.add_resource(role)

t.add_resource(InstanceProfile("InstanceProfile", Path="/", Roles=[Ref("Role")]))

t.add_resource(IAMPolicy("Policy", PolicyName="AllowS3", PolicyDocument=Policy(Statement=[Statement(Effect=Allow, Action=[Action("s3", "*")], Resource=["*"])]), Roles=[Ref("Role")]))

instance.IamInstanceProfile = Ref("InstanceProfile")

t.add_resource(instance)

t.add_output(Output(
    "InstanceAccess",
    Description = "Command to use to access the instance by SSH",
    Value = Join("", ["ssh -i ~/.ssh/LampKey.pem ubuntu@", GetAtt(instance, "PublicDnsName")])
))
t.add_output(Output(
    "WebURL",
    Description = "URL of web server",
    Value = Join("", ["http://", GetAtt(instance, "PublicDnsName")])
))

print(t.to_json())
