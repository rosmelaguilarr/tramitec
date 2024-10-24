document.addEventListener('DOMContentLoaded', function () {

    var fields = [
        { id: 'exp_search', defaultValue: "", transform: 'toUpperCase' },
        { id: 'id_observation', defaultValue: "NINGUNO", transform: 'toUpperCase' },
        { id: 'id_name', defaultValue: "", transform: 'toUpperCase' },
    ];

    function transformInput(event, transform) {
        if (transform === 'toUpperCase') {
        event.target.value = event.target.value.toUpperCase();
        }
    }

    function handleFocus(event, defaultValue) {
        var element = event.target;
        if (element.value === defaultValue) {
            element.value = "";
            element.style.backgroundColor = ""; // Restablecer color al enfocar
        }
    }

    function handleBlur(event, defaultValue) {
        var element = event.target;
        if (element.value.trim() === "") {
            element.value = defaultValue;
            if (defaultValue === "NINGUNO") {
                element.style.backgroundColor = "#f0f0f0"; // Cambiar color a gris
            }
        }
    }

    fields.forEach(function (field) {
        var element = document.getElementById(field.id);

        if (element) {
        
            if (field.transform === 'toUpperCase') {
                    element.addEventListener('input', function (event) {
                        transformInput(event, field.transform);
                    });
            }
        
            element.addEventListener("focus", function (event) {
                handleFocus(event, field.defaultValue);
            });
        
            element.addEventListener("blur", function (event) {
            handleBlur(event, field.defaultValue);
            });

            if (element.value.trim() === "") {
            element.value = field.defaultValue;
            if (field.defaultValue === "NINGUNO") {
                element.style.backgroundColor = "#f0f0f0";
            }
            }
        }
    });

});