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
        dane
    ):


        try:


            employee = Employee(

                int(dane["id"]),

                dane["imie"],

                dane["process"]

            )



            cls.employee_repository.save(
                employee
            )



            return {

                "success": True

            }



        except Exception:


            return {

                "success": False,

                "komunikat":
                "ID już istnieje."

            }




    @classmethod
    def delete_worker(
        cls,
        id
    ):


        cls.employee_repository.delete(
            id
        )



        return {

            "success": True

        }
