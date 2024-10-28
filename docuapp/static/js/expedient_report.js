$(document).ready(function() {
    const reportUrl = $('#reportData').data('url');

    const table = $('.datatable').DataTable({
        "language": {
            "url": "/tramitec/static/js/es-ES.json"
        },
        "paging": true,
        "searching": true,
        "ordering": true,
        "info": true,
        'autoWidth': false,
    });

    // Inicio imprimir PDF
    $('#printReport').on('click', function(event) {
        event.preventDefault(); 
        const selectedConditions = [];
        
        $('.filter-checkbox:checked').each(function() {
            selectedConditions.push($(this).val());
        });
        
        const url = $('#reportDataPdf').data('url') + '?condition[]=' + selectedConditions.join('&condition[]=');
        window.open(url, '_blank');
    });
     // Fin imprimir PDF


    function loadData(selectedConditions) {
        $.ajax({
            url: reportUrl,
            method: 'GET',
            data: {
                condition: selectedConditions
            },
            success: function(response) {

                table.clear();

                if (response.expedients && Array.isArray(response.expedients) && response.expedients.length > 0) {
                    response.expedients.forEach(expedient => {
                        const dateAttention = expedient.date_attention ? expedient.date_attention : '-';
                        table.row.add([
                            expedient.exp_code,
                            expedient.created_at,
                            dateAttention,
                            expedient.exp_number,
                            expedient.office,
                            expedient.condition,
                            expedient.user.toUpperCase()
                        ]).draw();
                    });
                } else {
                    console.log("No hay expedientes que mostrar.");
                }
            },
            error: function(xhr, status, error) {
                console.error("An error occurred:", status, error);
                alert("Ocurrió un error al obtener los expedientes.");
            }
        });
    }

    $('.filter-checkbox').on('change', function() {
        const selectedConditions = [];
        $('.filter-checkbox:checked').each(function() {
            selectedConditions.push($(this).val());
        });

        if (selectedConditions.length > 0) {
            loadData(selectedConditions);
        } else {
            table.clear().draw();
        }
    });

    table.clear().draw();
    // loadData([]);
});