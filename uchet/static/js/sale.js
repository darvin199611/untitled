(function() {
    function loadSubmissions() {
        $.get('/get_market_sales', {
            'market_id': $('#market_id').val()
        }).done(function(data) {
            console.log(data);
            var table = $('#sales');
            table.html('<tr><th>наименование товара</th><th>Цена</th><th>Время</th> </tr>');
            data.submissions.forEach(function(sale) {
                console.log(sale);
                var row = $('<tr>');
                row.append($('<td>').text(sale.stuff));
                row.append($('<td>').text(sale.price));
                row.append($('<td>').text(sale.dt));
                table.prepend(row);
            });
        });
    }

    loadSubmissions();

    // setInterval(loadSubmissions, 5000);
})();
