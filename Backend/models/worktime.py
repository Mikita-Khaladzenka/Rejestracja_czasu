class WorkTime:


    def __init__(
        self,
        id,
        pracownik_id,
        data,
        rozpoczecie,
        zakonczenie,
        czas_pracy,
        nie_zakonczyl_prace
    ):

        self.id = id
        self.pracownik_id = pracownik_id
        self.data = data
        self.rozpoczecie = rozpoczecie
        self.zakonczenie = zakonczenie
        self.czas_pracy = czas_pracy
        self.nie_zakonczyl_prace = nie_zakonczyl_prace
