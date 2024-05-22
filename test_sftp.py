import paramiko

from upload_utils.sftp import file_exists


def connect_ssh_client(ssh_client):
    # remote server credentials
    host = "10.22.33.20"
    username = "andrew"
    password = "qwertasdfg"
    port = '2022'
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host,port=port,username=username,password=password, look_for_keys=False)


def sftp_file_exists(remote_path):
    with paramiko.SSHClient() as ssh_client:
        connect_ssh_client(ssh_client)

        # create an SFTP client object
        with ssh_client.open_sftp() as sftp:
            #create_remote_sftp_dir_recursively(sftp_client=sftp, remote_dir="/chafa/trimmed/chilo")
            return file_exists(sftp_client=sftp, remote_path=remote_path)

print(sftp_file_exists("/test.txt"))
print(sftp_file_exists("/test_upload.py"))