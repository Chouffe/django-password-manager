$(function() {
    var nowTemp = new Date();
    var now = new Date(nowTemp.getFullYear(), nowTemp.getMonth(), nowTemp.getDate(), 0, 0, 0, 0);
    loadTypeAhead();
    $('#generate').click(loadGeneratedPassword);
    hidePasswords();
    $('#show-passwords').click(showPasswords);
    $('.datepicker').datepicker({
        onRender: function(date) {
                return date.valueOf() < now.valueOf() ? 'disabled' : '';
                  }
    });
});



function cleanEntries() {
    $('#table-entries').remove();
}

function fillEntries(entries) {

    cleanEntries();
    if( entries.length == 0) {
        console.log('No entries');
    }
    else {

        // create table
        var $table = $('<table id="table-entries" class="table table-striped">');

        // caption
        // $table.append('<caption>Entry Table</caption>');

        // thead
        $table
        .append('<thead>').children('thead')
        .append('<tr />').children('tr').append('<th>#</th><th>Title</th><th>Url</th><th>Username</th><th>Expires</th><th id="show-passwords">Password <i class="pull-right icon-eye-open"></i></th>');

        //tbody
        var $tbody = $table.append('<tbody />').children('tbody');

        // add row
        for ( var i in entries ) {

            $tbody.append('<tr />').children('tr:last')
            .append("<td><a class='' href=''><i class='icon-cog'></i></a></td>")
            .append("<td>" + entries[i]['title'] + "</td>")
            .append("<td>" + entries[i]['url'] + "</td>")
            .append("<td>" + entries[i]['username'] + "</td>")
            .append("<td>" + entries[i]['expires'] + "</td>")
            .append('<td>' + entries[i]['password'] + "<a class='pull-right' href=''><i class='icon-remove'></i></a></td>");

        }


        // add table to dom
        $table.appendTo('#table-container');
    }

}

function searchEntries(cat) {

    $.getJSON('/api/search.json', { category: cat }).done(function(data) {
        fillEntries(data);
    });
}

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
