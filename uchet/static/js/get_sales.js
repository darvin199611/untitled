
$("#check").click(function() {


    let market_data = $('.market_data');
    $.ajax({
        type: "GET",
        url: "/get_market_sales",
        data: {
            'market_id': market_data.data('market_id'),
        },
        dataType: "Text",
        cache: false,
        success: function(data) {
            console.log(data)

        }

    });
});
