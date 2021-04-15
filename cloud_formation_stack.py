import time
import sys

class CloudFormationStack:
    def __init__(self, client, stack_name):
        self.client = client
        self.stack_name = stack_name


    def deploy_url(self):
        stacks = self.client.describe_stacks(StackName=self.stack_name)['Stacks']
        url = stacks[0]['Outputs'][0]['OutputValue']
        return url


    def exists(self):
        stack_list = self.client.describe_stacks()["Stacks"]
        stack_exists = False
        for stack in stack_list:
            if self.stack_name == stack["StackName"]:
                print("Stack " + self.stack_name + " already exists.")
                stack_exists = True
        return stack_exists


    def delete(self):
        print("Calling Delete Stack API for " + self.stack_name)
        self.client.delete_stack(StackName=self.stack_name)
        self.check_status()


    def create(self, template_url):
        print("Calling CREATE_STACK method to create: " + self.stack_name)
        result = self.client.create_stack(StackName=self.stack_name, DisableRollback=True, TemplateURL=template_url, Capabilities=["CAPABILITY_IAM"])
        stack_status = self.check_status()
        if stack_status == "CREATE_COMPLETE":
            print("Stack " + self.stack_name + " created successfully.")
        else:
            print("Failed to create stack " + self.stack_name)
            sys.exit(1)
        return result


    def check_status(self):
        stacks = self.client.describe_stacks(StackName=self.stack_name)["Stacks"]
        stack = stacks[0]
        stack_status = stack["StackStatus"]
        print("Current status of stack " + self.stack_name + ": " + stack_status)
        error_cnt = 0
        for loop in range(1, 9999):
            if "IN_PROGRESS" in stack_status:
                print("Waiting for status update(" + str(loop) + ")...", end="\r")
                time.sleep(1)
                try:
                    stacks = self.client.describe_stacks(StackName=self.stack_name)["Stacks"]
                    error_cnt = 0
                except:
                    error_cnt += 1
                    print(" ")
                    print("Error getting status for Stack " + self.stack_name + "!")
                    print("Retry status check (" + str(error_cnt) + ")...")
                    if error_cnt > 4:
                        stack_status = "STACK_DELETED"
                        break
                stack = stacks[0]
                if stack["StackStatus"] != stack_status:
                    stack_status = stack["StackStatus"]
                    print(" ")
                    print("Updated status of stack " + self.stack_name + ": " + stack_status)
            else:
                break
        return stack_status
