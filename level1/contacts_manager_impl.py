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

