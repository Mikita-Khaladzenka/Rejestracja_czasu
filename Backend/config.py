import os


class Config:


    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )


    DB = os.path.join(
        BASE_DIR,
        "storage.db"
    )


    FRONTEND = os.path.join(
        BASE_DIR,
        "..",
        "Frontend"
    )


    SECRET_KEY = "Twoje tajne hasło do sesji"


    ADMIN_PASSWORD = "Twoje tajne hasło do panelu administracyjnego"
