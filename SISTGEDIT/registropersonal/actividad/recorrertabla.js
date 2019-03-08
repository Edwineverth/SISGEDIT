$("#btnRecorrer").click(function () {
    $("#tabla tbody tr").each(function (index) {
        var campo1, campo2, campo3;
        $(this).children("td").each(function (index2) {
            switch (index2) {
                case 0:
                    campo1 = $(this).text();
                    break;
                case 1:
                    campo2 = $(this).text();
                    break;
                case 2:
                    campo3 = $(this).text();
                    break;
            }
            $(this).css("background-color", "#ECF8E0");
        })
        console.log(campo1 + ' - ' + campo2 + ' - ' + campo3);
    })
})
