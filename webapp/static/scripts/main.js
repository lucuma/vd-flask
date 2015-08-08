
window.CSRFToken = $('meta[name="csrf_token"]').attr('content');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        var url = settings.url.replace(location.origin, '');
        var isAbsoluteUrl = /^[a-z0-9]+:\/\/.*/.test(url);
        // Only send the token to relative URLs i.e. locally.
        if (! isAbsoluteUrl) {
            xhr.setRequestHeader("X-CSRFToken", window.CSRFToken);
        }
    }
});


function setupConfirmMessages(){
    var onClick = function(e){
        e.preventDefault();
        e.stopPropagation();
        var $this = $(this);
        var msg = $(this).attr('data-confirm');
        if (!window.confirm(msg)) return;
        
        var action = $(this).attr('href');
        var method = $(this).attr('data-method') || 'post';
        var $form = $('<form></form>')
            .attr('method', method)
            .attr('action', action);
        $('<input type="hidden" name="_csrf_token" />').attr('value', CSRFToken).appendTo($form);
        $form.appendTo('body');
        $form.submit();
    };

    $('a[data-confirm]').on('click', onClick);
}
setupConfirmMessages();

