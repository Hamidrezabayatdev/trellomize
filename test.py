import unittest
import main
import logging

#logging :
#logger3 = logging.getLogger("test.py")

#logging.basicConfig(filename="user_actions.log",
                    #filemode='a',
                    #format='%(asctime)s, %(name)s %(levelname)s %(message)s',
                    #datefmt="%Y-%m-%d %H:%M:%S",
                    #level=logging.INFO)
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
    def test_checkInExistingUser(self):
        mydictlist = [{"key11":"value11", "key12":"value12"}, {"key11":"value21" , "key12":"value22"}]
        self.assertEqual(1,main.checkInUsers("value21", "key11",mydictlist))
    def test_checkInNonExistingUser(self):
        mydictlist = [{"key11":"value11", "key12":"value12"}, {"key11":"value21" , "key12":"value22"}]
        self.assertFalse(main.checkInUsers("value33","key11",mydictlist))
    def test_checkInExistingProj(self):
        mydictlist = [{"key11":"value11", "key12":"value12"}, {"key11":"value21" , "key12":"value22"}]
        self.assertEqual(1,main.checkInProjects("value21", "key11",mydictlist))
    def test_checkInNonExistingProj(self):
        mydictlist = [{"key11":"value11", "key12":"value12"}, {"key11":"value21" , "key12":"value22"}]
        self.assertFalse(main.checkInProjects("value33","key11",mydictlist))
    
    
        

        