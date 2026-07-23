class Employee:


    def __init__(
        self,
        id,
        imie,
        process
    ):

        self.id = id
        self.imie = imie
        self.process = process



    def to_dict(self):

        return {

            "id": self.id,

            "imie": self.imie,

            "process": self.process

        }
