$(function() {
    $('#logout').click(function() {
        swal({
            title: "Logout?",
            text: "",
            type: "info",
            showCancelButton: true,
            closeOnConfirm: false,
            animation: "slide-from-top",
        }, function(isConfirm) {
            if (!isConfirm) return;
            redirect('/auth/logout');
        });
    });

    /* Probably not the best way to do copy to clipboard, but it's better than throwing js inline. */
    $('.copybtn').click(function() {
        var element = this.name;
        var tmp = $('<input>');
        $("body").append(tmp);
        tmp.val(element).select();
        document.execCommand("copy");
        tmp.remove();
        createAlert('success', 'Copied to clipboard!');
    });
});

function redirect(location, time=1000) {
    window.setTimeout(function() {
        window.location.href = location;
    }, time);
}

function createAlert(type, text, position='bottomRight', time=3000) {
    new Noty({
        type: type,
        text: text,
        layout: position,
        timeout: time,
        progressBar: true,
        closeWith: ['click'],
        animation: {
            open: 'noty_effects_open',
            close: 'noty_effects_close'
        }
    }).show();
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


