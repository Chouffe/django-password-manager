$(function() {
    loadTypeAhead();
    $('#generate').click(loadGeneratedPassword);
    hidePasswords();
    $('#show-passwords').click(showPasswords);
});

function loadTypeAhead() {

    $.get('/api/entries.json', function(data) {
        console.log(data);
        var data_source = data;
        $('#search').typeahead({source: data_source});
    });
}

function fillInputField(field, value) {
    $(field).val(value);
}

function loadGeneratedPassword() {

    var length = parseInt($("#length").val());
    console.log(length);
    $.get('/api/random_key.json?length='+length, function(data) {
        console.log(data);
        fillInputField('#id_password', data);
    });
}

function hidePasswords() {
    $('.password-cell').css({'color': 'white'});
}

function showPasswords() {
    $('.password-cell').css({'color': 'black'});
}
