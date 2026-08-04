async function login(){


let haslo = document.getElementById(
    "haslo"
).value;



let r = await fetch(
    "/adm/login",
    {

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            haslo:haslo
        })

    }
);



let d = await r.json();



if(d.success){


    document.getElementById(
        "login"
    ).remove();


    document.getElementById(
        "panel"
    ).style.display="block";


    przygotujRaporty();


    load();


}
else{


    alert(
        "Błędne hasło"
    );


}

}




// ======================================
// PRZYGOTOWANIE PÓL RAPORTÓW
// ======================================

function przygotujRaporty(){


    let rok =
    document.getElementById(
        "rokRaportu"
    );


    let obecny =
    new Date().getFullYear();



    for(
        let i = obecny;
        i >= obecny - 5;
        i--
    ){

        let option =
        document.createElement(
            "option"
        );


        option.value = i;

        option.text =
        i;


        rok.appendChild(
            option
        );

    }



    let tydzien =
    document.getElementById(
        "tydzienRaportu"
    );



    for(
        let i=1;
        i<=53;
        i++
    ){


        let option =
        document.createElement(
            "option"
        );


        option.value=i;

        option.text =
        "Tydzień " + i;


        tydzien.appendChild(
            option
        );


    }



    zmianaTypuRaportu();


}




// ======================================
// ZMIANA TYPU RAPORTU
// ======================================

function zmianaTypuRaportu(){



let typ =
document.getElementById(
    "typRaportu"
).value;



let miesiac =
document.getElementById(
    "miesiacRaportu"
);



let tydzien =
document.getElementById(
    "tydzienRaportu"
);



if(
    typ === "monthly"
){


    miesiac.style.display =
    "block";


    tydzien.style.display =
    "none";


}
else{


    miesiac.style.display =
    "none";


    tydzien.style.display =
    "block";


}



}






// ======================================
// LISTA PRACOWNIKÓW
// ======================================

async function load(){



let r =
await fetch(
    "/adm/pracownicy"
);



let dane =
await r.json();



let html = "";



dane.forEach(
p=>{


html += `

<tr>

<td>${p.id}</td>

<td>${p.imie}</td>

<td>${p.nazwisko ?? ""}</td>

<td>${p.process ?? ""}</td>

<td>

<button onclick="usun(${p.id})">
Usuń
</button>

</td>


</tr>

`;



});



document.getElementById(
    "lista"
).innerHTML = html;



}





// ======================================
// DODAWANIE PRACOWNIKA
// ======================================

async function dodaj() {

    const dane = {
        id: document.getElementById(
            "id"
        ).value.trim(),

        imie: document.getElementById(
            "imie"
        ).value.trim(),

        nazwisko: document.getElementById(
            "nazwisko"
        ).value.trim(),

        process: document.getElementById(
            "process"
        ).value.trim()
    };


    try {

        const response = await fetch(
            "/adm/dodaj",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(dane)
            }
        );


        const wynik = await response.json();

        console.log(
            "Dodawanie pracownika:",
            wynik
        );


        if (!response.ok || !wynik.success) {

            alert(
                wynik.komunikat ||
                "Nie udało się dodać pracownika."
            );

            return;
        }


        document.getElementById(
            "id"
        ).value = "";

        document.getElementById(
            "imie"
        ).value = "";

        document.getElementById(
            "nazwisko"
        ).value = "";

        document.getElementById(
            "process"
        ).value = "";


        await load();

    } catch (error) {

        console.error(
            "Błąd dodawania pracownika:",
            error
        );

        alert(
            "Błąd połączenia z serwerem."
        );
    }
}






// ======================================
// USUWANIE
// ======================================

async function usun(id) {

    const potwierdzenie = confirm(
        "Czy na pewno chcesz usunąć pracownika?"
    );

    if (!potwierdzenie) {
        return;
    }

    try {

        const response = await fetch(
            "/adm/usun/" + id,
            {
                method: "DELETE"
            }
        );

        const wynik = await response.json();

        if (!response.ok || !wynik.success) {

            alert(
                wynik.komunikat ||
                "Nie udało się usunąć pracownika."
            );

            return;
        }

        await load();

    } catch (error) {

        console.error(
            "Błąd usuwania pracownika:",
            error
        );

        alert(
            "Błąd połączenia z serwerem."
        );
    }
}







// ======================================
// GENEROWANIE RAPORTU
// ======================================

// ======================================
// GENEROWANIE RAPORTU
// ======================================

async function generujRaport(){


let typ =
document.getElementById(
    "typRaportu"
).value;



let format =
document.getElementById(
    "formatRaportu"
).value;



let year =
document.getElementById(
    "rokRaportu"
).value;



let month =
document.getElementById(
    "miesiacRaportu"
).value;



let week =
document.getElementById(
    "tydzienRaportu"
).value;



let dane = {


    typ: typ,

    format: format,

    year: year

};



if(typ === "monthly"){


    dane.month = month;


}
else{


    dane.week = week;


}



let response =
await fetch(

"/adm/raport",

{

method:"POST",

headers:{

    "Content-Type":"application/json"

},

body:JSON.stringify(dane)

}

);



if(!response.ok){


    alert(
        "Błąd generowania raportu"
    );


    return;

}



let blob =
await response.blob();


let url =
window.URL.createObjectURL(
    blob
);


let a =
document.createElement(
    "a"
);


a.href = url;


// Nazwa przekazana przez backend
let disposition =
response.headers.get(
    "Content-Disposition"
);


let filename =
format === "pdf"
    ? "Raport.pdf"
    : "Raport.xlsx";


if(disposition){


    // Obsługa:
    // filename*=UTF-8''nazwa%20pliku.xlsx
    let utf8Match =
    disposition.match(
        /filename\*=UTF-8''([^;]+)/i
    );


    if(utf8Match){

        filename = decodeURIComponent(
            utf8Match[1]
        );

    }
    else{

        // Obsługa:
        // filename="nazwa pliku.xlsx"
        let standardMatch =
        disposition.match(
            /filename="?([^";]+)"?/i
        );


        if(standardMatch){

            filename = standardMatch[1];

        }

    }

}


a.download = filename;


document.body.appendChild(
    a
);


a.click();


a.remove();


window.URL.revokeObjectURL(
    url
);


}