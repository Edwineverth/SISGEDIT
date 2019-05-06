// Generacion de tabla a partir de los datos obtenidos del ORM 
var fechasemana = {}
var contador = 0

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

/* 01:
Generación de tabla de actividades a partir de las actividades estaticas
ingresadas en el sistema dentro de la tabla actividad
*/
function generarTabla() {

    // Obtencion de los datos de la semana por mes y semana de año
    let semanames_select = document.getElementById('semana_select');
    let semanames = semanames_select.options[semanames_select.selectedIndex].id;
    let semana = document.getElementById('semana').innerHTML;
    //semana = '15'
    // Generar una arreglo de datos que contiene el numero de la semana por mes y el numero de la semana por año
    let semana_mes_data = { 'semana_mes': semanames, 'semana': semana }

    console.log(semana_mes_data)
    // Creacion de AJAX para envio de datos para obtener las actividades correspondeientes al numero de semana por mes y por año
    $.ajax({
        type: "get",
        url: "/actividad/planificacion/datostabla",
        data: { "actividad_mes": JSON.stringify(semana_mes_data), 'csrfmiddlewaretoken': '{{ csrf_token }}' },
        success: function (data) {
            if (data['result'] == "OK") {
                console.log('Proceso completado')
                TablaJson(data) // Se ejecutará en el caso de que el proceso sea completado

            } else {
                console.log(data)
                console.log(data['result'])
                console.log("¡ Error en la transacción ")
            }
        }
    });
}
// Creacion de tabla Jquery para insertar los datos de la consulta ORM, añadiendo los parametros para fecha
function TablaJson(data) {

    console.log(data['existeplanificacion'])

    if (data['existeplanificacion'] == 0) {
        fechasemana = {
            'fechainicio': data['semanames']['fechainicio'],
            'fechafin': data['semanames']['fechafin']
        }
        $("#actividadAdicional").show();
        $("#cronogramaTabla").show();
        $("#guardar_boton").prop('disabled', false);

        $('#mainTable tbody tr').remove(); // Limpiar cada una de las filas que contiene la tabla 
        console.log("entra por json")
        //let contador = 0 // Creacion de contador para obtener el numero de filas
        let nuevaFila = ""; // Crear cadena de string que contendra el codigo HTML para ingresar los datos del ORM o actividad consultada 

        console.log(data['fechasemana'])
        for (let i in data['semana']) {
            nuevaFila = "<tr>";
            nuevaFila += "<td style='" + "text-align:center" + "'> <input type=" + "'checkbox'" + " id=" + "'ch" + (parseInt(i) + contador) + "'" + "class=" + "'chk-col-teal checkbox'" + "/><label for=" + "'ch" + (parseInt(i) + contador) + "'" + "></label> </td>";
            nuevaFila += "<td>" + data['semana'][i]['nombre'] + "</td>";
            nuevaFila += "<td>" + data['semana'][i]['secuencial_cobertura__nombre'] + "</td>";
            nuevaFila += "<td>" + data['semana'][i]['secuencial_usuario__usuario'] + "</td>";
            nuevaFila += "<td>" + data['semana'][i]['secuencial_requerido__nombre'] + "</td>";
            //Creación de los datapiker por cada una de las actividades
            nuevaFila += "<td >";
            nuevaFila += "<input type='date' name='datei" + parseInt(i) + "' id='fechai_" + parseInt(i) + "' class='form-control date' min='" + data['semanames']['fechainicio'] + "' max='" + data['semanames']['fechafin'] + "' placeholder='Ex: 30/07/2016' required>";
            nuevaFila += "</td>";
            nuevaFila += "<td >";
            nuevaFila += "<input type='date' name='datef" + parseInt(i) + "' id='fechaf_" + parseInt(i) + "' class='form-control date' min='" + data['semanames']['fechainicio'] + "' max='" + data['semanames']['fechafin'] + "' placeholder='Ex: 30/07/2016' required>";
            nuevaFila += "</td>";
            nuevaFila += "</tr>";
            contador += (parseInt(i) + 1);
            $("#mainTable tbody").append(nuevaFila);  // Añadir la cadana de string dentro del cuerpo de la tabla   
        }
        console.log(contador)
        // Será activo en el caso de que toque una semana en la cual este vigente una actividad tipo bimestral, timestral, cuatrimestra, semestral y anual
        console.log(data['semanatipo'].length)
        console.log(data['semanatipo'])
        if ((data['semanatipo'].length) >= 1) {
            for (let i in data['semanatipo']) {
                nuevaFila = "<tr>";
                nuevaFila += "<td style='" + "text-align:center" + "'> <input type=" + "'checkbox'" + " id=" + "'ch" + (parseInt(i) + contador) + "'" + "class=" + "'chk-col-teal checkbox'" + "/><label for=" + "'ch" + (parseInt(i) + contador) + "'" + "></label> </td>";
                nuevaFila += "<td>" + data['semanatipo'][i]['nombre'] + "</td>";
                nuevaFila += "<td>" + data['semanatipo'][i]['secuencial_cobertura__nombre'] + "</td>";
                nuevaFila += "<td>" + data['semanatipo'][i]['secuencial_usuario__usuario'] + "</td>";
                nuevaFila += "<td>" + data['semanatipo'][i]['secuencial_requerido__nombre'] + "</td>";
                //Creación de los datapiker por cada una de las actividades
                nuevaFila += "<td >";
                nuevaFila += "<input type='date' name='datei" + (parseInt(i) + contador) + "' id='fechai_" + (parseInt(i) + contador) + "' class='form-control date' min='" + data['semanames']['fechainicio'] + "' max='" + data['semanames']['fechafin'] + "' placeholder='Ex: 30/07/2016' required>";
                nuevaFila += "</td>";
                nuevaFila += "<td >";
                nuevaFila += "<input type='date' name='datef" + (parseInt(i) + contador) + "' id='fechaf_" + (parseInt(i) + contador) + "' class='form-control date' min='" + data['semanames']['fechainicio'] + "' max='" + data['semanames']['fechafin'] + "' placeholder='Ex: 30/07/2016' required>";
                nuevaFila += "</td>";
                nuevaFila += "</tr>";
                contador += i;
                $("#mainTable tbody").append(nuevaFila);
            }
        }
        console.log(data['semanaunica'].length)
        // Será activo en el caso de que existan actividades unicas registradas en el sistema
        if ((data['semanaunica'].length) >= 1) {
            for (let i in data['semanaunica']) {
                nuevaFila = "<tr>";
                nuevaFila += "<td style='" + "text-align:center" + "'> <input type=" + "'checkbox'" + " id=" + "'ch" + (parseInt(i) + contador) + "'" + "class=" + "'chk-col-teal checkbox'" + "/><label for=" + "'ch" + (parseInt(i) + contador) + "'" + "></label> </td>";
                nuevaFila += "<td>" + data['semanaunica'][i]['nombre'] + "</td>";
                nuevaFila += "<td>" + data['semanaunica'][i]['secuencial_cobertura__nombre'] + "</td>";
                nuevaFila += "<td>" + data['semanaunica'][i]['secuencial_usuario__usuario'] + "</td>";
                nuevaFila += "<td>" + data['semanaunica'][i]['secuencial_requerido__nombre'] + "</td>";
                //Creación de los datapiker por cada una de las actividades
                nuevaFila += "<td >";
                nuevaFila += "<input type='date' name='datei" + (parseInt(i) + contador) + "' id='fechai_" + (parseInt(i) + contador) + "' class='form-control date' min='" + data['semanames']['fechainicio'] + "' max='" + data['semanames']['fechafin'] + "' placeholder='Ex: 30/07/2016' required>";
                nuevaFila += "</td>";
                nuevaFila += "<td >";
                nuevaFila += "<input type='date' name='datef" + (parseInt(i) + contador) + "' id='fechaf_" + (parseInt(i) + contador) + "' class='form-control date' min='" + data['semanames']['fechainicio'] + "' max='" + data['semanames']['fechafin'] + "' placeholder='Ex: 30/07/2016' required>";
                nuevaFila += "</td>";
                nuevaFila += "</tr>";
                contador += i;
                $("#mainTable tbody").append(nuevaFila);
            }
        }
        //contador = 0
    } else {
        console.log("no cumple proceso")
        swal("Oops", "Ya existe una planificación generada para esta semana..!", "info")
    }


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


$("#tablaform").submit(function (event) {
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
    let nfilastbody = $("#mainTable tbody tr").length
    console.log(nfilastbody)
    $("#mainTable tbody tr").each(function (index) {
        let actividad, cobertura, responsable, requerido, fechainicio, fechafin, vid;
        $(this).children("td").each(function (index2) { // Recorre cada fila y a su vez cada columna
            // Obtiene el indice de la columna en la que esta para archivar el valor en una variable
            switch (index2) {
                case 1:
                    actividad = $(this).text();
                    break;
                case 2:
                    cobertura = $(this).text();
                    break;
                case 3:
                    responsable = $(this).text();
                    break;
                case 4:
                    requerido = $(this).text();
                    break;
                case 5:
                    $(this).find("input").each(function () {
                        fechainicio = this.value
                        fechainicio_id = this.id
                    });
                    break;
                case 6:
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

        console.log(fecha2.diff(fecha1, 'days'), ' dias de diferencia');

        //console.log(actividad + ' - ' + cobertura + ' - ' + responsable + ' - ' + requerido + ' - ' + fechainicio + ' - ' + fechafin);
        // Añade cada uno de los datos obtenidos de la tabla dentro del arreglo de datos creando un JSON
        if (fecha2.diff(fecha1, 'days') >= 0) {
            console.log('Fila de fechas correctas')
            $('#' + fechainicio_id).css('border-color', '');
            $('#' + fechafin_id).css('border-color', '');
            datos.planificacion.push({
                'actividad': actividad,
                'cobertura': cobertura,
                'responsable': responsable,
                'requerido': requerido,
                'fechainicio': fechainicio,
                'fechafin': fechafin
            });
            bandera += 1;
        } else {
            $('#' + fechainicio_id).css('border-color', 'red');
            $('#' + fechafin_id).css('border-color', 'red');
            showNotification('bg-red', 'Existen fechas fuera de rango. Verificar los datos insertados..!!', 'top', 'right', 'animated fadeInRight', 'animated fadeOutRight');
            bandera -= 0;
        }

    })
    console.log(datos);
    if (bandera == nfilastbody) {
        bandera = 0;
        console.log("Pasa");
        // ejecucion de función Ajax para guardar los datos obtenidos de la tabla
        let csrftoken = getCookie('csrftoken'); // Obtener el Token correspondiente

        $.ajax({
            type: request_method,
            url: post_url,
            data: { 'datosplaning': JSON.stringify(datos), csrfmiddlewaretoken: csrftoken },
            success: function (data) {
                if (data['result'] == "OK") {
                    console.log('Proceso completado')
                    swal("Planificación Creada Correctamente!", "Da Clic en el boton para finalizar!", "success");
                    //swal("Planificación Creada Correctamente!", "Da Clic en el boton para finalizar!", "success");
                    //TablaJson(data) // Se ejecutará en el caso de que el proceso sea completado
                } else {
                    console.log("¡ Error en la transacción ")
                    swal("Oops", "A ocurrido un error en el proceso!: \n Descripción: " + data['error'], "error")
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
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
    } else {
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


function obtenerActividades() {
    let tipoactividad_select = document.getElementById('tipoactividad_select');
    let tipoactividad = tipoactividad_select.options[tipoactividad_select.selectedIndex].id;
    $.ajax({
        type: "get",
        url: "/actividad/planificacion/datosactividad",
        data: { "tipoactividad": JSON.stringify(tipoactividad), 'csrfmiddlewaretoken': '{{ csrf_token }}' },
        success: function (data) {
            if (data['result'] == "OK") {
                console.log('Proceso completado')
                //console.log(data)
                llenarSelectMultiple(data)
            } else {
                console.log("¡ Error en la transacción ")
            }
        }
    }
    );

}


function llenarSelectMultiple(data) {
    $('#optgroup').empty().multiSelect('refresh');

    for (let index = 0; index < data['actividades'].length; index++) {
        $('#optgroup').multiSelect('addOption', {
            value: data['actividades'][index]['secuencial'],
            text: data['actividades'][index]['nombre'] + "-" + data['actividades'][index]['secuencial_usuario__usuario'] + "-" + data['actividades'][index]['secuencial_cobertura__nombre'] + "-" + data['actividades'][index]['secuencial_requerido__nombre']
        });
    }
}


function obtenerActividadesSeleccionadas() {
    let actividadesAdicionales = { 'actividad': [], };
    $('#optgroup :selected').each(function () {
        if (typeof ($(this).text()) != "undefined") {
            //console.log(`Valor indefinido  ${$(this).val()} ${$(this).text()}`)
            actividadesAdicionales.actividad.push({
                "id": $(this).val(),
                "valor": $(this).text(),
            })
        }
    });
    
    let nuevaFila = ""
    if (actividadesAdicionales['actividad'].length > 0) {
        for (let i in actividadesAdicionales['actividad']) {
            let actividadesSplit = (actividadesAdicionales['actividad'][i]['valor']).split("-");
            console.log(!(buscarRepetidosTabla(actividadesSplit[0])))
            if(!(buscarRepetidosTabla(actividadesSplit[0]))){

                nuevaFila = "<tr>";
                nuevaFila += "<td style='" + "text-align:center" + "'> <input type=" + "'checkbox'" + " id=" + "'ch" + (parseInt(i) + contador) + "'" + "class=" + "'chk-col-teal checkbox'" + "/><label for=" + "'ch" + (parseInt(i) + contador) + "'" + "></label> </td>";
                nuevaFila += "<td>" + actividadesSplit[0] + "</td>";
                nuevaFila += "<td>" + actividadesSplit[2] + "</td>";
                nuevaFila += "<td>" + actividadesSplit[1] + "</td>";
                nuevaFila += "<td>" + actividadesSplit[3] + "</td>";
                //Creación de los datapiker por cada una de las actividades
                nuevaFila += "<td >";
                nuevaFila += "<input type='date' name='datei" + (parseInt(i) + contador) + "' id='fechai_" + (parseInt(i) + contador) + "' class='form-control date' min='" + fechasemana['fechainicio'] + "' max='" + fechasemana['fechafin'] + "' placeholder='Ex: 30/07/2016' required>";
                nuevaFila += "</td>";
                nuevaFila += "<td >";
                nuevaFila += "<input type='date' name='datef" + (parseInt(i) + contador) + "' id='fechaf_" + (parseInt(i) + contador) + "' class='form-control date' min='" + fechasemana['fechainicio'] + "' max='" + fechasemana['fechafin'] + "' placeholder='Ex: 30/07/2016' required>";
                nuevaFila += "</td>";
                nuevaFila += "</tr>";
                contador += parseInt(i);
                $("#mainTable tbody").append(nuevaFila);
            }else{
                swal("Oops", "Ya existe una actividad similar ingresada en la tabla..!", "info")
                break;
            }
            
        }
    }
    $('#optgroup').empty().multiSelect('refresh');
    resetInputActividadUnica()
    //contador = 0

}

function actividadCheck() {
    if ($('#actividad_Check').is(":checked")) {
        $("#seleccionarActividad").show();
        $('#actividad_select').prop('disabled', false);

    } else {
        $("#seleccionarActividad").hide();
        $('#actividad_select').prop('disabled', true);
        $("#tipoactividad").css("display", "none");
        $("#actividadunica").css("display", "none");
    }

}

function tipoactividad() {
    $('#optgroup').empty().multiSelect('refresh');
    resetInputActividadUnica()
    let actividad_select = document.getElementById('actividad_select');
    let actividad = actividad_select.options[actividad_select.selectedIndex].value;
    console.log(actividad)
    if (actividad === "Unicas") {
        console.log("entra")
        //$("#actividadunica").show();
        $("#actividadunica").css("display", "block");
        $("#tipoactividad").css("display", "none");
        $("#guardarActividadUnica").prop('disabled', false);
        //$("#tipoactividad").hide();
    } else if (actividad === "Recurrentes") {
        console.log("easdas")
        //$("#actividadunica").hide();
        //$("#tipoactividad").show();
        $("#actividadunica").css("display", "none");
        $("#tipoactividad").css("display", "block");
        $("#guardarActividadUnica").prop('disabled', true);

    }
}

$("#actividadform").submit(function (event) {

    event.preventDefault(); //prevent default action 
    let nombre = document.getElementById("nombre_Text").value;
    let usuario_select = document.getElementById("usuario_select");
    let cobertura_select = document.getElementById("cobertura_select");
    let requerido_select = document.getElementById("requerido_select");
    let nuevaFila = ""
    if (!(buscarRepetidosTabla(nombre))) {
        nuevaFila = "<tr>";
        nuevaFila += "<td style='" + "text-align:center" + "'> <input type=" + "'checkbox'" + " id=" + "'ch" + contador + "'" + "class=" + "'chk-col-teal checkbox'" + "/><label for=" + "'ch" + contador + "'" + "></label> </td>";
        nuevaFila += "<td>" + nombre + "</td>";
        nuevaFila += "<td>" + cobertura_select.options[cobertura_select.selectedIndex].value + "</td>";
        nuevaFila += "<td>" + usuario_select.options[usuario_select.selectedIndex].value + "</td>";
        nuevaFila += "<td>" + requerido_select.options[requerido_select.selectedIndex].value + "</td>";
        //Creación de los datapiker por cada una de las actividades
        nuevaFila += "<td >";
        nuevaFila += "<input type='date' name='datei" + contador + "' id='fechai_" + contador + "' class='form-control date' min='" + fechasemana['fechainicio'] + "' max='" + fechasemana['fechafin'] + "' placeholder='Ex: 30/07/2016' required>";
        nuevaFila += "</td>";
        nuevaFila += "<td >";
        nuevaFila += "<input type='date' name='datef" + contador + "' id='fechaf_" + contador + "' class='form-control date' min='" + fechasemana['fechainicio'] + "' max='" + fechasemana['fechafin'] + "' placeholder='Ex: 30/07/2016' required>";
        nuevaFila += "</td>";
        nuevaFila += "</tr>";
        $("#mainTable tbody").append(nuevaFila);
        contador += 1;
        resetInputActividadUnica();
    } else {
        swal("Oops", "Ya existe una actividad igual ingresada en la tabla..!", "info")
    }


});

function buscarRepetidosTabla(nombre) {
    let retorno = false
    $("#mainTable tbody tr").each(function (index) {
        let actividad
        
        $(this).children("td").each(function (index2) { // Recorre cada fila y a su vez cada columna
            // Obtiene el indice de la columna en la que esta para archivar el valor en una variable
            switch (index2) {
                case 1:
                    actividad = $(this).text();
                    
                    if (actividad == nombre) {
                        retorno = true
                        console.log(actividad)
                    }
                    break;
            }
            if(retorno) return true
        })
        if(retorno) return true
    });
    if(retorno) return true
    else return false
}


function resetInputActividadUnica() {
    $('#nombre_Text').val("");
    $('#descripcion_text').val("");
}


function toggleChecked(status) {
    $(".checkbox").each(function () {
        console.log(status)
        $(this).prop('checked', status);
    })
}

$('.deleteall').on("click", function (event) {
    var tb = $(this).attr('title');
    var sel = false;
    var ch = $('#' + tb).find('tbody input[type=checkbox]');
    var c = confirm('Continue delete?');
    if (c) {
        ch.each(function () {
            var $this = $(this);
            if ($this.is(':checked')) {
                sel = true;	//set to true if there is/are selected row
                $this.parents('tr').fadeOut(function () {
                    $this.remove(); //remove row when animation is finished
                });
                //b.prop('checked', false);
            }
        });
        if (!sel) alert('No data selected');
    }
    return false;
});

