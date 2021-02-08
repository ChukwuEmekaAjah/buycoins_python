from buycoins_client import Auth
import unittest

class TestAuthMethods(unittest.TestCase):

    def test_invalid_secret_key_setup(self):
        """
            Should throw an exception for invalid secret key
        """
        try:
            Auth.setup("name",3)
        except Exception as e:
            self.assertEqual(str(e), "Invalid secret key. Secret key should be a string")

    def test_invalid_public_key_setup(self):
        """
            Should throw an exception for invalid secret key
        """
        try:
            Auth.setup(1,3)
        except Exception as e:
            self.assertEqual(str(e), "Invalid public key. Public key should be a string")

    def test_valid_auth_setup(self):
        """
            Should return public and secret key as username and password auth
        """
        auth = Auth.setup("buycoins", "africa")

        self.assertEqual(auth, True)



if __name__ == '__main__':
    unittest.main()
