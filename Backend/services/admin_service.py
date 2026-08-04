from models.employee import Employee

from repositories.employee_repository import EmployeeRepository

from config import Config



class AdminService:


    employee_repository = EmployeeRepository()



    @staticmethod
    def login(dane):


        if dane and dane.get("haslo") == Config.ADMIN_PASSWORD:


            return {

                "success": True

            }



        return {

            "success": False,

            "komunikat": "Błędne hasło."

        }



    @classmethod
    def get_workers(cls):


        workers = cls.employee_repository.find_all()



        return [

            worker.to_dict()

            for worker in workers

        ]




    @classmethod
    def add_worker(
        cls,
        dane,
    ):

        if not dane:

            return {
                "success": False,
                "komunikat": "Nie przesłano danych."
            }

        try:

            employee_id = int(
                dane.get("id")
            )

            imie = str(
                dane.get("imie", "")
            ).strip()

            nazwisko = str(
                dane.get("nazwisko", "")
            ).strip()

            process = str(
                dane.get("process", "")
            ).strip()


            if not imie:

                return {
                    "success": False,
                    "komunikat": "Imię jest wymagane."
                }


            employee = Employee(
                employee_id,
                imie,
                nazwisko,
                process,
            )


            cls.employee_repository.save(
                employee
            )


            return {
                "success": True
            }


        except ValueError:

            return {
                "success": False,
                "komunikat":
                    "Identyfikator musi być liczbą."
            }


        except Exception as error:

            print(
                "Błąd dodawania pracownika:",
                error
            )

            return {
                "success": False,
                "komunikat":
                    "Nie udało się dodać pracownika. "
                    "ID już istnieje."
            }




    @classmethod
    def delete_worker(
        cls,
        id,
    ):

        try:

            deleted = cls.employee_repository.delete(
                id
            )

            if not deleted:

                return {
                    "success": False,
                    "komunikat":
                        "Nie znaleziono pracownika."
                }

            return {
                "success": True,
                "komunikat":
                    "Pracownik został usunięty."
            }

        except Exception as error:

            print(
                "Błąd usuwania pracownika:",
                repr(error)
            )

            return {
                "success": False,
                "komunikat":
                    "Nie można usunąć pracownika, "
                    "ponieważ posiada historię czasu pracy."
            }
