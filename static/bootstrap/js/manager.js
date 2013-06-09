$(function() {

    var nowTemp = new Date();
    var now = new Date(nowTemp.getFullYear(), nowTemp.getMonth(), nowTemp.getDate(), 0, 0, 0, 0);

    loadTypeAhead();
    $('#generate').click(loadGeneratedPassword);

    $('.datepicker').datepicker({
        onRender: function(date) {
                return date.valueOf() < now.valueOf() ? 'disabled' : '';
                  }
    });
    // $('#search').bind('change', searchEntriesByTitle($(this).val()));
    // $('#form-search').submit(function() { return false; });

    // $('#entry_create').click(function() {
    //     $.post("/api/entry/add").done(function(data) {
    //         alert(data);
    //     })
    //     .fail(function() { alert('error'); })
    //     .always(function() { alert('always'); });
    //     $.post("/api/entry/add", { title: "John", password: "2pm", category: 1 } );
    //     .done(function(data) {
    //         alert(data);
    //     });
    //     alert('yo');
    // });
});


/**
 * Main table where passwords are displayed
 *
 */
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
        .append('<tr />').children('tr')
        .append('<th>#</th><th>Title</th><th>Url</th><th>Username</th><th>Expires</th><th id="show-passwords">Password</th>');

        //tbody
        var $tbody = $table.append('<tbody />').children('tbody');

        // add row
        for ( var i in entries ) {

            $tbody.append('<tr />').children('tr:last')
            .append("<td><a href='/entry/update/" + entries[i]['id'] + "' ><i class='icon-cog'></i></a></td>")
            .append("<td>" + entries[i]['title'][0].toUpperCase() + entries[i]['title'].slice(1) + "</td>")
            .append("<td><a href='http://" + entries[i]['url'] + "'>" + entries[i]['url'] + "</a></td>")
            .append("<td>" + entries[i]['username'] + "</td>")
            .append("<td>" + progress_bar_generate(entries[i]['expires']) + "</td>")
            .append('<td onclick="toggleVisibility(this);"><span style="visibility:hidden">' + entries[i]['password'] + "</span><a class='pull-right' href='/entry/delete/" + entries[i]['id'] + "'><i class='icon-remove'></i></a></td>");

        }

        // add table to dom
        $table.appendTo('#table-container');
    }
}

function progress_bar_generate(date_string) {

    var bar = '<div title="' + progress_bar_days_left(date_string) + '" class="progress ' + progress_bar_class(date_string) + ' progress-striped"> <div class="bar " style="width: ' + progress_bar_width(date_string) + '%;"> </div> </div>';
    return bar;

}

function progress_bar_days_left(date_string) {

    if (date_string == 'None') {
        return 'Never';
    }
    else {
        var nowTemp = new Date();
        var now = new Date(nowTemp.getFullYear(), nowTemp.getMonth(), nowTemp.getDate(), 0, 0, 0, 0);
        var data = date_string.split('-');
        var expires = new Date(parseInt(data[0]), parseInt(data[1]-1), parseInt(data[2]));
        // console.log(data);
        // console.log(now);
        // console.log(expires);
        var time = expires.getTime() - now.getTime();
        var one_day = 1000*60*60*24;
        return time / one_day;
    }
}

function progress_bar_width(date_string) {

    var _max = 100;
    var _min = 0;
    var days_left = progress_bar_days_left(date_string);

    if (date_string == 'None') {
        return 100;
    }
    else {
        if (days_left > _max) {
            days_left = _max;
        }
        return (_max - days_left) * 100 / (_max - _min);
    }
}

function progress_bar_class(date_string) {

    var width = progress_bar_width(date_string);
    if (width < 20 || date_string == 'None') {
        return 'progress-success';
    }
    else if(width < 80) {
        return 'progress-warning';
    }
    else {
        return 'progress-danger';
    }
}

function hidePasswords() {
    $('.password-cell').css({'color': 'white'});
}

function showPasswords() {
    $('.password-cell').css({'color': 'black'});
}

function toggleVisibility(elem) {

    if ( $(elem).find('span').css('visibility') == 'hidden' ) {
        $(elem).find('span').css('visibility', 'visible');
    }
    else {
        $(elem).find('span').css('visibility', 'hidden');
    }
}

/**
 * API calls
 *
 */
function searchEntries(cat) {

    $.getJSON('/api/search.json', { category: cat }).done(function(data) {
        fillEntries(data);
    });
}

function searchEntriesByTitle(title) {

    // console.log('ok');
    console.log('title: ' + title);
    // console.log($('#search').val());

    $.getJSON('/api/search.json', { title: title }).done(function(data) {
        fillEntries(data);
    });

}

function loadTypeAhead() {

    $.get('/api/entries.json', function(data) {
        // console.log(data);
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
