from interface import ContactsManagerInterface


class ContactsManagerImpl(ContactsManagerInterface):
    class User:
        user_name: str
        user_phone_number: str
        user_calls: int
        user_call_history: list[int]

        def __init__(self, name, phone_number) -> None:
            self.user_name = name
            self.user_phone_number = phone_number
            self.user_calls = 0
            self.user_call_history = list()
    
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
            user.user_call_history.append(0)
            # self.database[id].user_calls += 1
            return f"CALLING {user.user_name} WITH {user.user_phone_number}"
        else:
            return "NO SUCH USER"

    def most_popular(self, n: int) -> list[str]:
        popular = list()
        # current_count = 0
        for id in self.database:
            user = self.database.get(id)
            if user.user_calls == 0: continue
            # if (current_count >= n): break
            # current_count += 1
            
            popular.append([user.user_calls, f"{user.user_name}({user.user_calls})"])
        popular.sort(key=lambda x: x[0], reverse=True)
        return list(map(lambda x: x[1], popular))[:n]

    def call_with_ts(self, id: int, ts: int) -> str:
        if (self.has_record(id)):
            user = self.database.get(id)
            user.user_calls += 1
            user.user_call_history.append(ts)
            # self.database[id].user_calls += 1
            return f"CALLING {user.user_name} WITH {user.user_phone_number} AT {ts}"
        else:
            return "NO SUCH USER"

    def most_popular_in_range(self, n: int, ts_start: int, ts_end: int) -> list[str]:
        popular = list()
        # current_count = 0
        for id in self.database:
            user = self.database.get(id)
            calls_in_timestamp = self.get_calls_in_timestamp(user, ts_start, ts_end)
            if calls_in_timestamp == 0: continue
            popular.append([calls_in_timestamp, f"{user.user_name}({calls_in_timestamp})"])
        popular.sort(key=lambda x: x[0], reverse=True)
        return list(map(lambda x: x[1], popular))[:n]
    
    def get_calls_in_timestamp(self, user: User, ts_start: int, ts_end: int):
        calls_in_timestamp = 0
        for call_timestamp in user.user_call_history:
            if (ts_start <= call_timestamp <= ts_end):
                calls_in_timestamp += 1
        return calls_in_timestamp


    def calls_history(self, id: int) -> list[str]:
        if (self.has_record(id)):
            calls = list()
            user = self.database.get(id)
            if (user.user_call_history.count(0) > 0):
                calls.append(f"0({user.user_call_history.count(0)})")
            for call_timestamp in user.user_call_history:
                if (call_timestamp == 0): continue
                calls.append(f"{call_timestamp}")
            return calls
        return False



    def calls_history_grouped(self, id: int, window: int) -> list[str]:
        if (self.has_record(id)):
            calls = dict()
            user = self.database.get(id)
            for call_timestamp in user.user_call_history:
                if (call_timestamp == 0): continue
                for call_group_start in calls:
                    if calls[call_group_start][0] + window > call_timestamp:
                        calls[call_group_start][0] = call_timestamp
                        calls[call_group_start][1] += 1
                        break
                else:
                    calls[call_timestamp] = [call_timestamp, 1]
            if (user.user_call_history.count(0) > 0):
                calls[0] = [0, user.user_call_history.count(0)]
            call_history = list()
            for group_start_time in sorted(calls.keys()):
                call_history.append(f"{group_start_time}({calls[group_start_time][1]})")
            return call_history
        return False

