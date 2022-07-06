$(document).on('submit','#contact-form',function(e){
    e.preventDefault();

    $.ajax({
        type: "POST",

        url: "contact/",
        data: {
            name :$('#name').val(),
            email : $('#email').val(),
            desc :$('#desc').val(),
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
            dataType: "json",
        },
        success: function(response)
        {
            alert(response.msg)
        },

    });
});
