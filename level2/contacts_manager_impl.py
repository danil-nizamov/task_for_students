from interface import ContactsManagerInterface
class ContactsManagerImpl(ContactsManagerInterface):

    class User:
        user_name: str
        user_phone_number: str
        user_calls: int

        def __init__(self, name, phone_number) -> None:
            self.user_name = name
            self.user_phone_number = phone_number
            self.user_calls = 0
    
    database = dict() # type: dict[int, User]

    def __init__(self):
        pass
    
    def clear(self):
        self.database.clear()

    def has_record(self, id: int) -> bool:
        return id in self.database

    def set_record(self, id: int, name: str, phone_number: str) -> bool:
        if (self.has_record(id)): return False
        self.database[id] = self.User(name, phone_number)
        return True

    def delete_record(self, id: int) -> bool:
        if (self.has_record(id)):
            self.database.pop(id, None)
            return True
        return False

    def call(self, id: int) -> str:
        if (self.has_record(id)):
            user = self.database.get(id)
            user.user_calls += 1
            # self.database[id].user_calls += 1
            return f"CALLING {user.user_name} WITH {user.user_phone_number}"
        else:
            return "NO SUCH USER"

    def most_popular(self, n: int) -> list[str]:
        popular = list()
        current_count = 0
        for id in self.database:
            user = self.database.get(id)
            if user.user_calls == 0: continue
            if (current_count >= n): break
            current_count += 1
            
            popular.append([user.user_calls, f"{user.user_name}({user.user_calls})"])
        popular.sort(key=lambda x: x[0], reverse=True)
        return list(map(lambda x: x[1], popular))
