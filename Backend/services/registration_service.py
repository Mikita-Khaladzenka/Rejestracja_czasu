from datetime import datetime, timedelta

from repositories.employee_repository import EmployeeRepository

from repositories.worktime_repository import WorkTimeRepository




class RegistrationService:



    employee_repository = EmployeeRepository()

    worktime_repository = WorkTimeRepository()





    @classmethod
    def register(
        cls,
        dane
    ):



        if not dane or "id" not in dane:


            return {


                "success": False,

                "typ": "no_id"


            }





        try:


            pracownik_id = int(

                dane["id"]

            )



        except:



            return {



                "success": False,

                "typ": "bad_qr"



            }







        pracownik = cls.employee_repository.find_by_id(


            pracownik_id


        )






        if not pracownik:



            return {



                "success": False,

                "typ": "not_found"



            }









        teraz = datetime.now()



        godzina = teraz.strftime(

            "%H:%M"

        )









        wpis = cls.worktime_repository.get_last_by_employee(



            pracownik_id



        )









        if wpis:



            start = datetime.strptime(



                wpis["rozpoczecie"],



                "%Y-%m-%d %H:%M:%S"



            )






            roznica = teraz - start







            # ======================================
            # Zakończenie pracy
            # ======================================



            if roznica < timedelta(hours=14):



                sekundy = int(



                    roznica.total_seconds()



                )





                godziny = sekundy // 3600





                minuty = (



                    sekundy % 3600



                ) // 60







                cls.worktime_repository.close_work(



                    wpis["id"],



                    teraz.strftime(



                        "%Y-%m-%d %H:%M:%S"



                    ),



                    sekundy



                )








                return {



                    "success": True,



                    "typ": "finish",



                    "imie": pracownik.imie,



                    "godzina": godzina,



                    "godziny": godziny,



                    "minuty": minuty



                }









            # ======================================
            # Nie zakończył poprzedniej pracy
            # ======================================



            else:




                if wpis["zakonczenie"] is None:



                    cls.worktime_repository.mark_not_finished(



                        wpis["id"]



                    )









        # ======================================
        # Rozpoczęcie nowej pracy
        # ======================================




        cls.worktime_repository.create(




            pracownik_id,



            teraz.strftime(



                "%Y-%m-%d"



            ),




            teraz.strftime(



                "%Y-%m-%d %H:%M:%S"



            )



        )









        return {



            "success": True,



            "typ": "start",



            "imie": pracownik.imie,



            "godzina": godzina



        }
