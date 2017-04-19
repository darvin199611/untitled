var sale_table = document.getElementById("sale_table");
var created_date = sale_table.getAttribute("data-market-created-date");
var min_date = new Date(created_date);
var on_select_block = false;


var datepicker_from = $('#date_from').datepicker().data('datepicker');
var datepicker_to = $('#date_to').datepicker().data('datepicker');
$('#date_from').datepicker({

    onSelect: function(formattedDate, date, inst) {
        var date_end;
        datepicker_to.update('minDate', date);
        if (datepicker_to.selectedDates[0] === undefined) {
            date_end = datepicker_to.maxDate;
            date_end = date_end.toLocaleDateString();
        }
        else {
              date_end = datepicker_to.selectedDates[0];
              date_end = date_end.toLocaleDateString();
        }
        date_start = date.toLocaleDateString();
        if (on_select_block){return}
        get_sales_by_date(date_start,date_end);
    },
    autoClose: true,
    maxDate: new Date(),
    toggleSelected: false,
    minDate: min_date

});
$('#date_to').datepicker({
    onSelect: function(formattedDate, date, inst) {
        datepicker_from.update('maxDate',date);
        if(datepicker_from.selectedDates[0] === undefined){
            date_start = datepicker_from.minDate;
            date_start = date_start.toLocaleDateString();
        }
        else {
              date_start = datepicker_from.selectedDates[0];
              date_start = date_start.toLocaleDateString();
        }
        date_end = date.toLocaleDateString();
        if (on_select_block){return}
        get_sales_by_date(date_start,date_end);

    },
    maxDate: new Date(),
    autoClose: true,
    todayButton: new Date(),
    toggleSelected: false
});



function get_sales_by_date(date_start,date_end) {
        $.ajax({
            type: "GET",
            url: "/take_sales/",
            data: {
                date_start: date_start,
                date_end: date_end
            },
            cache: false,
            success: function (data) {
    console.log(data);
    var table = $('#sale_table');
    table.html("<thead><tr><th id='sale_table_stuff'>Товар</th><th id='sale_table_price'>Цена</idth><th id='sale_table_time' >Время</th><th>В корзину</th></tr></thead>");
    data.sales.forEach(function (sale) {
        var row = $('<tr>');
        row.append($('<td>').text(sale.stuff));
        row.append($('<td>').text(sale.price));
        row.append($('<td>').text(sale.dt));
        row.append($('<td>').html("<a href='#' class='glyphicon glyphicon-trash sale_trash' data-sale-id ='"+sale.id+"'></a>"));
        table.prepend(row);
    })
}

        });

}

function default_range(range) {
    var dt_from = new Date;
    var dt_to = new Date;
switch (range) {
  case 'today':
    on_select_block = true;
    datepicker_from.selectDate(dt_from);
    on_select_block = false;
    datepicker_to.selectDate(dt_to);
    break;
  case 'week':
    on_select_block = true;
    datepicker_to.selectDate(dt_to);
    dt_from.setDate(dt_from.getDate()-7);
    on_select_block = false;
    datepicker_from.selectDate(dt_from);
    break;
  case 'month':
    on_select_block = true;
    dt_from.setMonth(dt_from.getMonth()-1);
    datepicker_from.selectDate(dt_from);
    on_select_block = false;
    datepicker_to.selectDate(dt_to);
    break;
    case 'all_time':
    on_select_block = true;
    datepicker_from.selectDate(datepicker_from.minDate);
    on_select_block = false;
    datepicker_to.selectDate(datepicker_to.maxDate);
    break;
  default:
    alert('Передано неправильное значение');
}

}

$(document).on('click', "a.sale_trash", function(event) {
    event.preventDefault();
    var is_shure = confirm("Вы Уверены?  продажа будет удалена");
    if(is_shure===true) {
        var crsf_token =$('#csrf_getting_form [name = "csrfmiddlewaretoken"]').val();
        var sale_id = this.getAttribute('data-sale-id');
        var data = {};
        data.sale_id = sale_id;
        data["csrfmiddlewaretoken"] = crsf_token;
        var url ='/delete_sale/';
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                if(data === "yes"){
                    alert('Запись удалена!')
                }
                else {
                    alert('неудача')
                }
                var date_start,date_end;
                if(datepicker_from.selectedDates[0] === undefined){
                    date_start = datepicker_from.minDate;
                    date_start = date_start.toLocaleDateString();
                }
                else {
                    date_start = datepicker_from.selectedDates[0];
                    date_start = date_start.toLocaleDateString();
                    }
                if (datepicker_to.selectedDates[0] === undefined) {
                    date_end = datepicker_to.maxDate;
                    date_end = date_end.toLocaleDateString();
                    }
                else {
                    date_end = datepicker_to.selectedDates[0];
                    date_end = date_end.toLocaleDateString();
                    }
                get_sales_by_date(date_start,date_end)
            }
        });

    }
});
$(document).on('click', "a.date_click", function(event) {
    event.preventDefault();
    var range = this.getAttribute('data-range');
    default_range(range)
});
$(document).on('click', "a.date_click", function(event) {
    event.preventDefault();
    var range = this.getAttribute('data-range');
    default_range(range)
});
