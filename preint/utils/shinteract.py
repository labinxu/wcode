import paramiko  
import getpass

class ShInteractor():
    def __init__(self, hostname, username, password=None):
        self.username = username
        self.password = password
        self.hostname = hostname
        #### test code
        self.hostname = 'musxeris016.imu.intel.com'
        self.port = 22   
        self.username = 'labinxux'   
        self.password = 'Mar@0303'
        if not self.password:
            self.password = getpass.getpass("Password:")
        ########end
        paramiko.util.log_to_file('paramiko.log')  
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.login()
        
    def login(self):
        self.ssh.connect(self.hostname, self.port, self.username, self.password)
        
        stdin,stdout,stderr = self.ssh.exec_command('bash')  

    def execCommand(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return(stdin, stdout, stderr)

    def close():
        self.ssh.close()


    def transFile(self, localfile, remotefile):
        print("Upload file %s to %s" % (localfile, remotefile))
        try:
            t = paramiko.Transport((self.hostname, int(self.port)))
            t.connect(username=self.username, password=self.password)
            sftp=paramiko.SFTPClient.from_transport(t)
            sftp.put(localfile, remotefile)
        except Exception as e:
            print(e)
        finally:
            t.close()
