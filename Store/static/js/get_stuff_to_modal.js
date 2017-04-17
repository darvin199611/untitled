$('#get_stuff_form').on('submit', function (event) {
    event.preventDefault(); //останавливает стандартное поведение (перезагрузку страницы)
    var stuff_pk = $('#stuff_pk').val();
    var market_id = $('#market_id').val();
    $('#modal_form').data("stuff_pk", stuff_pk);
    get_stuff(stuff_pk, market_id);

});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// AJAX for posting
function get_stuff(stuff_pk, market_id) {
    //noinspection JSDuplicatedDeclaration
    $.ajax({
        url: "/get_stuff/", // the endpoint
        type: "POST", // http method
        data: {
            stuff_pk: stuff_pk,
            market_id: market_id
        }, // data sent with the post request

        // handle a successful response
        success: function (json) {
            // remove the value from the input
            $("#stuffname").html("Товар : " + json.stuffs.name);
            $("#stuffimage").html("<p><img src=/media/" + json.stuffs.picture + " align='left' alt='изображение отсутствует'/></p>");
            $("#stuffdescription").html("<textarea readonly='readonly'>"+json.stuffs.description+"</textarea>");
            $("#stuffamount").html("Количество на складе : " + json.stuffs.amount);
            $("#stuffprice").html("Цена: " + json.stuffs.price);
            showmodal();

        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            $('#results').html("<div class='alert alert-danger'>Ошибка : такого товара нет в магазине!" +
                "<a href='' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + err); // provide a bit more info about the error to the console
        }
    });
}
