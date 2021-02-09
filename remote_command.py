"""SSH remote command, file upload and file download functions.
"""

# Global imports
import configparser

# 3rd party imports
import paramiko

# Local imports
from lib.helper import debug


# -----------------------------------------------------------------------------
def ssh_run_remote_command(host, username, password, cmd):
    """Use SSH to run a command on a remote host.

    :param host: Host name or IP address
    :param username: SSH user
    :param password: SSH password
    :param cmd: Command to run
    :return: The result of the command
    """

    debug(f"{host=}, {username=}, {password=}, {cmd=}")

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=username, password=password)
    _stdin, stdout, stderr = ssh_client.exec_command(cmd)

    out = stdout.read().decode().strip()
    error = stderr.read().decode().strip()

    # print(f"{out=}\n{error=}")

    if error:
        raise Exception("ERROR: {}".format(error))
    ssh_client.close()

    return out


# -----------------------------------------------------------------------------
def ssh_upload_file(host, username, password, localpath, remotepath) -> None:
    """Use SSH to upload a file to a remote host.

    :param host: Host name or IP address
    :param username: SSH user
    :param password: SSH password
    :param localpath: Path to the local source file
    :param remotepath: Path to the remote destinatio file
    """

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=username, password=password)
    ftp_client = ssh_client.open_sftp()
    ftp_client.put(localpath, remotepath)
    ftp_client.close()
    ssh_client.close()


# -----------------------------------------------------------------------------
def ssh_download_file(host, username, password, remotepath, localpath) -> None:
    """Use SSH to download a file from a remote host.

    :param host: Host name or IP address
    :param username: SSH user
    :param password: SSH password
    :param remotepath: Path to the remote source file
    :param localpath: Path to the local destinatio file
    """

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=username, password=password)
    ftp_client = ssh_client.open_sftp()
    ftp_client.get(remotepath, localpath)
    ftp_client.close()
    ssh_client.close()


# =============================================================================
if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read("config.ini")

    hostname = config["DEFAULT"]["ssh_host"]
    user = config["DEFAULT"]["ssh_user"]
    passwd = config["DEFAULT"]["ssh_password"]

    ssh_upload_file(hostname, user, passwd, "README.md", "test.md")
    ret = ssh_run_remote_command(hostname, user, passwd, "ls")
    print(ret)


