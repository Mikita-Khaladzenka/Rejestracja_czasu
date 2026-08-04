from datetime import datetime, timedelta

from repositories.employee_repository import EmployeeRepository
from repositories.worktime_repository import WorktimeRepository


class RegistrationService:
    """
    Logika biznesowa rejestracji czasu pracy.

    Pierwszy skan rozpoczyna pracę.
    Każdy następny skan w ciągu 14 godzin
    aktualizuje godzinę zakończenia tej samej sesji.
    """

    employee_repository = EmployeeRepository()
    worktime_repository = WorktimeRepository()

    MAX_SHIFT_HOURS = 14

    @classmethod
    def register(
        cls,
        dane: dict,
    ) -> dict:

        # ===============================
        # WALIDACJA IDENTYFIKATORA
        # ===============================

        if not dane or "id" not in dane:

            return {
                "success": False,
                "typ": "no_id",
            }

        try:

            pracownik_id = int(
                str(dane["id"]).strip()
            )

        except (TypeError, ValueError):

            return {
                "success": False,
                "typ": "bad_qr",
            }

        # ===============================
        # SPRAWDZENIE PRACOWNIKA
        # ===============================

        pracownik = (
            cls.employee_repository.find_by_id(
                pracownik_id
            )
        )

        if not pracownik:

            return {
                "success": False,
                "typ": "not_found",
            }

        teraz = datetime.now()

        godzina = teraz.strftime(
            "%H:%M"
        )

        wpis = (
            cls.worktime_repository
            .get_last_by_employee(
                pracownik_id
            )
        )

        # ===============================
        # OBSŁUGA OSTATNIEGO WPISU
        # ===============================

        if wpis:

            start = datetime.strptime(
                wpis["rozpoczecie"],
                "%Y-%m-%d %H:%M:%S",
            )

            roznica = teraz - start

            # ===============================
            # AKTUALIZACJA GODZINY WYJŚCIA
            # ===============================

            if roznica < timedelta(
                hours=cls.MAX_SHIFT_HOURS
            ):

                sekundy = int(
                    roznica.total_seconds()
                )

                godziny = sekundy // 3600

                minuty = (
                    sekundy % 3600
                ) // 60

                # Ta metoda wykonuje UPDATE,
                # dlatego kolejne skany nadpisują
                # zakończenie tej samej sesji.
                cls.worktime_repository.close_work(
                    wpis["id"],
                    teraz.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    sekundy,
                )

                return {
                    "success": True,
                    "typ": "finish",
                    "imie": pracownik.imie,
                    "godzina": godzina,
                    "godziny": godziny,
                    "minuty": minuty,
                }

            # ===============================
            # SESJA STARSZA NIŻ 14 GODZIN
            # ===============================

            if wpis["zakonczenie"] is None:

                cls.worktime_repository.mark_not_finished(
                    wpis["id"]
                )

        # ===============================
        # ROZPOCZĘCIE NOWEJ SESJI
        # ===============================

        cls.worktime_repository.create(
            pracownik_id,
            teraz.strftime(
                "%Y-%m-%d"
            ),
            teraz.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        )

        return {
            "success": True,
            "typ": "start",
            "imie": pracownik.imie,
            "godzina": godzina,
        }
