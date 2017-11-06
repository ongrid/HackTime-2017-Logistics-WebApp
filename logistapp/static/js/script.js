/**
 * Created by proofx on 06.11.17.
 */
$(document).ready(function () {
    $('#confirm_transfer').on('click', function () {
        var from = $('#from').val();
        var to = $('#to').val();
        var item = $('#item_pk').val();
        $.ajax({
            url: '/set_arr_dep/',
            type: 'post',
            dataType: 'html',
            data: {
                item: item,
                from: from,
                to: to
            },
            beforeSend: function () {
                $('#text').text('');
                $('#preloader').show();
                $('#preloader img').show();
            },
            success: function (data) {
                cl(data);
                $('#text').text(data);
                $('#preloader img').hide();
                setTimeout(function () {
                    $('#preloader').hide();
                }, 2000);
            }
        })
    });

    function cl(value) {
        console.log(value);
    }
});