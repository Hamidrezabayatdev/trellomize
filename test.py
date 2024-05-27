import unittest
import main

class TestMyProgram(unittest.TestCase):
    def test_getHashedPassfunc(self):
        passExample="testpassword"
        hashedPass = main.get_hashed_password(passExample)
        self.assertTrue(hashedPass)
    def test_checkPassfunc(self):
        passExample = "testpassword"
        hashedPass = main.get_hashed_password(passExample)
        self.assertTrue(main.check_password(passExample, hashedPass))
    def test_checkmail(self):
        mailExample = "myemail@gmail.com"
        self.assertTrue(main.checkEmail(mailExample))

        