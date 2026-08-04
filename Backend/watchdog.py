from __future__ import annotations

import logging
import os
import subprocess
import sys
import time
from pathlib import Path

import psutil


# ======================================
# ŚCIEŻKI
# ======================================

WORKDIR = Path(__file__).resolve().parent
APP = WORKDIR / "app.py"

CHECK_INTERVAL = 5


# ======================================
# LOGOWANIE
# ======================================

logging.basicConfig(
    filename=str(WORKDIR / "watchdog.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


# ======================================
# INTERPRETER PYTHONA
# ======================================

def get_python_interpreter() -> Path:
    """
    Wybiera interpreter z lokalnego środowiska .venv.
    Na Windows używa pythonw.exe.
    Na Linuxie i macOS używa .venv/bin/python.
    """

    project_directory = WORKDIR.parent

    if os.name == "nt":
        python_path = (
            project_directory
            / ".venv"
            / "Scripts"
            / "pythonw.exe"
        )
    else:
        python_path = (
            project_directory
            / ".venv"
            / "bin"
            / "python"
        )

    if not python_path.exists():
        raise FileNotFoundError(
            f"Nie znaleziono interpretera środowiska "
            f"wirtualnego: {python_path}"
        )

    return python_path


PYTHON = get_python_interpreter()


# ======================================
# SPRAWDZANIE PROCESU
# ======================================

def app_running() -> bool:
    """
    Sprawdza, czy app.py jest już uruchomiony.
    """

    expected_app = os.path.normcase(
        os.path.realpath(APP)
    )

    for process in psutil.process_iter(
        ["pid", "cmdline"]
    ):
        try:
            cmdline = process.info.get(
                "cmdline"
            )

            if not cmdline:
                continue

            for argument in cmdline:
                if not argument:
                    continue

                try:
                    normalized_argument = (
                        os.path.normcase(
                            os.path.realpath(argument)
                        )
                    )
                except (OSError, TypeError):
                    continue

                if normalized_argument == expected_app:
                    return True

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    return False


# ======================================
# URUCHAMIANIE APLIKACJI
# ======================================

def start_app() -> None:
    """
    Uruchamia app.py jako osobny proces.
    """

    app_log_path = WORKDIR / "app.log"

    app_log = open(
        app_log_path,
        "a",
        encoding="utf-8",
    )

    options = {
        "cwd": str(WORKDIR),
        "stdout": app_log,
        "stderr": app_log,
        "stdin": subprocess.DEVNULL,
    }

    if os.name == "nt":
        options["creationflags"] = (
            subprocess.CREATE_NO_WINDOW
        )
    else:
        options["start_new_session"] = True

    try:
        process = subprocess.Popen(
            [
                str(PYTHON),
                str(APP),
            ],
            **options,
        )

        logging.info(
            "Uruchomiono app.py. PID: %s, Python: %s",
            process.pid,
            PYTHON,
        )

    finally:
        app_log.close()


# ======================================
# GŁÓWNA PĘTLA
# ======================================

def main() -> None:
    logging.info(
        "Watchdog uruchomiony. "
        "Python: %s, aplikacja: %s",
        PYTHON,
        APP,
    )

    while True:
        try:
            if not app_running():
                logging.info(
                    "app.py nie działa — uruchamiam."
                )

                start_app()

        except Exception:
            logging.exception(
                "Błąd działania watchdoga"
            )

        time.sleep(
            CHECK_INTERVAL
        )


if __name__ == "__main__":
    main()