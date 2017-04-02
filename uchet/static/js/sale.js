    function loadSales() {
        $.get('/get_market_sales', {
            'market_id': $('#market_id').val()
        }).done(function (data) {
            var table = $('#sales');
            table.html('<thead><tr><th>Товар</th><th>Цена</th><th>Время</th> </tr></thead>');
            data.submissions.forEach(function (sale) {
                var row = $('<tr>');
                row.append($('<td>').text(sale.stuff));
                row.append($('<td>').text(sale.price));
                row.append($('<td>').text(sale.dt));
                table.prepend(row);
            });
        });
    }

    loadSales();
    // setInterval(loadSubmissions, 5000);
