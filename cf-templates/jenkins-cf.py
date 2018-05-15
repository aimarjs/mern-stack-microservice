from troposphere import Ref, Template, Parameter, Output, Join, GetAtt, Base64
import troposphere.ec2 as ec2

t = Template()

sg = ec2.SecurityGroup("MernSg")
sg.GroupDescription = "Allow access to ports 8080 and 22 to the web server"
sg.SecurityGroupIngress = [
    ec2.SecurityGroupRule(IpProtocol = "tcp", FromPort = "22", ToPort = "22", CidrIp = "0.0.0.0/0"),
    ec2.SecurityGroupRule(IpProtocol = "tcp", FromPort = "8080", ToPort = "8080", CidrIp = "0.0.0.0/0"),
]

t.add_resource(sg)

keypair = t.add_parameter(Parameter(
    "KeyName",
    Description = "Name of the SSH key pair that will be used to access the instance",
    Type = "String"
))
instance = ec2.Instance("Jenkins")
instance.ImageId = "ami-f90a4880"
instance.InstanceType = "t2.micro"
instance.SecurityGroups = [Ref(sg)]
instance.KeyName = Ref(keypair)
ud = Base64(Join("\n",
    [
        "#!/bin/bash",
        "sudo apt-get install -y python-minimal",
    ]))

instance.UserData = ud

t.add_resource(instance)

t.add_output(Output(
    "InstanceAccess",
    Description = "Command to use to access the instance by SSH",
    Value = Join("", ["ssh -i ~/.ssh/MernKey.pem ubuntu@", GetAtt(instance, "PublicDnsName")])
))
t.add_output(Output(
    "WebURL",
    Description = "URL of web server",
    Value = Join("", ["http://", GetAtt(instance, "PublicDnsName"),":8080"])
))

print(t.to_json())
