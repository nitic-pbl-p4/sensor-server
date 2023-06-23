from typing import Optional, List
from datetime import datetime
from queue import Queue
from logger import console, highlighter


class Person:
    def __init__(self, id: str, seenAt: datetime) -> None:
        if len(id) < 1:
            raise ValueError("Invalid id for person")
        self.id = id
        self.seenAt = seenAt

    def __repr__(self):
        return f"Person(id={self.id}, seenAt={self.seenAt})"


class Book:
    def __init__(self, id: str, readAt: datetime) -> None:
        if len(id) < 1:
            raise ValueError("Invalid id for book")
        self.id = id
        self.readAt = readAt

    def __repr__(self):
        return f"Book(id={self.id}, readAt={self.readAt})"


class State:
    def __init__(self) -> None:
        self._person: Optional[Person] = None
        self._book_queue: Queue[Book] = Queue(maxsize=100)

    @property
    def person(self) -> Optional[Person]:
        return self._person

    @person.setter
    def person(self, value: Optional[Person]) -> None:
        if value and not isinstance(value, Person):
            raise ValueError("Invalid value for person")
        self._person = value

    # getterを追加
    def get_person(self) -> Optional[Person]:
        return self._person

    def add_book(self, book: Book) -> None:
        # bookがBookのインスタンスか確かめる
        if not isinstance(book, Book):
            raise ValueError("Invalid value for book")
        # book_queueにbookを追加する
        # 挿入できる余裕がない場合は、一つ削除する
        if self._book_queue.full():
            self._book_queue.get(block=False)

        self._book_queue.put(book, block=False)

        return

    def get_books(self) -> List[Book]:
        return list(self._book_queue.queue)

    def __repr__(self):
        return (
            f"State(person={self._person}, book_queue={list(self._book_queue.queue)})"
        )


if __name__ == "__main__":
    my_obj = State()

    my_obj.person = Person(id="123", seenAt=datetime.now())
    console.log(f"my_obj.get_person(): {highlighter(repr(my_obj.get_person()))}")

    for i in range(120):
        my_obj.add_book(Book(id=f"book{i}", readAt=datetime.now()))

    console.log(f"my_obj.get_books(): {highlighter(repr(my_obj.get_books()))}")
