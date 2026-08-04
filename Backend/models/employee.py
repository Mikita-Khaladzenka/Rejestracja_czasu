class Employee:


    def __init__(
        self,
        id,
        imie,
        nazwisko,
        process
    ):

        self.id = id
        self.imie = imie
        self.nazwisko = nazwisko
        self.process = process



    def to_dict(self):

        return {

            "id": self.id,

            "imie": self.imie,

            "nazwisko": self.nazwisko,

            "process": self.process

        }