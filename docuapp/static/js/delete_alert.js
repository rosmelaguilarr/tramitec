function deleteRecord(url, id, queryParams = '', actionType){
    let title, confirmButtonText;

    if (actionType === 'canceled') {
        title = "¿Está seguro de anular?";
        confirmButtonText = "Anular";
    } else if (actionType === 'delete') {
        title = "¿Está seguro de eliminar?";
        confirmButtonText = "Eliminar";
    }

    Swal.fire({
        "title": title,
        "icon": "question",
        "showCancelButton": true,
        "confirmButtonText": confirmButtonText,
        "cancelButtonText": "Cancelar",
        "confirmButtonColor": "#dc3545"
    })
    .then(function(result) {
        if(result.isConfirmed) {
            let fullUrl = `${url}/${id}`
            if (queryParams) {
                fullUrl += `/?${queryParams}`
            }
            window.location.href = fullUrl
        }
    })
}
