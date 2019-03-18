// Generacion de tabla a partir de los datos obtenidos del ORM 
function startTime() {
    today = new Date();
    h = today.getHours();
    m = today.getMinutes();
    s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('reloj').innerHTML = h + ":" + m + ":" + s;
    t = setTimeout('startTime()', 500);
}
function checkTime(i) { if (i < 10) { i = "0" + i; } return i; }
window.onload = function () { startTime(); }



function generarTabla(){
    $("#guardar_boton").prop('disabled', false);
    // Obtencion de los datos de la semana por mes y semana de año
    let semanames_select = document.getElementById('semana_select');
    let semanames = semanames_select.options[semanames_select.selectedIndex].id;
    let semana = document.getElementById('semana').innerHTML;
    //semana = '15'
    // Generar una arreglo de datos que contiene el numero de la semana por mes y el numero de la semana por año
    let semana_mes_data = {'semana_mes':semanames, 'semana':semana}
   
    console.log(semana_mes_data)
    // Creacion de AJAX para envio de datos para obtener las actividades correspondeientes al numero de semana por mes y por año
    $.ajax({
        type: "get",
        url: "/actividad/planificacion/datostabla",
        data: {"actividad_mes":JSON.stringify(semana_mes_data), 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        success: function (data) {
            if (data['result'] == "OK") {
                console.log('Proceso completado')
                TablaJson(data) // Se ejecutará en el caso de que el proceso sea completado
            } else {
                console.log("¡ Error en la transacción ")
            }
        }
        }
    );
}
// Creacion de tabla Jquery para insertar los datos de la consulta ORM, añadiendo los parametros para fecha
function TablaJson(data){
    $('#mainTable tbody tr').remove(); // Limpiar cada una de las filas que contiene la tabla 
    console.log("entra por json")
    let contador = 0 // Creacion de contador para obtener el numero de filas
    let nuevaFila=""; // Crear cadena de string que contendra el codigo HTML para ingresar los datos del ORM o actividad consultada 
    
    console.log(data['fechasemana'])
    for(let i in data['semana']){
        nuevaFila="<tr>";
        nuevaFila+="<td>"+ data['semana'][i]['nombre'] +"</td>";
        nuevaFila+="<td>"+ data['semana'][i]['secuencial_cobertura__nombre'] +"</td>";
        nuevaFila+="<td>"+ data['semana'][i]['secuencial_usuario__usuario'] +"</td>";
        nuevaFila+="<td>"+ data['semana'][i]['secuencial_requerido__nombre'] +"</td>";
        //Creación de los datapiker por cada una de las actividades
        nuevaFila+="<td >";
        nuevaFila+="<input type='date' name='datei"+i+"' id='fechai_"+i+"' class='form-control date' min='"+data['semanames']['fechainicio'] +"' max='"+data['semanames']['fechafin'] +"' placeholder='Ex: 30/07/2016' required>";
        nuevaFila+="</td>";
        nuevaFila+="<td >";
        nuevaFila+="<input type='date' name='datef"+i+"' id='fechaf_"+i+"' class='form-control date' min='"+data['semanames']['fechainicio'] +"' max='"+data['semanames']['fechafin'] +"' placeholder='Ex: 30/07/2016' required>";
        nuevaFila+="</td>";
        nuevaFila+="</tr>";
        contador+=(parseInt(i)+1);
        $("#mainTable tbody").append(nuevaFila);  // Añadir la cadana de string dentro del cuerpo de la tabla   
    } 
    console.log(contador)
    // Será activo en el caso de que toque una semana en la cual este vigente una actividad tipo bimestral, timestral, cuatrimestra, semestral y anual
    console.log(data['semanatipo'].length)
    console.log(data['semanatipo'])
    if ((data['semanatipo'].length)>=1) {
        for(let i in data['semanatipo']){
            nuevaFila="<tr>";
            nuevaFila+="<td>"+ data['semanatipo'][i]['nombre'] +"</td>";
            nuevaFila+="<td>"+ data['semanatipo'][i]['secuencial_cobertura__nombre'] +"</td>";
            nuevaFila+="<td>"+ data['semanatipo'][i]['secuencial_usuario__usuario'] +"</td>";
            nuevaFila+="<td>"+ data['semanatipo'][i]['secuencial_requerido__nombre'] +"</td>";
            //Creación de los datapiker por cada una de las actividades
            nuevaFila+="<td >";
            nuevaFila+="<input type='date' name='datei"+(i+contador)+"' id='fechai_"+(i+contador)+"' class='form-control date' min='"+data['semanames']['fechainicio'] +"' max='"+data['semanames']['fechafin'] +"' placeholder='Ex: 30/07/2016' required>";
            nuevaFila+="</td>";
            nuevaFila+="<td >";
            nuevaFila+="<input type='date' name='datef"+(i+contador)+"' id='fechaf_"+(i+contador)+"' class='form-control date' min='"+data['semanames']['fechainicio'] +"' max='"+data['semanames']['fechafin'] +"' placeholder='Ex: 30/07/2016' required>";
            nuevaFila+="</td>";
            nuevaFila+="</tr>";
            contador+=i;
            $("#mainTable tbody").append(nuevaFila);
        }
    }
    console.log(data['semanaunica'].length)
    // Será activo en el caso de que existan actividades unicas registradas en el sistema
    if ((data['semanaunica'].length)>=1) {
        for(let i in data['semanaunica']){
            nuevaFila="<tr>";
            nuevaFila+="<td>"+ data['semanaunica'][i]['nombre'] +"</td>";
            nuevaFila+="<td>"+ data['semanaunica'][i]['secuencial_cobertura__nombre'] +"</td>";
            nuevaFila+="<td>"+ data['semanaunica'][i]['secuencial_usuario__usuario'] +"</td>";
            nuevaFila+="<td>"+ data['semanaunica'][i]['secuencial_requerido__nombre'] +"</td>";
            //Creación de los datapiker por cada una de las actividades
            nuevaFila+="<td >";
            nuevaFila+="<input type='date' name='datei"+(i+contador)+"' id='fechai_"+(i+contador)+"' class='form-control date' min='"+data['semanames']['fechainicio'] +"' max='"+data['semanames']['fechafin'] +"' placeholder='Ex: 30/07/2016' required>";
            nuevaFila+="</td>";
            nuevaFila+="<td >";
            nuevaFila+="<input type='date' name='datef"+(i+contador)+"' id='fechaf_"+(i+contador)+"' class='form-control date' min='"+data['semanames']['fechainicio'] +"' max='"+data['semanames']['fechafin'] +"' placeholder='Ex: 30/07/2016' required>";
            nuevaFila+="</td>";
            nuevaFila+="</tr>";
            contador+=i;
            $("#mainTable tbody").append(nuevaFila);
        }
    }
    contador = 0
    
    //$("#mainTable tbody").append(nuevaFila);

}

//OBTENER EL TOKEN CORRESPONDIENTE
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

  }//end function getCookie


$("#my_form").submit(function(event){
    event.preventDefault(); //prevent default action 
    let post_url = $(this).attr("action"); //get form action url
    let request_method = $(this).attr("method"); //get form GET/POST method
    //var form_data = new FormData(this); //Encode form elements for submission
    let bandera = 0
    
    let semana = document.getElementById('semana').innerHTML;
    let datos = {
        'planificacion': [],
        'semana': parseInt(semana)
    };
    let fechainicio_id
    let fechafin_id
    let nfilastbody =  $("#mainTable tbody tr").length
    console.log(nfilastbody)
    $("#mainTable tbody tr").each(function (index) {
        let actividad, cobertura, responsable, requerido, fechainicio, fechafin, vid;
        $(this).children("td").each(function (index2) { // Recorre cada fila y a su vez cada columna
            // Obtiene el indice de la columna en la que esta para archivar el valor en una variable
            switch (index2) {
                case 0:
                    actividad = $(this).text();
                    break;
                case 1:
                    cobertura = $(this).text();
                    break;
                case 2:
                    responsable = $(this).text();
                    break;
                case 3:
                    requerido = $(this).text();
                    break;
                case 4:
                    $(this).find("input").each(function () {
                        fechainicio = this.value
                        fechainicio_id = this.id
                    });
                    break;
                case 5:
                    $(this).find("input").each(function () {
                        fechafin = this.value
                        fechafin_id = this.id
                    });
                    break;
            }
            //$(this).css("background-color", "#ECF8E0");
        })
        let fecha1 = moment(fechainicio);
        let fecha2 = moment(fechafin);

        //console.log(fecha2.diff(fecha1, 'days'), ' dias de diferencia');

        //console.log(actividad + ' - ' + cobertura + ' - ' + responsable + ' - ' + requerido + ' - ' + fechainicio + ' - ' + fechafin);
        // Añade cada uno de los datos obtenidos de la tabla dentro del arreglo de datos creando un JSON
        if(fecha2.diff(fecha1, 'days')>=0){
            console.log('Fila de fechas correctas')
            $('#'+fechainicio_id).css('border-color', '');
            $('#'+fechafin_id).css('border-color', '');
            datos.planificacion.push({
                'actividad': actividad,
                'cobertura': cobertura,
                'responsable': responsable,
                'requerido': requerido,
                'fechainicio': fechainicio,
                'fechafin': fechafin
            });
            bandera+= 1;
        }else{
            $('#'+fechainicio_id).css('border-color', 'red');
            $('#'+fechafin_id).css('border-color', 'red');
            showNotification('bg-red', 'Existen fechas fuera de rango. Verificar los datos insertados..!!','top', 'right', 'animated fadeInRight', 'animated fadeOutRight');
            bandera-= 0;
        }
        
    })
    console.log(datos);
    if (bandera == nfilastbody){
        bandera = 0; 
        console.log("Pasa");
        // ejecucion de función Ajax para guardar los datos obtenidos de la tabla
        let csrftoken = getCookie('csrftoken'); // Obtener el Token correspondiente
        $.ajax({
            type: request_method,
            url: post_url,
            data: {'datosplaning':JSON.stringify(datos), csrfmiddlewaretoken: csrftoken},
            success: function (data) {
                if (data['result'] == "OK") {
                    console.log('Proceso completado')
                    swal("Planificación Creada Correctamente!", "Da Clic en el boton para finalizar!", "success");
                    //swal("Planificación Creada Correctamente!", "Da Clic en el boton para finalizar!", "success");
                    //TablaJson(data) // Se ejecutará en el caso de que el proceso sea completado
                } else {
                    console.log("¡ Error en la transacción ")
                    swal ( "Oops" ,  "A ocurrido un error en el proceso!: \n Descripción: "+ data['error'] ,  "error" )
                }
            },
            error: function( jqXHR, textStatus, errorThrown ) {
                if (jqXHR.status === 0) {
                    swal("Error al intentar Conectarse: Verifique su conexion a Internet.", "error");
                } else if (jqXHR.status == 404) {
                    swal("La Pagina solicitada no fue encontrada [404].", "error");    
                } else if (jqXHR.status == 500) {
                    swal("Erro Interno [500].", "error");    
                } else if (textStatus === 'parsererror') {
                    swal("Error en el retorno de Datos. [parseJson]", "error");
                } else if (textStatus === 'timeout') {
                    swal('Tiempo de Espera agotado', "error");
                } else if (textStatus === 'abort') {
                    swal("Solicitud Abortada. [Ajax Request].", "error");
                } else {
                    swal('Error desconocido: ' + jqXHR.responseText, "error");
                }//end if 
    
            }//end error
        })
    }else{
        console.log("No se realizaro proceso")
    }
    
    
    
});

function showNotification(colorName, text, placementFrom, placementAlign, animateEnter, animateExit) {
    if (colorName === null || colorName === '') { colorName = 'bg-black'; }
    if (text === null || text === '') { text = 'Turning standard Bootstrap alerts'; }
    if (animateEnter === null || animateEnter === '') { animateEnter = 'animated fadeInDown'; }
    if (animateExit === null || animateExit === '') { animateExit = 'animated fadeOutUp'; }
    var allowDismiss = true;

    $.notify({
        message: text
    },
        {
            type: colorName,
            allow_dismiss: allowDismiss,
            newest_on_top: true,
            timer: 1000,
            placement: {
                from: placementFrom,
                align: placementAlign
            },
            animate: {
                enter: animateEnter,
                exit: animateExit
            },
            template: '<div data-notify="container" class="bootstrap-notify-container alert alert-dismissible {0} ' + (allowDismiss ? "p-r-35" : "") + '" role="alert">' +
            '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
            '<span data-notify="icon"></span> ' +
            '<span data-notify="title">{1}</span> ' +
            '<span data-notify="message">{2}</span>' +
            '<div class="progress" data-notify="progressbar">' +
            '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
            '</div>' +
            '<a href="{3}" target="{4}" data-notify="url"></a>' +
            '</div>'
        });
}