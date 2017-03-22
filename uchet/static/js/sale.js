(function() {
    function loadSubmissions() {
        $.get('/get_market_sales', {
           'market_id': $('#market_id').val()
       }).done(function(data) {
           console.log(data);
           var table = $('#sales');
          table.html('<tr> <th>id товара</th> <th>id магазина</th> <th>название товара</th> <th>date</th> </tr>');
          data.submissions.forEach(function (sale) {
              console.log(sale);
              var row = $('<tr>');
              row.append($('<td>').text(sale.id));
              row.append($('<td>').text(sale.market));
              row.append($('<td>').text(sale.stuff_name));
              row.append($('<td>').text(" tyt budet vremya"));
              table.prepend(row);
          });
      });
   }

  loadSubmissions();

 // setInterval(loadSubmissions, 5000);
})();