function getCookie(name) {

    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    //RETORNANDO EL TOKEN
    return cookieValue;

}//end function getCookies


$( document ).ready(function() {
    console.log( "ready!" );
    let csrftoken = getCookie('csrftoken');
    let usuario =  $("#usuario").text();
    console.log(usuario)
    let data = { 'usuario': JSON.stringify(usuario), 'csrfmiddlewaretoken': csrftoken }
    envioajax('post','/actividad/ejecutar/',data,1) 
});


function envioajax(tipo,enlace,dato,evento){
    $.ajax({
        type: tipo,
        url: enlace,
        data: dato,
        success: function (response) {
            switch (evento) {
                case 1:
                    generartablaactividad(response);
                    break;
                case 2:
                    console.log('prueba2')
                    break;
                default:
                    break;
            }
        }
    });
}

function generartablaactividad(response){
    $('#mainTable tbody tr').remove(); 
    let nuevaFila = ""; // Crear cadena de string que contendra el codigo HTML para ingresar los datos del ORM o actividad consultada 
    console.log(response)
    for (let i in response['actividades']) {
        nuevaFila = "<tr>";
        nuevaFila += "<td>" + i + "</td>";
        nuevaFila += "<td>" + response['actividades'][i]['actividad'] + "</td>";
        nuevaFila += "<td>" + response['actividades'][i]['fechainicio'] + "</td>";
        nuevaFila += "<td>" + response['actividades'][i]['fechafin'] + "</td>";
        if(response['actividades'][i]['estado'] == 'I'){
            nuevaFila += "<td align='center'><i class='material-icons'>access_time</i> </td>";
        }
        //nuevaFila += "<td><a onclick=alert('hola')><i class='material-icons' >mode_edit</i> asas</a> </td>";
       
        //nuevaFila += "<td align='center'>" + "<button type='button' onclick='actualizarEstado("+response['actividades'][i]['secuencial']+")' class='btn bg-light-green waves-effect'><i class='material-icons'>create</i></button>" + "</td>";
        let variable = 'enviarparametros("btn'+'-'+response['actividades'][i]['secuencial']+'-'+response['actividades'][i]['estado']+'-'+i+'")'
        nuevaFila += "<td align='center'>" + "<button type='button' name='btn' value='btn' id='submitBtn1' onclick= '"+variable+"' data-toggle='modal' data-target='#confirm-submit' class='btn btn-default'><i class='material-icons'>create</i></button>"+"</td>";
        
        console.log(variable)
        //nuevaFila += "<td>" + response['actividades'][i]['estado'] + "</td>";
        nuevaFila += "<td align='center'>" + "<button type='button' onclick='gestionarInforme("+response['actividades'][i]['secuencial']+")' class='btn bg-red waves-effect'><i class='material-icons'>print</i></button>" + "</td>";
        nuevaFila += "</tr>";

        //class='btn btn-default waves-effect' data-toggle='modal' data-target='#smallModal'


        $("#mainTable tbody").append(nuevaFila);  // Añadir la cadana de string dentro del cuerpo de la tabla   

    }
}


function actualizarEstado(dato) {
    console.log(dato)
}

function gestionarInforme(dato) {
    
}


function enviarparametros(params) {
    console.log(params)
    let arrayparams = params.split("-")
    console.log(`Actividad: ${arrayparams[1]}`)
    console.log(`Estado: ${arrayparams[2]}`)
    console.log(`Row ${arrayparams[3]}`)
    $('#lname').text($('#lastname').val());
    $('#fname').text(params);
}

/// PRUBA DE MODAL CON PARAMETROS
$('#submitBtn').click(function() {
    $('#lname').text($('#lastname').val());
    $('#fname').text($('#submitBtn').val());
    
});

$('#submit').click(function(){
   alert('submitting');
   $('#formfield').submit();
});