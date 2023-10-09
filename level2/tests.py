import unittest
from contacts_manager_impl import ContactsManagerImpl


class LevelTests(unittest.TestCase):

    failureException = Exception

    def __assertListEmpty(self, x):
        self.assertTrue(
            len(x) == 0, "List is not empty"
        )

    def __prepCallsForMostPopular(self):
        self.assertTrue(self.manager.set_record(1, "Alice", "+123"))
        self.assertTrue(self.manager.set_record(2, "Bob", "+456"))
        self.assertTrue(self.manager.set_record(3, "John", "+3333"))
        self.assertEquals(self.manager.call(2), "CALLING Bob WITH +456")
        self.assertEquals(self.manager.call(2), "CALLING Bob WITH +456")
        self.assertEquals(self.manager.call(1), "CALLING Alice WITH +123")
        self.assertEquals(self.manager.call(1), "CALLING Alice WITH +123")
        self.assertEquals(self.manager.call(1), "CALLING Alice WITH +123")
        self.assertEquals(self.manager.call(3), "CALLING John WITH +3333")

    @classmethod
    def setUp(cls):
        cls.manager = ContactsManagerImpl()

    def test1_1_allOperationsSimpleCase(self):
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

    def test1_2_nonExistentUsersCalls(self):
        self.assertEquals(self.manager.call(1), "NO SUCH USER")
        self.assertEquals(self.manager.call(1), "NO SUCH USER")
        self.assertEquals(self.manager.call(2), "NO SUCH USER")
        self.assertFalse(self.manager.delete_record(1))
        self.assertFalse(self.manager.delete_record(2))
        self.assertTrue(self.manager.set_record(1, "Bob", "+1234"))

    def test1_3_deletionAndRecreation(self):
        self.assertTrue(self.manager.set_record(1, "Alice", "+123"))
        self.assertTrue(self.manager.set_record(2, "Bob", "+456"))
        self.assertTrue(self.manager.delete_record(1))
        self.assertFalse(self.manager.delete_record(1))
        self.assertEquals(self.manager.call(2), "CALLING Bob WITH +456")
        self.assertTrue(self.manager.set_record(1, "Alice", "+123"))
        self.assertEquals(self.manager.call(1), "CALLING Alice WITH +123")

    def test_1_4_equalUsersWithDifferentIDs(self):
        self.assertTrue(self.manager.set_record(1, "Alice", "+123"))
        self.assertTrue(self.manager.set_record(2, "Alice", "+123"))
        self.assertTrue(self.manager.set_record(228, "Alice", "+123"))
        self.assertEquals(self.manager.call(1), "CALLING Alice WITH +123")
        self.assertEquals(self.manager.call(2), "CALLING Alice WITH +123")
        self.assertEquals(self.manager.call(228), "CALLING Alice WITH +123")

    def test_2_1_allOperationsSimpleCase(self):
        self.__prepCallsForMostPopular()
        self.assertListEqual(self.manager.most_popular(3), ["Alice(3)", "Bob(2)", "John(1)"])

    def test_2_2_mostPopularEmptyList(self):
        self.__assertListEmpty(self.manager.most_popular(3))
        self.assertTrue(self.manager.set_record(1, "Ivan", "+322"))
        self.__assertListEmpty(self.manager.most_popular(3))
        self.__assertListEmpty(self.manager.most_popular(5))

    def test_2_3_mostPopularCut(self):
        self.__prepCallsForMostPopular()
        self.assertListEqual(self.manager.most_popular(3), ["Alice(3)", "Bob(2)", "John(1)"])
        self.assertListEqual(self.manager.most_popular(2), ["Alice(3)", "Bob(2)"])
        self.assertListEqual(self.manager.most_popular(1), ["Alice(3)"])
        self.assertListEqual(self.manager.most_popular(10), ["Alice(3)", "Bob(2)", "John(1)"])

    def test_2_3_mostPopularTies(self):
        self.__prepCallsForMostPopular()
        self.assertListEqual(self.manager.most_popular(3), ["Alice(3)", "Bob(2)", "John(1)"])
        self.assertListEqual(self.manager.most_popular(2), ["Alice(3)", "Bob(2)"])
        self.assertListEqual(self.manager.most_popular(1), ["Alice(3)"])
        self.assertEquals(self.manager.call(2), "CALLING Bob WITH +456")
        self.assertEquals(self.manager.call(2), "CALLING Bob WITH +456")
        self.assertListEqual(self.manager.most_popular(3), ["Bob(4)", "Alice(3)", "John(1)"])
        self.assertEquals(self.manager.call(1), "CALLING Alice WITH +123")
        self.assertListEqual(self.manager.most_popular(3), ["Alice(4)", "Bob(4)", "John(1)"])

        