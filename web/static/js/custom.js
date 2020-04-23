
// --------------------------------------------------------
// Globals
// --------------------------------------------------------

var exportpath = '/export';

// --------------------------------------------------------
// CONFIRM DIALOG
// https://learnersbucket.com/examples/bootstrap4/custom-confirm-box-with-bootstrap/
// --------------------------------------------------------
function confirmDialog(message,handler) {

    $(`<div class="modal" tabindex="-1" role="dialog" id="confirmModal">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${message}</h5>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-sm btn-success btn-yes text-white">yes</button>
                    <button class="btn btn-sm btn-danger btn-no text-white">no</button>
                </div>
            </div>
        </div>
    </div>`).appendTo('body');

    $("#confirmModal").modal( {backdrop:'static',keyboard:false} );     
    $("#confirmModal").on('hidden.bs.modal', function() { $("#confirmModal").remove(); });

    $(".btn-yes").click( function() { handler(true); $("#confirmModal").modal("hide"); });
    $(".btn-no").click( function() { handler(false); $("#confirmModal").modal("hide"); });
}

// --------------------------------------------------------
// JQUERY READY
// --------------------------------------------------------
$( document ).ready(function() {

    // flash messages timeout
    $('#flash-messages').delay(3000).slideUp(300);

    // run search query
    $('#search_form').submit( function(event){
        event.preventDefault();
        // remove spaces, trailing commas and convert to lowercase
        // var search = $('#search_input').val().replace(/ /g,'').replace(/\,$/,'').toLowerCase();
        var search = $('#search_input').val().toLowerCase();

        if(search) window.location.href = '/contacts/search/' + search;        
        return false;
    });

    // run autocompletion on tag input
    if( $('#contact_tags').length ) {
        // https://github.com/amsify42/jquery.amsify.suggestags#suggestions-through-ajax
        $.getJSON( exportpath + '/tags', function(data) {
            $('input[name="contact_tags"]').amsifySuggestags({
                // showAllSuggestions: true,
                suggestions: data['tags'],
                defaultTagClass: 'btn-sm',
            },'refresh');
        });
    }

    // run confirmation modal
    if( $('.contact_del_btn').length ) {
        $('.contact_del_btn').click( function(event){
            event.preventDefault();
            confirmDialog('do you confirm that contact deletion', (ans) => {
                if(ans) event.currentTarget.form.submit();
            });
        });
    }

    // run confirmation modal
    if( $('.user_del_btn').length ) {
        $('.user_del_btn').click( function(event){
            event.preventDefault();
            confirmDialog('do you confirm that user deletion ?', (ans) => {
                if(ans) event.currentTarget.form.submit();
            });
        });
    }

    if( $('.vcard_btn').length ) {
        $('.vcard_btn').click( function(event){
            event.preventDefault();
            window.location.href = exportpath + '/vcard/' + $(this).attr("data-id"); 
            // $.ajax({
            //     url: exportpath + '/vcard/' + $(this).attr("data-id"),
            //     contentType: "text/directory",

            //     success: function(data){
            //         console.log(data);
            // }});
        });
    }
});

