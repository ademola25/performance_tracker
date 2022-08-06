jQuery.expr[':'].Contains = function(a, i, m) {
    return jQuery(a).text().toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
};

$(function() {
    $('#searchField').on('keyup', function() {
        console.log('hello trainee')
        var w = $(this).val();
        if (w) {
            $('#trainees tr').hide();
            $('#trainees tr:Contains('+w+')').show();
        } else {
            $('#trainees tr').show();                  
        }
    });
})
