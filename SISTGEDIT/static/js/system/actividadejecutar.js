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
                    generartablaactividad();
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

function generartablaactividad(){
    $('#mainTable tbody tr').remove(); 
    let nuevaFila_TBody = ""; // Crear cadena de string que contendra el codigo HTML para ingresar los datos del ORM o actividad consultada 

}