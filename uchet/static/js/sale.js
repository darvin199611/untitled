(function() {
    function loadSubmissions() {
        $.get('/get_market_sales', {
           'market_id': $('#market_id').val()
       }).done(function(data) {
           var table = $('#submissions');
          table.html('<tr> <th>#</th> <th>Код</th> <th>Статус</th> <th>Комментарий</th> </tr>');
          data.submissions.forEach(function (submission) {
              console.log(submission)
              var row = $('<tr>');
              row.append($('<td>').text(submission.id));
              row.append($('<td>').html($('<pre>').text(submission.market)));
              row.append($('<td>').text(submission.stuff_name));
              row.append($('<td>').text(submission.amount));
              table.prepend(row);
          });
      });
   }

  loadSubmissions();

  setInterval(loadSubmissions, 5000);
})();