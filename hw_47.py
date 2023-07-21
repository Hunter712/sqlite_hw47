import sqlite3


class Person:

    def __init__(self, name, favorite_color, profit):
        self.name = name
        self.favorite_color = favorite_color
        self.profit = profit

    def __repr__(self):
        return f"Person(name={self.name}, favorite_color={self.favorite_color}, profit={self.profit})"

    def get_person_attributes(self):
        return self.name, self.favorite_color, self.profit


class PeopleRepository:

    def __init__(self, db_path):
        self._connection = sqlite3.connect(db_path, isolation_level=None)
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "CREATE TABLE IF NOT EXISTS Persons(person_id INTEGER PRIMARY KEY, "
            "name TEXT, favorite_color TEXT, profit REAL);")

    def __del__(self):
        if self._cursor:
            self._cursor.close()
        if self._connection:
            self._connection.commit()
            self._connection.close()

    def add_person(self, person):
        self._cursor.execute("INSERT INTO Persons(name, favorite_color, profit) VALUES ((?), (?), (?));",
                             person.get_person_attributes())

    def add_people(self, persons):
        self._cursor.executemany("INSERT INTO Persons(name, favorite_color, profit) VALUES ((?), (?), (?));",
                                 [person.get_person_attributes() for person in persons])

    def get_all_people(self):
        data = self._cursor.execute('SELECT * from Persons;')
        return self.rows2objects(data)

    def get_person_by_parameter(self, search_parameter, sign, search_value):
        data = self._cursor.execute(f'SELECT * from Persons WHERE {search_parameter}{sign}(?);', (search_value,))
        return self.rows2objects(data)

    def update_person_by_parameter(self, set_parameter, new_value, search_parameter, sign, search_value):
        self._cursor.execute(f'UPDATE Persons SET {set_parameter}=(?)'
                             f'WHERE {search_parameter}{sign}(?);', (new_value, search_value))

    def delete_person_by_parameter(self, search_parameter, sign, search_value):
        self._cursor.execute(f'DELETE FROM Persons WHERE {search_parameter}{sign}(?);', (search_value,))

    def row2object(self, row):
        return Person(*row[1:])

    def rows2objects(self, rows):
        return [self.row2object(row) for row in rows]


person_repo = PeopleRepository('people.db')
people = [Person('Vlad1', 'RED', 3), Person('Vlad2', 'GREEN', 2), Person('Vlad3', 'BLUE', 21)]
person_repo.add_people(people)

print(person_repo.get_all_people())
print(person_repo.get_person_by_parameter("favorite_color", "=", "RED"))
person_repo.delete_person_by_parameter("favorite_color", "=", "GREEN")
print(person_repo.get_all_people())
person_repo.update_person_by_parameter("name", "Vladddd", "profit", ">", "10")
print(person_repo.get_all_people())
