/*Función para guardar registro de usuario dentro del sistema*/
$(function () {
    $('.js-sweetalert button').on('click', function () {
        var type = $(this).data('type');
        console.log("Paso 1 ")
        if (type === 'success') {
            console.log("Paso 2")
            guardarPersonaUsuario();
            showSuccessMessage();
        }
    });
});


function guardarPersonaUsuario() {
    let nombre = document.getElementById("nombre_Text").value;
    let apellido = document.getElementById("apellido_Text").value;
    let usuario = document.getElementById("username_Text").value;
    let password = document.getElementById("password_Text").value;
    let puesto = document.getElementById("puesto_Select");
    let seleccionado = puesto.options[puesto.selectedIndex].value;
    let datos = {
        'person': [{ 'nombre': nombre, 
        'apellido': apellido, 
        'usuario': usuario, 
        'password': password, 
        'puesto': seleccionado }]
    };
    localStorage.setItem = JSON.parse(localStorage.getItem('datos'));
    $.ajax({
        type: "get",
        url: "/insertar/",
        data: {'person':JSON.stringify(datos),'csrfmiddlewaretoken': '{{ csrf_token }}'},
        success: function (data) {
            if (data['result']=="OK") {
                console.log("¡Registro de persona guardado exitosamente")
            }else{
                console.log("¡ Error en la transacción ")
            }
            
        }
    });

}
function showSuccessMessage() {
    swal("Registro Guardado!", "Dar clic en el botón!", "success");
}
