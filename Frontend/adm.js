async function login(){

let haslo=document.getElementById("haslo").value;


let r=await fetch("/adm/login",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
haslo:haslo
})

});


let d=await r.json();


if(d.success){

document.getElementById("login").remove();

document.getElementById("panel").style.display="block";

load();

}

else{

alert("Błędne hasło");

}

}




async function load(){


let r=await fetch("/adm/pracownicy");

let dane=await r.json();


let html="";


dane.forEach(p=>{


html += `

<tr>

<td>${p.id}</td>

<td>${p.imie}</td>

<td>${p.process ?? ""}</td>

<td>

<button onclick="usun(${p.id})">
Usuń
</button>

</td>

</tr>

`;

});


document.getElementById("lista").innerHTML=html;

}





async function dodaj(){


await fetch("/adm/dodaj",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

id:id.value,

imie:imie.value,

process:process.value

})

});


load();

}




async function usun(id){


await fetch("/adm/usun/"+id,{

method:"DELETE"

});


load();

}