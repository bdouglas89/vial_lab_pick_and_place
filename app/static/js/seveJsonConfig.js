// script.js
function saveJson() {
    var jsonText = document.getElementById('jsonInput').value;
    try {
        JSON.parse(jsonText); // Solo para verificar si el JSON es válido
        alert('JSON válido. Cambios guardados.');
    } catch (e) {
        alert('JSON inválido: ' + e.message);
    }
}
