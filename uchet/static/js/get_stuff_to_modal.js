$('#get_post_form').on('submit', function(event){
    event.preventDefault();//останавливает стандартное поведение (перезагрузку страницы)
    var postpk =$('#postpk').val();
    $('#modal_form').data("postpkk",postpk);
    console.log($('#modal_form').data("postpkk"));
    get_post(postpk);

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
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// AJAX for posting
function get_post(postpk) {
    console.log("post is working!") // sanity check
    //noinspection JSDuplicatedDeclaration
    $.ajax({
        url : "get_post/", // the endpoint
        type : "POST", // http method
        data : { postpk : postpk},                  // data sent with the post request

        // handle a successful response
        success :
            function(json) {
            $('#postpk').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success");
            $("#postautor").html("Автор поста : "+ json.posts.author +" :)");
            $("#postnomer").html("<p><img src=/media/"+ json.posts.picture +" align='left' alt='изображение отсутствует' hspace='50' vspace='20'/></p>");
            $("#posttext").html("Текст поста : "+ json.posts.text +" :)");
            $("#postdate").html("дата добавления : "+ json.posts.created +" :)");

            // another sanity check
            showmodal();

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert alert-danger'>Ошибка : такого товара нет в базе! "+
                "<a href='' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": "+err ); // provide a bit more info about the error to the console
        }
    });
}


