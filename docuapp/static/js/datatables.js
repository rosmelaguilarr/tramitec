// static/js/datatables.js

$(document).ready(function() {
// Inicializar DataTables
const dataTable = $('.datatable').DataTable({
    "language": {
        "url": "/tramitec/static/js/es-ES.json"
    },
    "paging": true,
    "searching": true,
    "ordering": true,
    "info": true,
    'autoWidth': false,
});

dataTable.columns.adjust().draw();

// Aplicar el término de búsqueda al cargar la página
const storedSearchTerm = localStorage.getItem('searchTerm') || '';
dataTable.search(storedSearchTerm).draw();

// Capturar el término de búsqueda actual y guardarlo en localStorage
dataTable.on('search', function () {
    const searchTerm = dataTable.search();
    localStorage.setItem('searchTerm', searchTerm); 
});

// Limpiar el término de búsqueda en localStorage cuando se realice una búsqueda vacía
$('#search-clear-button').on('click', function() {
    localStorage.removeItem('searchTerm');
});

// Enfocar el campo de búsqueda del DataTable
// setTimeout(function() {
//     $('.dataTables_filter input').focus();
// }, 100); 



dataTable.draw();
});
