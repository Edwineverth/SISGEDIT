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


function recarga(){

}


window.onload = async function() {

    
    
    let arrayData = {}
    let jdata 
    /////////////////////////////////////////TABLAAAAAAAA//////////////////////

    //let thedata = GetPermissions();
    let promise1  = await Promise.resolve(GetPermissions())
    console.log(promise1)
   /* promise1.then(function(value) {
        console.log("imprime un estado");
        
        
        // expected output: 123
      });*/
      jdata = promise1;

        console.log(jdata)
        arrayData = {
            'data': [],
        }
        
        for (let i in jdata['actividades']) {
            arrayData.data.push([String(parseInt(i) + 1), jdata['actividades'][i]['secuencial'], jdata['actividades'][i]['actividad'], jdata['actividades'][i]['fechainicio'], jdata['actividades'][i]['fechafin'], jdata['actividades'][i]['estado']])
        }
     

    let table = $('#example').DataTable({
        data: arrayData.data, // arrayData.data
        columnDefs: [{
            targets: -1,
            data: null,
            defaultContent: "<button>Edit</button>"
        },
        {
            targets: -2,
            data: null,
            defaultContent: "<button type='button' name='btn' id='submitBtn1' class='btn btn-default btnedit1' ><i class='material-icons'>create</i></button>"
        }]
    });
   
    let actividad = null
    $('.btnedit1').each(function () {
        $(this).on('click', function (evt) {
            $this = $(this);
            var dtRow = $this.parents('tr');
            //$('div.modal-body').innerHTML='<div style="border: 1px;border-style: ridge;"><input type="radio" name="radio" id="radio1" /><label for="radio1">TAREA PENDIENTES</label></div><div style="border: 1px;border-style: ridge;"><input type="radio" name="radio" id="radio2" checked /><label for="radio2">TAREA EN CURSO</label></div><div style="border: 1px;border-style: ridge;"><input type="radio" name="radio" id="radio3" /><label for="radio3">TAREA FINALIZADAS</label></div>';
            //$('div.modal-body').append('Row index: '+dtRow[0].rowIndex+'<br/>');
            //$('div.modal-body').append('Number of columns: '+dtRow[0].cells.length+'<br/>');
			/*for(var i=0; i < dtRow[0].cells.length; i++){
				$('div.modal-body').append('Cell (column, row) '+dtRow[0].cells[i]._DT_CellIndex.column+', '+dtRow[0].cells[i]._DT_CellIndex.row+' => innerHTML : '+dtRow[0].cells[i].innerHTML+'<br/>');
            }*/
            //console.log(`El secuencial de la actividad ${dtRow[0].cells[1].innerHTML}`)
            //console.log(`El estado de la actividad ${dtRow[0].cells[5].innerHTML}`)
            actividad = parseInt(dtRow[0].cells[1].innerHTML)
            $('#myModal').modal('show');
        });
    });

    $("#btnsave").click(function () {
        let csrftoken = getCookie('csrftoken');
        let estado = "";
        if ($('#radio1:checked').val() ? true : false)
            estado = "I"
        else if ($('#radio2:checked').val() ? true : false)
            estado = "P"
        else if ($('#radio3:checked').val() ? true : false)
            estado = "T"
        // Crear estrutura JSON
        //console.log(estado)
        let datos = {
            'actividad': parseInt(actividad),
            'estadoactividad': estado
        };


        let parametros = { 'estado': JSON.stringify(datos), 'csrfmiddlewaretoken': csrftoken }

        $.ajax({
            type: 'post',
            url: '/actividad/cambioestado/',
            data: parametros,
            success: function (response) {
                $("#myModal").modal("hide").data('bs.modal', null);
                $('#mainTable').data.reload();
            }
        });


        //$('#example').ajax.reload();


    })

    async function GetPermissions() {
        let arrayData = { }

        console.log("ready!");

        let csrftoken = getCookie('csrftoken');

        let usuario = $("#usuario").text();

        console.log(usuario)

        let datO = { 'usuario': JSON.stringify(usuario), 'csrfmiddlewaretoken': csrftoken }
        const result = await $.ajax({
            type: 'post',
            url: '/actividad/ejecutar/',
            data: datO,
            datatype: 'json',
        })

        return result
    }

};



/*
console.log("ENTRA")
            console.log(data)
            jdata = data;

            arrayData = {
                'data': [],
            }
            
            for (let i in jdata['actividades']) {
                arrayData.data.push([String(parseInt(i) + 1), jdata['actividades'][i]['secuencial'], jdata['actividades'][i]['actividad'], jdata['actividades'][i]['fechainicio'], jdata['actividades'][i]['fechafin'], jdata['actividades'][i]['estado']])
            }
            console.log(arrayData.data)
            return arrayData.data;

*/

Ejemplos
Vuelva a cargar los datos de la tabla cada 30 segundos (restablecimiento de paginación):

Javascript
1
2
3
4 4
5 5
6 6
7 7
var table = $('#example').DataTable( {
    ajax: "data.json"
} );
 
setInterval( function () {
    table.ajax.reload();
}, 30000 );
Vuelva a cargar los datos de la tabla cada 30 segundos (paginación retenida):

Javascript
1
2
3
4 4
5 5
6 6
7 7
var table = $('#example').DataTable( {
    ajax: "data.json"
} );
 
setInterval( function () {
    table.ajax.reload( null, false ); // user paging is not reset on reload
}, 30000 );
Use la devolución de llamada para actualizar elementos externos:

Javascript
1
2
3
4 4
5 5
var table = $('#example').DataTable();
 
table.ajax.reload( function ( json ) {
    $('#myInput').val( json.lastInput );
} );

async function recarga(){
    let arrayData = {}
    let jdata 
    let promise1  = await Promise.resolve(GetPermissions())
    console.log(promise1)
    jdata = promise1;
    arrayData = {
        'data': [],
    }
    for (let i in jdata['actividades']) {
        arrayData.data.push([String(parseInt(i) + 1), jdata['actividades'][i]['secuencial'], jdata['actividades'][i]['actividad'], jdata['actividades'][i]['fechainicio'], jdata['actividades'][i]['fechafin'], jdata['actividades'][i]['estado']])
    }
    return  arrayData.data
}
async function GetPermissions() {
    console.log("ready!");
    let csrftoken = getCookie('csrftoken');

    let usuario = $("#usuario").text();
    let datO = { 'usuario': JSON.stringify(usuario), 'csrfmiddlewaretoken': csrftoken }
    const result = await $.ajax({
        type: 'post',
        url: '/actividad/ejecutar/',
        data: datO,
        datatype: 'json',
    })

    return result
}