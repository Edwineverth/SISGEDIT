// Función Jquery para guardar registro de actividad con los parametros recolectados

function activarSemanas() {
    let valorSeleccion = document.getElementById("recurrencia_select").value;
    //document.getElementById("demo").innerHTML = "You selected: " + valorSeleccion;
    if (valorSeleccion == "Mensuales" | valorSeleccion == "Únicas") {
       console.log("Ingreso de una actividad mensual")
       $("#tablasemana").hide()
        $("#nsemana").show();
    }else{
        console.log("Ingreso de una activididad por otro tipo")
        $("#nsemana").hide();
        $("#tablasemana").show()
    }
   
}

function guardarActividad() {
    let nombre = document.getElementById("nombre_Text").value;
    let descripcion = document.getElementById("descripcion_text").value;
    // Obtención de los datos generales de seleccionador
    let usuario_select = document.getElementById("usuario_select");
    let cobertura_select = document.getElementById("cobertura_select");
    let requerido_select = document.getElementById("requerido_select");
    let recurrencia_select = document.getElementById("recurrencia_select");
    
    let numerosemana = document.getElementById("nsemana_Text").value;
    
    // Extracción de datos de cuadro seleccionador 
    let usuario = usuario_select.options[usuario_select.selectedIndex].id;
    let cobertura = cobertura_select.options[cobertura_select.selectedIndex].id;
    let requerido = requerido_select.options[requerido_select.selectedIndex].id;
    let recurrencia = recurrencia_select.options[recurrencia_select.selectedIndex].id;
    let tabla = document.getElementById('mainTable');
    console.log(usuario)
    // Creación de dato JSON
    let actividad_data = {
        'actividad': [
            {
                'nombre': nombre,
                'descripcion': descripcion,
                'usuario': usuario,
                'cobertura': cobertura,
                'requerido': requerido,
                'recurrencia': recurrencia,
            }
        ],
        'proceso':[],
        'semana':[]
    };
    
    let valorSeleccion = document.getElementById("recurrencia_select").value;
    // Proceso para guardar actividades que tienen un periodo semanal y se realizan
    //cada mes
    if (valorSeleccion == "Mensuales" | valorSeleccion == "Únicas") {
        actividad_data.semana.push({'semana':numerosemana})
        actividad_data.proceso.push({'proceso':1})
        guardarAJAX(actividad_data) // Proceso de envio por GET metodo AJAX, de ser OK el proceso redirecciona
    } else { // En el caso de que sea una actividad por otro periodo.. 
        if (tabla.rows.length>1) {
            actividad_data.proceso.push({'proceso':2})
            for (let iterador = 0+1; tabla.rows[iterador]; iterador++) {
                let semana = document.getElementById("mainTable").rows[iterador].cells[0];
                console.log(semana)
                actividad_data.semana.push({'semana':parseInt(semana.innerHTML)})
            }
            //console.log(actividad_data)
            guardarAJAX(actividad_data);
        } else {
            alert("no hay datos en la tabla")
            
        }
    }
    
}    

//Función para guardar datos mediante petición GET dentro del sistema
function guardarAJAX(actividad_data) {
    $.ajax({
        type: "get",
        url: "/actividad/guardar/",
        data: { 'actividad': JSON.stringify(actividad_data), 'csrfmiddlewaretoken': '{{ csrf_token }}' },
        success: function (data) {
            if (data['result'] == "OK") {
                console.log("¡Registro de persona guardado exitosamente")
                setTimeout("location.href='/actividad/listar'",10)
            } else {
                console.log("¡ Error en la transacción ")
            }
        }
    });
}


$(document).ready(function(){
    /**
     * Funcion para añadir una nueva columna en la tabla
     */
    $("#add").click(function(){
        // Obtenemos el numero de filas (td) que tiene la primera columna
        // (tr) del id "tabla"
        var tds=$("#mainTable tbody tr:first td").length;
        // Obtenemos el total de columnas (tr) del id "mainTable"
        var trs=$("#mainTable tbody tr").length;
        var nuevaFila="<tr>";
        for(var i=0;i<tds;i++){
            // añadimos las columnas
            console.log(i)
            console.log(tds)
            nuevaFila+="<td>columna "+(i+1)+" fila "+(trs+1)+"</td>";
        }
        // Añadimos una columna con el numero total de filas.
        // Añadimos uno al total, ya que cuando cargamos los valores para la
        // columna, todavia no esta añadida
        //nuevaFila+="<td>"+(trs+1)+" filas";
        nuevaFila+="</tr>";
        $("#mainTable tbody").append(nuevaFila);
        $('#mainTable').editableTableWidget();
    });

    /**
     * Funcion para eliminar la ultima columna de la mainTable.
     * Si unicamente queda una columna, esta no sera eliminada
     */
    $("#del").click(function(){
        // Obtenemos el total de columnas (tr) del id "mainTable"
        var trs=$("#mainTable tbody tr").length;
        console.log(trs)
        if(trs>1)
        {
            // Eliminamos la ultima columna
            $("#mainTable tbody tr:last").remove();
        }
    });
});



