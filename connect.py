import paramiko
import logger
logname = logger.get_logger(__name__)
class SSHClient:
    def __init__(self, server_ip, username, password):
        self.server_ip = server_ip
        self.username = username
        self.password = password

    def exec_command(self, cmd):
        """this method use to connect remote ssh machine and execute commands :param cmd::return:"""
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            client.connect(self.server_ip, username=self.username, password=self.password)
            _stdin, _stdout, _stderr = client.exec_command(cmd)
            result = _stdout.read().decode()
            return result
        except Exception as errinfo:
            print("error found")
            print(f"{errinfo}")

if __name__ == "__main__":
   connection = SSHClient("192.168.0.111", "root", "Winteck@2024")
