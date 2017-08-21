$(function () {
    // sidebar search response
    $('#sidebar-search-inputgroup').keyup(function (e) {
        if (e.keyCode === 13) {
            window.location.href = '/globalsearch?query=' + $('#sidebar-search-input').val();
        }
    });
    $('#sidebar-search-button').click(function () {
        window.location.href = '/globalsearch?query=' + $('#sidebar-search-input').val();
    });
});
