$(document).ready(function() {
        var socket = io.connect('http://' + document.domain + ':' + location.port);

        socket.on('send_output', function(msg) {
                $('#shell_output').append(msg);
                $('#shell_output').scrollTop($('#shell_output')[0].scrollHeight);
        });

        $('#shell_input').keypress(function(e) {
                if (e.keyCode == '13') {
                        socket.emit('send_input', $('#shell_input').val());
                        $('#shell_input').val('');
                        return false;
                }
        });
});
