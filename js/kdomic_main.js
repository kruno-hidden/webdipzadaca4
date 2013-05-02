function addErrorMess(parent, message){
	if(document.getElementById(parent.name+"Error")!==null)
        return;	
	var table=document.getElementsByTagName("table")[0];
	var newPos = parent.parentNode.parentNode.rowIndex+1;
	var row = table.insertRow(newPos);
	var cell1=row.insertCell(0);
	var cell2=row.insertCell(1);
	cell1.innerHTML="";
	cell2.setAttribute("id",parent.name+"Error");
	cell2.setAttribute("class","errorLabelMessage");
	cell2.innerHTML=message;
}

function removeErrorMess(id){
    if(document.getElementById(id+"Error")===null)
        return;
    var table=document.getElementsByTagName("table")[0];
	var remPos = document.getElementById(id+"Error").parentNode.rowIndex;
    table.deleteRow(remPos);
}

function checkUsername(){
    var username = $('#korisnicko').val();
    var ok;
    $.ajax({
        url:'podaci/korisnik.php?korisnik='+username,
        async:false,
        type: 'GET',
        dataType: 'xml',
        success: function(xml) {
            var data = $(xml).find('korisnici');
            var num = parseInt(data.text());
            if(num===1){
                addErrorMess(korisnicko, "Već postoji!");
                ok = false;
            } else {
                removeErrorMess("korisnicko");
                ok = true;
            }
        }
    });
    return ok;
}

function checkPassword(){
    var lozinka1 = document.getElementById("lozinka");
    var lozinka2 = document.getElementById("lozinka2");
    if(lozinka1.value===""){
        addErrorMess(lozinka1, "Lozinka je obavezna!");
        return false;
    } else {
        removeErrorMess("lozinka");
    }
    if(lozinka1.value!==lozinka2.value){
        addErrorMess(lozinka2, "Lozinke se ne poklapaju!");
        return false;
    } else {
        removeErrorMess("lozinka2");
        return true;
    }
}

function checkText(t){
    var pattern = /^[A-Z][a-z]*$/;
    return pattern.test(t);
}

function checkSex(){
    var spol = document.getElementById("spol");
    if(spol.value!=='m' && spol.value!=='z'){
        addErrorMess(spol, "Izaberite spol");
        return false;        
    } else {
        removeErrorMess("spol");
        return true;
    }
}

function korisnickoIsEmpty(){
    if(!document.getElementById("korisnicko").value){
    	addErrorMess(korisnicko, "Obavezno polje");
    	document.getElementById("korisnicko").focus();
        return true;
    } else {
        removeErrorMess("korisnicko");
        return false;
    }
}

function lozinkaIsEmpty(){
    if(!document.getElementById("lozinka").value){
    	addErrorMess(lozinka, "Obavezno polje");
    	if(!korisnickoIsEmpty()) document.getElementById("lozinka").focus();
        return true;
    } else {
        removeErrorMess("lozinka");
        return false;
    }
}

var checkRegForm = function (e) {
    var imeOk = checkText(document.getElementById("ime").value);
    var prezimeOk = checkText(document.getElementById("prezime").value);
    var passOk = checkPassword();
    var sexOk = checkSex();
    var usernameOk = checkUsername();
    if(!(imeOk && prezimeOk && passOk && sexOk && usernameOk))
        e.preventDefault();
    selectFirstError();
};

var checkLoginForm = function (e) {
    if(korisnickoIsEmpty()||lozinkaIsEmpty()) e.preventDefault();
};

function  selectFirstError() {
    var errorList = document.getElementsByClassName("errorLabelMessage");
    var id = errorList[0].id.split("Error")[0];
    document.getElementById(id).focus();    
}

function getCitys(){
    var mjesta = new Array();    
    $.getJSON("podaci/gradovi.json", function(data){
    $.each(data, function (index, value) {
        mjesta.push(value);
    });
});
    return mjesta;
}

window.onload = function() {  
    /* === Define color change === */
    //polje koje ima fokus je označeno drugom css klasom od ostalih (boja, okvir, ... - po želji)
    var inputs = document.getElementsByTagName("input");
    if(inputs && inputs.length){
        inputs[0].className = "selectInput";
        for(var i=0; i<inputs.length; i++){
            inputs[i].addEventListener("focus",function(){this.className = "selectInput";});
            inputs[i].addEventListener("blur",function(){this.className = "deselectInput";});
        }        
    }
    //labela iznad koje je kursor mijenja klasu na hover
    var labels = document.getElementsByTagName("label");
    if(labels)
        for(var i=0; i<labels.length; i++){
            labels[i].addEventListener("mouseover",function(){this.className = "currentLabel";});
            labels[i].addEventListener("mouseout",function(){this.className = "";});
        }

    /* === Check field for pattern === */
    //lozinka i potvrda lozinke moraju biti iste
    var lozinka1 = document.getElementById("lozinka");
    var lozinka2 = document.getElementById("lozinka2");
    if(lozinka1 && lozinka2){
        lozinka1.addEventListener("blur",function(){checkPassword();});
        lozinka2.addEventListener("keyup",function(){checkPassword();});
    }
    
        
    //provjera da li ime i prezime počinju velikim slovom, da li sadržavaju samo slova
    var ime = document.getElementById("ime");
    if(ime)
        ime.addEventListener("blur",function(){
            if(!checkText(ime.value)){
                addErrorMess(ime, "Prvo veliko, ostalo malo");
            } else {
                removeErrorMess("ime");
            }
        });        
    var prezime = document.getElementById("prezime");
    if(prezime)
        prezime.addEventListener("blur",function(){
            if(!checkText(prezime.value)){
                addErrorMess(prezime, "Prvo veliko, ostalo malo");
            } else {
                removeErrorMess("prezime");
            }
        });
            
    /* === onSubmit - registracija ===*/
    //selectbox za odabir spola ima vrijednosti 'odaberi','ženski','muški',
    var forma = document.getElementById("regForm");    
    if(forma){
        forma.addEventListener('submit', checkRegForm, false);
        $('#korisnicko').blur(function(){checkUsername();});
        $(function() {
            var popisMjesta = getCitys();
            $("#mjesto").autocomplete({
            source: popisMjesta
                });
          });
    }
    
    /* === onSubmit - login ===*/
    var forma = document.getElementById("loginForm");   
    if(forma){
        forma.addEventListener('submit', checkLoginForm, false);
        korisnicko.addEventListener("blur",function(){korisnickoIsEmpty();});
        lozinka.addEventListener("blur",function(){lozinkaIsEmpty();});
    }
    
};

/* === Tablica korisnika ===*/

$('#btnXML').click(function(){btnXML();});
$('#btnJSON').click(function(){btnJSON();});

function btnXML(){
    $.ajax({
        url:'podaci/korisnici.xml',
        type: 'GET',
        dataType: 'xml',
        success: function(xml) {
            var tablica = $('<table id="tablica">');
            tablica.append('<thead><tr><th>Ime</th><th>Prezime</th><th>Email</th></tr></thead>');
            var tbody = $('<tbody>');
            $(xml).find('korisnici').each(function() {               
                $(this).children().each(function(){
                    tbody.append('<tr><td>' + $(this).attr('ime') + '</td><td>' + $(this).attr('prezime') +'</td><td>'+ $(this).attr('email') +'</td></tr>');
                });                
            });
            tablica.append(tbody);
            $('#content').html(tablica);
            $('#tablica').dataTable();
        }
    });
}

function btnJSON(){
    $.getJSON('podaci/korisnici.json', function(data){
        var tablica = $('<table id="tablica">');
        tablica.append('<thead><tr><th>Ime</th><th>Prezime</th><th>Email</th></tr></thead>');
        var tbody = $('<tbody>');
        for(i = 0; i < data.length; i++) {
            tbody.append('<tr><td>' + data[i].ime + '</td><td>' + data[i].prezime+'</td><td>'+data[i].email+'</td></tr>')  ;              
        }
        tablica.append(tbody);
        $('#content').html(tablica);
        $('#tablica').dataTable();
    });
}

function editJSONuser(id){
    window.open("korisnici_uredi.php?id="+id, "_self");
}