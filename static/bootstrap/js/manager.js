$(function() {
    loadTypeAhead();
});

function loadTypeAhead() {

    $.get('/api/entries.json', function(data) {
        console.log(data);
        var data_source = data;
        $('#search').typeahead({source: data_source});
    });
}
