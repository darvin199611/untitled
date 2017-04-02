function checkLogin(login) {

    if (login != 0) {
        $.ajax({
            type: "GET",
            url: "/check_login/",
            data: {
                username: login,
            },
            dataType: "text",
            cache: false,
            success: function (data) {
                console.log(data);
                if (data == 'yes') {
                    console.log("yes");
                } else if (data == 'no') {
                    console.log("no");
                }
            }


        });
    }

}
