from interface import ContactsManagerInterface


class ContactsManagerImpl(ContactsManagerInterface):

    def __init__(self):
        pass

    def set_record(self, id: int, name: str, phone_number: str) -> bool:
        return True

    def delete_record(self, id: int) -> bool:
        return True

    def call(self, id: int) -> str:
        return ""

    def most_popular(self, n: int) -> list[str]:
        return []

    def call_with_ts(self, id: int, ts: int) -> str:
        return ""

    def most_popular_in_range(self, n: int, ts_start: int, ts_end: int) -> list[str]:
        return []

    def calls_history(self, id: int) -> list[str]:
        return []

