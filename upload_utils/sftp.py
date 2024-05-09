import errno
import paramiko
import os

def create_remote_sftp_dir_recursively(sftp_client, remote_dir):
    """
    Creates a directory and its parents recursively on the SFTP server,
    always relative to the root directory.
    """
    if not isinstance(sftp_client,paramiko.SFTPClient):
        raise ValueError("sftp_client must be an instance of paramiko.SFTPClient")
    
    if remote_dir.startswith('/'):  # Handle absolute paths
        path_components = remote_dir.split('/')[1:]  # Split and remove leading '/'
    else:  # don't support path not starting with '/' to prevent mistakes like changed to another directory first
        raise ValueError("Only absolute paths are supported")
        #path_components = remote_dir.split('/')

    current_dir = '/'  # Start from the root directory
    for component in path_components:
        if component == '':  # Skip empty components
            continue
        current_dir = os.path.join(current_dir, component)
        try:
            stat=sftp_client.stat(current_dir)
            #if not stat.S_ISDIR(stat.st_mode):
            #    sftp_client.mkdir(current_dir)
        except IOError as e:
            if e.errno == errno.ENOENT:
                sftp_client.mkdir(current_dir)
            else:
                raise e
            


# does not check if it is directory yet
def file_exists(sftp_client, remote_path):
    """
    Creates a directory and its parents recursively on the SFTP server,
    always relative to the root directory.
    """
    if not isinstance(sftp_client,paramiko.SFTPClient):
        raise ValueError("sftp_client must be an instance of paramiko.SFTPClient")
    
    if remote_path.startswith('/'):  # Handle absolute paths
        path_components = remote_path.split('/')[1:]  # Split and remove leading '/'
    else:  # don't support path not starting with '/' to prevent mistakes like changed to another directory first
        raise ValueError("Only absolute paths are supported")

    try:
        sftp_client.stat(remote_path)
        return True
    except IOError as e:
        if e.errno == errno.ENOENT:
            return False
        else:
            raise e
