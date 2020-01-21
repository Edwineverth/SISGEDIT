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


let table
let actividad = null

$(document).ready(function () {
    cargaDatos();

    $('#tablaActividad').on('click', 'button', function () {
        console.log($(this).data('name'));
        let dtRow = $(this).parents('tr');
        console.log(dtRow)

        var dtRowo = $(this).parents('tr');
        actividad = parseInt(dtRowo[0].cells[1].innerHTML)
        console.log(actividad)
    });

    $("#tablaActividad").on('click', ".btnedit1", function () {
        //Code 
        console.log('funciona los elementos')
        $this = $(this);
        var dtRow = $this.parents('tr');
        actividad = parseInt(dtRow[0].cells[1].innerHTML)
        $('#modalEstado').modal('show');
    });
    //btnedit2
    $("#tablaActividad").on('click', ".btnedit2", function () {
        //Code 
        console.log('funciona los elementos');
        let csrftoken = getCookie('csrftoken');

        $this = $(this);
        var dtRow = $this.parents('tr');
        actividad = parseInt(dtRow[0].cells[1].innerHTML);
        let parametros = { 'actividad': JSON.stringify(actividad), 'csrfmiddlewaretoken': csrftoken }
        $.ajax({
            type: 'get',
            url: '/actividad/cambioestado/',
            data: parametros,
            success: function (response) {
            }
        });


        $('#modalInforme').modal('show');

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
            }
        });
        $("#modalEstado").modal("hide").data('bs.modal', null);
        $('#tablaActividad').dataTable().api().ajax.reload(null, false);  // Sin recarga de paginación

    });

    

    //TinyMCE
    tinymce.init({
        selector: "textarea#tinymce",
        theme: "modern",
        height: 300,
        plugins: [
            'advlist autolink lists link image charmap print preview hr anchor pagebreak',
            'searchreplace wordcount visualblocks visualchars code fullscreen',
            'insertdatetime media nonbreaking save table contextmenu directionality',
            'emoticons template paste textcolor colorpicker textpattern imagetools'
        ],
        toolbar1: 'insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
        toolbar2: 'print preview media | forecolor backcolor emoticons',
        image_advtab: true
    });
    tinymce.suffix = ".min";
    tinyMCE.baseURL = "/static/plugins/tinymce";
});


function cargaDatos() {
    let csrftoken = getCookie('csrftoken');

    let usuario = $("#usuario").text();
    let dato_Token = { 'usuario': JSON.stringify(usuario), 'csrfmiddlewaretoken': csrftoken }

    $('#tablaActividad').DataTable({
        //*data:  recarga(), // arrayData.data
        ajax: {
            type: 'post',
            url: '/actividad/ejecutar/',
            data: dato_Token,
            datatype: 'json',
            dataSrc: function (json) {
                arrayData = {
                    'data': [],
                }
                //console.log(arrayData)
                for (let i in json['actividades']) {
                    arrayData.data.push([String(parseInt(i) + 1), json['actividades'][i]['secuencial'], json['actividades'][i]['actividad'], json['actividades'][i]['fechainicio'], json['actividades'][i]['fechafin'], json['actividades'][i]['estado']])
                }
                //console.log(arrayData.data)
                return arrayData.data;
            }
        },
        columnDefs: [
            {
                "targets": [5],
                "visible": false,
                "searchable": false
            },
            {
                targets: [-3], render: function (a, b, data, d) {
                    console.log(data)
                    console.log(data[5])
                    if (data[5] == 'I') {
                        console.log('etra')
                        return "<i class='material-icons'>info_outline</i>";
                    }
                    if (data[5] == 'P')
                        return "<i class='material-icons'>history</i>";

                    if (data[5] == 'T')
                        return "<i class='material-icons'>grade</i>";
                    return "<i class='material-icons'>help_outline</i>";
                },
                data: null,
            },
            {
                targets: [-1], render: function (a, b, data, d) {
                    console.log(data)
                    console.log(data[5])
                    if (data[5] == 'I') {
                        console.log('etra')
                        return "<button type='button' name='btn1' class='btn bg-red btnedit2' disabled><i class='material-icons'>print</i></button>";
                    }
                    if (data[5] == 'P')
                        return "<button type='button' name='btn1' class='btn bg-red btnedit2' disabled><i class='material-icons'>print</i></button>";

                    if (data[5] == 'T')
                        return "<button type='button' name='btn1' class='btn bg-green btnedit2' ><i class='material-icons'>print</i></button>";
                    return "<button type='button'>Sin dato</button>";
                },
                data: null,
            },
            {
                targets: -2,
                data: null,
                defaultContent: "<button type='button' name='btn' class='btn btn-default btnedit1' ><i class='material-icons'>create</i></button>"
            }
        ]
    });//cc bg-red
    setInterval(function () {
        $('#tablaActividad').dataTable().api().ajax.reload(null, false); // user paging is not reset on reload
    }, 30000);
}


