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

    def test3_1_allOperationsWithTimestampsSimpleCase(self):
        self.assertTrue(self.manager.set_record(1, "John", "+3581"))
        self.assertEquals(self.manager.call_with_ts(1, 1), "CALLING John WITH +3581 AT 1")
        self.assertEquals(self.manager.call_with_ts(12, 2), "NO SUCH USER")
        self.assertEquals(self.manager.call_with_ts(1, 3), "CALLING John WITH +3581 AT 3")
        self.assertListEqual(self.manager.calls_history(1), ["1", "3"])

    def test3_2_nonExistentUsersCallsWithTimestamps(self):
        self.assertEquals(self.manager.call_with_ts(1, 1), "NO SUCH USER")
        self.assertEquals(self.manager.call_with_ts(2, 2), "NO SUCH USER")
        self.assertFalse(self.manager.delete_record(1))
        self.assertTrue(self.manager.set_record(1, "Bob", "+1234"))
        self.assertEquals(self.manager.call_with_ts(1, 3), "CALLING Bob WITH +1234 AT 3")

    def test3_3_MixedCallTypes(self):
        self.assertTrue(self.manager.set_record(1, "Alice", "+123"))
        self.assertEquals(self.manager.call(1), "CALLING Alice WITH +123")
        self.assertEquals(self.manager.call_with_ts(1, 1), "CALLING Alice WITH +123 AT 1")
        self.assertEquals(self.manager.call(1), "CALLING Alice WITH +123")
        self.assertEquals(self.manager.call_with_ts(1, 1), "CALLING Alice WITH +123 AT 4512")
        self.assertListEqual(self.manager.calls_history(1), ["0(2)", "1", "4512"])
        self.assertEquals(self.manager.call(1), "CALLING Alice WITH +123")
        self.assertListEqual(self.manager.calls_history(1), ["0(3)", "1", "4512"])

    def test3_4_MixedCallTypesMultipleUsers(self):
        self.assertTrue(self.manager.set_record(1112, "Alice", "+322"))
        self.assertTrue(self.manager.set_record(324, "Bob", "+228"))
        self.assertEquals(self.manager.call(1112), "CALLING Alice WITH +322")
        self.assertEquals(self.manager.call_with_ts(1112, 16), "CALLING Alice WITH +123 AT 16")
        self.assertEquals(self.manager.call(1112), "CALLING Alice WITH +322")
        self.assertListEqual(self.manager.calls_history(1112), ["0(2)", "16"])
        self.assertEquals(self.manager.call(324), "CALLING Bob WITH +228")
        self.assertEquals(self.manager.call_with_ts(324, 202), "CALLING Bob WITH +228 AT 202")
        self.assertEquals(self.manager.call_with_ts(324, 255), "CALLING Bob WITH +228 AT 255")
        self.assertListEqual(self.manager.calls_history(324), ["0(1)", "202", "255"])
        self.assertListEqual(self.manager.calls_history(1112), ["0(2)", "16"])
        self.assertEquals(self.manager.call(1112), "CALLING Alice WITH +322")
        self.assertListEqual(self.manager.calls_history(324), ["0(1)", "202", "255"])
        self.assertListEqual(self.manager.calls_history(1112), ["0(3)", "16"])

    def test3_5_MostPopularInRange(self):
        self.manager.set_record(1, "Alice", "+123")
        self.manager.set_record(2, "Bob", "+456")
        self.manager.call_with_ts(1, 1)
        self.manager.call_with_ts(1, 2)
        self.manager.call_with_ts(1, 4)
        self.manager.call_with_ts(1, 5)
        self.manager.call_with_ts(2, 6)
        self.manager.call_with_ts(2, 7)
        self.manager.call_with_ts(2, 8)
        self.assertListEqual(self.manager.most_popular_in_range(2, 1, 4), ["Alice(3)"])
        self.assertListEqual(self.manager.most_popular_in_range(2, 3, 7), ["Alice(2)", "Bob(2)"])
        self.assertListEqual(self.manager.most_popular_in_range(2, 5, 8), ["Bob(3)", "Alice(1)"])
        self.assertListEqual(self.manager.most_popular_in_range(2, 6, 8), ["Bob(3)"])

    def test4_1_callsHistoryGroupedSingleGroup(self):
        self.manager.set_record(1, "Alice", "+123")
        self.manager.call_with_ts(1, 10)
        self.manager.call_with_ts(1, 12)
        self.manager.call_with_ts(1, 13)
        self.assertListEqual(self.manager.calls_history_grouped(1, 4), ["10(3)"])

    def test4_2_callsHistoryGroupedMultipleGroups(self):
        self.manager.set_record(1, "Alice", "+123")
        self.manager.call_with_ts(1, 10)
        self.manager.call_with_ts(1, 12)
        self.manager.call_with_ts(1, 18)
        self.manager.call_with_ts(1, 22)
        self.manager.call_with_ts(1, 23)
        self.manager.call_with_ts(1, 25)
        self.assertListEqual(self.manager.calls_history_grouped(1, 3), ["10(2)", "18(1)", "22(3)"])

    def test4_3_callsHistoryGroupedMixedCallTypes(self):
        self.manager.set_record(1, "Alice", "+123")
        self.manager.call(1)
        self.manager.call(1)
        self.manager.call_with_ts(1, 10)
        self.manager.call_with_ts(1, 12)
        self.manager.call_with_ts(1, 18)
        self.manager.call_with_ts(1, 22)
        self.manager.call_with_ts(1, 23)
        self.manager.call_with_ts(1, 25)
        self.assertListEqual(self.manager.calls_history_grouped(1, 3), ["0(2)", "10(2)", "18(1)", "22(3)"])

    def test4_4_callsHistoryGroupedSingleCall(self):
        self.manager.set_record(1, "Alice", "+123")
        self.manager.call_with_ts(1, 10)
        self.assertListEqual(self.manager.calls_history_grouped(1, 3), ["10(1)"])

    def test4_5_callsHistoryGroupedNoCalls(self):
        self.manager.set_record(1, "Alice", "+123")
        self.assertListEqual(self.manager.calls_history_grouped(1, 3), [])