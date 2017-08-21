$(function(){
   $('#globalsearch-search-group').keyup(function (e) {
        if (e.keyCode === 13) {
            window.location.href = '/globalsearch?query=' + $('#globalsearch-search-input').val();
        }
    });

    $('#globalsearch-search-button').click(function () {
        window.location.href = '/globalsearch?query=' + $('#globalsearch-search-input').val();
    });
});
