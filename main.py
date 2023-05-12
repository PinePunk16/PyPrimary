# person.py
# Example of implementation of primary_object.

from person import Person



def main() -> None:
    people: list[Person] = []
    current_person: Person = None
    
    for _ in range(10):
        current_person = Person()
        current_person.generate()
        people.append(current_person)
    
    for person in people:
        person.save()
        person.load()
        person.show()

if __name__ == "__main__":
    main()
