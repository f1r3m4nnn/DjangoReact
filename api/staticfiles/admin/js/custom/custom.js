window.onload = function() {
    // Adicione um ouvinte de eventos a cada elemento <select> em seus detalhes de pedido
    document.querySelectorAll("[id^='id_details-']").forEach(function(selectElement) {
        selectElement.onchange = function() {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/items/' + this.value + '/');
            xhr.onload = function() {
                if (xhr.status === 200) {
                    var item = JSON.parse(xhr.responseText);
                    
                    // Busque o campo de preço de venda correspondente e defina seu valor
                    var priceFieldId = 'id_' + selectElement.id.split('-').slice(0, -1).join('-') + '-price_at_sale';
                    document.getElementById(priceFieldId).value = item.price;
                }
            };
            xhr.send();
        };
    });
};