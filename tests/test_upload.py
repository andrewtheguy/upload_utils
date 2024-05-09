import os
from pathlib import Path
import random
import secrets
import string
import tempfile
import unittest

from upload_utils.onedrive_utils import OneDriveUtils


class TestUploadOneDrive(unittest.TestCase):
    def setUp(self):

        self.one_drive = OneDriveUtils(os.environ['ONEDRIVE_CLIENT_ID'])
        self.one_drive.test_connection()

    def run(self, result=None):
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.tmpdirname = tmpdirname
            self.destdirname = "test_python_upload"
            
            
            super(TestUploadOneDrive, self).run(result)


    def test_upload(self):
        upload_file = os.path.join(self.tmpdirname,secrets.token_hex(16) + ".txt")
        dest_path = '/'.join([self.destdirname,os.path.basename(upload_file)])    
        self.assertEqual(self.one_drive.file_exists(dest_path), False)
        file_content = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        with open(upload_file, 'w') as f:
            f.write(file_content)
        self.one_drive.upload(upload_file,dest_path,skip_if_exists=False)
        self.assertEqual(self.one_drive.file_exists(dest_path), True)

    def test_upload_empty(self):
        upload_empty_file = os.path.join(self.tmpdirname,secrets.token_hex(16) + "_empty.txt")
        dest_path = '/'.join([self.destdirname,os.path.basename(upload_empty_file)])    
        self.assertEqual(self.one_drive.file_exists(dest_path), False)
        Path(upload_empty_file).touch()
        self.one_drive.upload(upload_empty_file,dest_path,skip_if_exists=False)
        self.assertEqual(self.one_drive.file_exists(dest_path), True)

    def test_upload_with_forward_slash_begining(self):
        upload_file = os.path.join(self.tmpdirname,secrets.token_hex(16) + ".txt")
        dest_path = '/'.join([self.destdirname,os.path.basename(upload_file)])  
        dest_path_with_slash = '/'+dest_path
        self.assertEqual(self.one_drive.file_exists(dest_path), False)
        self.assertEqual(self.one_drive.file_exists(dest_path_with_slash), False)
        file_content = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        with open(upload_file, 'w') as f:
            f.write(file_content)
        self.one_drive.upload(upload_file,dest_path_with_slash,skip_if_exists=False)
        self.assertEqual(self.one_drive.file_exists(dest_path), True)
        self.assertEqual(self.one_drive.file_exists(dest_path_with_slash), True)

    def test_download(self):
        upload_file = os.path.join(self.tmpdirname,secrets.token_hex(16) + ".txt")
        dest_path = '/'.join([self.destdirname,os.path.basename(upload_file)])    
        self.assertEqual(self.one_drive.file_exists(dest_path), False)
        file_content = ''.join(random.choices(string.ascii_letters + string.digits, k=327680+2))
        with open(upload_file, 'w') as f:
            f.write(file_content)
        self.one_drive.upload(upload_file,dest_path,skip_if_exists=False)
        self.assertEqual(self.one_drive.file_exists(dest_path), True)

        download_dest_file = os.path.join(self.tmpdirname,secrets.token_hex(16) + "_download.txt")
        self.one_drive.download(dest_path,download_dest_file)
        with open(download_dest_file, 'r') as f:
            download_dest_file_file_content = f.read()

        self.assertEqual(file_content,download_dest_file_file_content)    


    def test_no_override_exists(self):
        upload_file = os.path.join(self.tmpdirname,secrets.token_hex(16) + ".txt")
        dest_path = '/'.join([self.destdirname,os.path.basename(upload_file)])    
        self.assertEqual(self.one_drive.file_exists(dest_path), False)
        file_content = ''.join(random.choices(string.ascii_letters + string.digits, k=16*1024+2))
        with open(upload_file, 'w') as f:
            f.write(file_content)
        self.one_drive.upload(upload_file,dest_path,skip_if_exists=False)
        self.assertEqual(self.one_drive.file_exists(dest_path), True)

        file_content2 = ''.join(random.choices(string.ascii_letters + string.digits, k=16*1024+3))

        self.assertNotEqual(file_content,file_content2)
        
        with open(upload_file, 'w') as f:
            f.write(file_content2)
        self.one_drive.upload(upload_file,dest_path,skip_if_exists=True)
        self.assertEqual(self.one_drive.file_exists(dest_path), True)

        download_dest_file = os.path.join(self.tmpdirname,secrets.token_hex(16) + "_download.txt")
        self.one_drive.download(dest_path,download_dest_file)
        with open(download_dest_file, 'r') as f:
            download_dest_file_file_content = f.read()

        self.assertEqual(file_content,download_dest_file_file_content)
        self.assertNotEqual(file_content2,download_dest_file_file_content)



    def test_override_exists(self):
        upload_file = os.path.join(self.tmpdirname,secrets.token_hex(16) + ".txt")
        dest_path = '/'.join([self.destdirname,os.path.basename(upload_file)])    
        self.assertEqual(self.one_drive.file_exists(dest_path), False)
        file_content = ''.join(random.choices(string.ascii_letters + string.digits, k=16*1024*2))
        with open(upload_file, 'w') as f:
            f.write(file_content)
        self.one_drive.upload(upload_file,dest_path,skip_if_exists=False)
        self.assertEqual(self.one_drive.file_exists(dest_path), True)

        file_content2 = ''.join(random.choices(string.ascii_letters + string.digits, k=16*1024+3))

        self.assertNotEqual(file_content,file_content2)
        
        with open(upload_file, 'w') as f:
            f.write(file_content2)
        self.one_drive.upload(upload_file,dest_path,skip_if_exists=False)
        self.assertEqual(self.one_drive.file_exists(dest_path), True)

        download_dest_file = os.path.join(self.tmpdirname,secrets.token_hex(16) + "_download.txt")
        self.one_drive.download(dest_path,download_dest_file)
        with open(download_dest_file, 'r') as f:
            download_dest_file_file_content = f.read()

        self.assertEqual(file_content2,download_dest_file_file_content)
        self.assertNotEqual(file_content,download_dest_file_file_content)
                

if __name__ == '__main__':
    unittest.main()