import base64

import unittest2
from boto.kms.exceptions import InvalidCiphertextException
from mock import patch

from cfn_sphere.aws.kms import KMS
from cfn_sphere.exceptions import InvalidEncryptedValueException


class KMSTests(unittest2.TestCase):
    @patch('cfn_sphere.aws.kms.kms.connect_to_region')
    def test_decrypt_value(self, kms_mock):
        kms_mock.return_value.decrypt.return_value = {'Plaintext': b'decryptedValue'}

        self.assertEqual('decryptedValue', KMS().decrypt("ZW5jcnlwdGVkVmFsdWU="))
        kms_mock.return_value.decrypt.assert_called_once_with(base64.b64decode("ZW5jcnlwdGVkVmFsdWU=".encode()))

    @patch('cfn_sphere.aws.kms.kms.connect_to_region')
    def test_decrypt_value_with_unicode_char(self, kms_mock):
        kms_mock.return_value.decrypt.return_value = {'Plaintext': b'(\xe2\x95\xaf\xc2\xb0\xe2\x96\xa1\xc2\xb0\xef\xbc\x89\xe2\x95\xaf\xef\xb8\xb5 \xe2\x94\xbb\xe2\x94\x81\xe2\x94\xbb'}

        self.assertEqual(u'(\u256f\xb0\u25a1\xb0\uff09\u256f\ufe35 \u253b\u2501\u253b', KMS().decrypt("KOKVr8Kw4pahwrDvvInila/vuLUg4pS74pSB4pS7"))
        kms_mock.return_value.decrypt.assert_called_once_with(base64.b64decode("KOKVr8Kw4pahwrDvvInila/vuLUg4pS74pSB4pS7".encode()))


    @patch('cfn_sphere.aws.kms.kms.connect_to_region')
    def test_invalid_base64(self, kms_mock):
        with self.assertRaises(InvalidEncryptedValueException):
            KMS().decrypt("asdqwda")

    @patch('cfn_sphere.aws.kms.kms.connect_to_region')
    def test_invalid_kms_key(self, kms_mock):
        kms_mock.return_value.decrypt.side_effect = InvalidCiphertextException("400", "Bad Request")

        with self.assertRaises(InvalidEncryptedValueException):
            KMS().decrypt("ZW5jcnlwdGVkVmFsdWU=")
