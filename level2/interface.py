from abc import ABC, abstractmethod


class ContactsManagerInterface(ABC):

    @abstractmethod
    def set_record(self, id: int, name: str, phone_number: str) -> bool:
        """
        Данная команда должна добавить в базу данных нового
        пользователя с указанными ID, именем, номером телефона.
        Если пользователь с таким ID уже существует,
        добавление невозможно – в таком случае, команда
        возвращает False. Если пользователь с таким ID
        был успешно добавлен – команда возвращает True.
        """
        pass

    @abstractmethod
    def delete_record(self, id: int) -> bool:
        """
        Данная команда удаляет пользователя с указанным ID
        из базы данных. Если удаление совершено успешно,
        команда возвращает True. Если пользователя с указанным
        ID не существует – команда возвращает False.
        """
        pass

    @abstractmethod
    def call(self, id: int) -> str:
        """
        Данная команда "совершает звонок" пользователю с
        указанным ID. Для этого команда должна вернуть строку
        "CALLING <NAME> WITH <PHONE NUMBER>. Если такого пользователя
        нет, команда возвращает строку "NO SUCH USER".
        """
        pass

    @abstractmethod
    def most_popular(self, n: int) -> list[str]:
        """
        Данная команда должна вернуть список N пользователей,
        которым звонят чаще всего. Если всего пользователей
        меньше, чем N – верните всех пользователей.
        Пользователи в списке должны быть отсортированы
        по количеству звонков в убывающем порядке.
        В случае ничьи – по алфавиту в возрастающем порядке.
        Команда возвращает список строк в данном формате:
        [<Name>(<Calls>), <Name2>(<Calls2>), ..., <NameN>(<CallsN>)]
        """
        pass
