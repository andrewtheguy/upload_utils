import os
import unittest

from upload_utils.onedrive_utils import OneDriveUtils


class TestUploadOneDrive(unittest.TestCase):
    def setUp(self):
        self.upload_file = 'tests/尖峰時刻/2024年05月07日 美國認為中國錯誤的解讀聯合國２７５８號決議案, 您認為呢, .txt'
        self.upload_empty_file = 'tests/尖峰時刻/2024年05月07日 美國認為中國錯誤的解讀聯合國２７５８號決議案, 您認為呢, 2.txt'
        if not os.path.isfile(self.upload_file):
            raise FileNotFoundError('File not found')
        if not os.path.isfile(self.upload_empty_file):
            raise FileNotFoundError('File not found')
        self.one_drive = OneDriveUtils(os.environ['ONEDRIVE_CLIENT_ID'])
        self.one_drive.test_connection()

    def test_upload(self):
        self.assertEqual(self.one_drive.file_exists('hfghfghfghfghfg/hfghjfjfghjf.txt'), False)
        #self.assertEqual(self.one_drive.file_exists('/hfghfghfghfghfg/hfghjfjfghjf.txt'), False)
        self.assertEqual(self.one_drive.file_exists(self.upload_file), True)
        self.one_drive.upload(self.upload_file,self.upload_file,skip_if_exists=True)
        self.assertEqual(self.one_drive.file_exists(self.upload_file), True)
        self.one_drive.upload(self.upload_empty_file,self.upload_empty_file,skip_if_exists=False)
        self.assertEqual(self.one_drive.file_exists(self.upload_empty_file), True)
        

if __name__ == '__main__':
    unittest.main()