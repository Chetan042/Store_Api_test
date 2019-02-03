from models.user import UserModel
from tests.unit.unit_base_test import UnitTestBase


class UserTest(UnitTestBase):
    def test_create_user(self):
        user = UserModel('test', 'abcd')
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.password, 'abcd')
