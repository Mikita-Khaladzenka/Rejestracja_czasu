let wynik = null;
let html5QrCode = null;
let blokada = false;

let language = localStorage.getItem("language") || "pl";

const translations = {
    pl: {
        title: "Rejestracja czasu pracy",
        description: "Skieruj kod QR pracownika do kamery",
        start: "Witaj {imie}<br><br>Rozpoczęcie pracy: {godzina}",
        finish:
            "Do zobaczenia {imie}<br><br>Wyjście: {godzina}<br>" +
            "Czas pracy: {godziny} godz. {minuty} min.",
        no_id: "Brak identyfikatora.",
        bad_qr: "Nieprawidłowy kod QR.",
        not_found: "Nie znaleziono pracownika.",
        server: "Błąd połączenia z serwerem.",
        camera: "Nie można uruchomić kamery.",
        camera_module: "Nie załadowano modułu kamery.",
        secure_context:
            "Kamera wymaga bezpiecznego połączenia.<br><br>" +
            "Otwórz stronę przez serwer aplikacji:<br>" +
            "<b>http://localhost:5000</b>"
    },

    es: {
        title: "Registro de tiempo de trabajo",
        description:
            "Apunte el código QR del empleado hacia la cámara",
        start:
            "Bienvenido {imie}<br><br>Inicio del trabajo: {godzina}",
        finish:
            "Hasta luego {imie}<br><br>Salida: {godzina}<br>" +
            "Tiempo trabajado: {godziny} h {minuty} min.",
        no_id: "Falta el identificador.",
        bad_qr: "Código QR no válido.",
        not_found: "No se encontró al empleado.",
        server: "Error de conexión con el servidor.",
        camera: "No se puede iniciar la cámara.",
        camera_module: "No se cargó el módulo de la cámara.",
        secure_context:
            "La cámara requiere una conexión segura.<br><br>" +
            "Abra la página a través del servidor:<br>" +
            "<b>http://localhost:5000</b>"
    }
};

function getWynik() {
    if (!wynik) {
        wynik = document.getElementById("wynik");
    }

    return wynik;
}

function translate(key, data = {}) {
    let text = translations[language]?.[key];

    if (!text) {
        return "";
    }

    Object.keys(data).forEach((name) => {
        text = text.replaceAll(
            `{${name}}`,
            String(data[name])
        );
    });

    return text;
}

function showMessage(message, success = false) {
    const box = getWynik();

    if (!box) {
        console.error("Nie znaleziono elementu #wynik");
        return;
    }

    box.style.display = "block";

    if (success) {
        box.style.background = "#d4edda";
        box.style.color = "#155724";
        box.style.border = "1px solid #28a745";
    } else {
        box.style.background = "#f8d7da";
        box.style.color = "#721c24";
        box.style.border = "1px solid #dc3545";
    }

    box.innerHTML = message;
}

function hideMessage() {
    const box = getWynik();

    if (!box) {
        return;
    }

    box.innerHTML = "";
    box.style.display = "none";
}

function changeLanguage() {
    language = language === "pl" ? "es" : "pl";

    localStorage.setItem("language", language);

    updateLanguage();
}

function updateLanguage() {
    const title = document.getElementById("title");
    const description = document.getElementById("description");
    const languageBtn = document.getElementById("languageBtn");

    if (title) {
        title.textContent = translations[language].title;
    }

    if (description) {
        description.textContent =
            translations[language].description;
    }

    if (languageBtn) {
        languageBtn.textContent =
            language === "pl" ? "ES" : "PL";
    }
}

async function rejestracja(id) {
    if (blokada) {
        return;
    }

    blokada = true;

    try {
        const response = await fetch("/rejestracja", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id: id
            })
        });

        if (!response.ok) {
            throw new Error(
                `Błąd HTTP: ${response.status}`
            );
        }

        const dane = await response.json();

        showMessage(
            translate(dane.typ, dane),
            dane.success === true
        );
    } catch (error) {
        console.error(
            "Błąd podczas rejestracji:",
            error
        );

        showMessage(translate("server"));
    } finally {
        setTimeout(() => {
            hideMessage();
            blokada = false;
        }, 3000);
    }
}

function onScanSuccess(decodedText) {
    if (blokada) {
        return;
    }

    console.log("Odczytano:", decodedText);

    rejestracja(decodedText);
}

function onScanFailure(errorMessage) {
    // Biblioteka zgłasza błędy odczytu w każdej klatce.
    // Nie wyświetlamy ich użytkownikowi.
}

async function startCamera() {
    if (!window.isSecureContext) {
        showMessage(translate("secure_context"));
        return;
    }

    if (typeof Html5Qrcode === "undefined") {
        showMessage(translate("camera_module"));
        return;
    }

    const reader = document.getElementById("reader");

    if (!reader) {
        showMessage(
            "Nie znaleziono elementu kamery #reader."
        );
        return;
    }

    try {
        html5QrCode = new Html5Qrcode("reader");

        await html5QrCode.start(
            {
               facingMode: "environment"
            },
            {
                fps: 10,
                qrbox: {
                    width: 250,
                    height: 250
                }
            },
            onScanSuccess,
            onScanFailure
        );
    } catch (error) {
        console.error(
            "Nie udało się uruchomić kamery:",
            error
        );

        let errorDetails = "";

        if (error?.name === "NotAllowedError") {
            errorDetails =
                "<br><br>Nie udzielono pozwolenia na użycie kamery.";
        } else if (error?.name === "NotFoundError") {
            errorDetails =
                "<br><br>Nie znaleziono kamery.";
        } else if (error?.name === "NotReadableError") {
            errorDetails =
                "<br><br>Kamera jest używana przez inną aplikację.";
        } else {
            errorDetails =
                `<br><br>${String(error)}`;
        }

        showMessage(
            translate("camera") + errorDetails
        );
    }
}

document.addEventListener("DOMContentLoaded", () => {
    wynik = document.getElementById("wynik");

    updateLanguage();
    startCamera();
});