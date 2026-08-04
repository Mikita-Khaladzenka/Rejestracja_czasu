def start_app() -> None:

    process_options = {
        "cwd": str(WORKDIR),
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "stdin": subprocess.DEVNULL,
    }

    if os.name == "nt":

        process_options["creationflags"] = (
            subprocess.CREATE_NO_WINDOW
        )

    else:

        process_options["start_new_session"] = True

    subprocess.Popen(
        [
            str(PYTHON),
            str(APP),
        ],
        **process_options,
    )

    logging.info(
        "Uruchomiono app.py przy użyciu: %s",
        PYTHON,
    )s