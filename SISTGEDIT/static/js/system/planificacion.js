function generarTabla(){
    let semanames_select = document.getElementById('semana_select');
    let semanames = semanames_select.options[semanames_select.selectedIndex].id;
    let semana_mes_data = {'semana_mes':semanames}
    $.ajax({
        type: "get",
        url: "/actividad/planificacion/datostabla",
        data: {"actividad_mes":JSON.stringify(semana_mes_data), 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        success: function (data) {
            console.log(data['seamana'])
        }
        }
    );
}