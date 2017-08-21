$(function () {
    var search_group = $('#costum-query-search-group .form-group');
    var search_button = $('#costum-query-search-button');
    var url = window.location.href.split('?')[0];

    $('#costum-query-search-group').keyup(function (e) {
        if (e.keyCode === 13) {
            window.location.href = url + '?' + getQuery(search_group);
        }
    });

    search_button.click(function () {
        window.location.href = url + '?' + getQuery(search_group);
    });
});

function getQuery(search_group) {
    var out = [];
    for (var i = 0 ; i < search_group.length ; i++){
        //out.push([search_group[i].childNodes[1].value, search_group[i].childNodes[3].value])
        out.push(search_group[i].childNodes[1].textContent + '=' + search_group[i].childNodes[3].value);
    }
    return out.join('&');
}