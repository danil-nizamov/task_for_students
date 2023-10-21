import unittest
from contacts_manager_impl import ContactsManagerImpl


class LevelTests(unittest.TestCase):

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.manager = ContactsManagerImpl()

    def test1_1_simpleOperationsOrder(self):
        self.assertTrue(self.manager.set_record(1, "John", "+3581"))
        self.assertFalse(self.manager.set_record(1, "Jake", "+1123"))
        self.assertTrue(self.manager.set_record(12, "Jake", "+1123"))
        self.assertFalse(self.manager.set_record(12, "Alice", "+1123"))
        self.assertEquals(self.manager.call(1), "CALLING John WITH +3581")
        self.assertEquals(self.manager.call(2), "NO SUCH USER")
        self.assertEquals(self.manager.call(12), "CALLING Jake WITH +1123")
        self.assertTrue(self.manager.delete_record(1))
        self.assertFalse(self.manager.delete_record(1))
        self.assertEquals(self.manager.call(1), "NO SUCH USER")
        self.assertEquals(self.manager.call(12), "CALLING Jake WITH +1123")
        self.manager.clear()

    def test1_2_nonExistentUsersCalls(self):
        self.assertEquals(self.manager.call(1), "NO SUCH USER")
        self.assertEquals(self.manager.call(1), "NO SUCH USER")
        self.assertEquals(self.manager.call(2), "NO SUCH USER")
        self.assertFalse(self.manager.delete_record(1))
        self.assertFalse(self.manager.delete_record(2))
        self.assertTrue(self.manager.set_record(1, "Bob", "+1234"))
        self.manager.clear()

    def test1_3_deletionAndRecreation(self):
        self.assertTrue(self.manager.set_record(1, "Alice", "+123"))
        self.assertTrue(self.manager.set_record(2, "Bob", "+456"))
        self.assertTrue(self.manager.delete_record(1))
        self.assertFalse(self.manager.delete_record(1))
        self.assertEquals(self.manager.call(2), "CALLING Bob WITH +456")
        self.assertTrue(self.manager.set_record(1, "Alice", "+123"))
        self.assertEquals(self.manager.call(1), "CALLING Alice WITH +123")
        self.manager.clear()

    def test_1_4_equalUsersWithDifferentIDs(self):
        self.assertTrue(self.manager.set_record(1, "Alice", "+123"))
        self.assertTrue(self.manager.set_record(2, "Alice", "+123"))
        self.assertTrue(self.manager.set_record(228, "Alice", "+123"))
        self.assertEquals(self.manager.call(1), "CALLING Alice WITH +123")
        self.assertEquals(self.manager.call(2), "CALLING Alice WITH +123")
        self.assertEquals(self.manager.call(228), "CALLING Alice WITH +123")
        self.manager.clear()

if __name__ == '__main__':
    unittest.main()