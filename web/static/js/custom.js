// https://learnersbucket.com/examples/bootstrap4/custom-confirm-box-with-bootstrap/
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

// jQuery ready
$( document ).ready(function() {

    $('#search_form').submit( function(event){
        // remove spaces, trailing commas and convert to lowercase
        // var search = $('#search_input').val().replace(/ /g,'').replace(/\,$/,'').toLowerCase();
        var search = $('#search_input').val().toLowerCase();

        if(search) window.location.href = '/contacts/search/' + search;
        
        event.preventDefault();
        return false;
    });

    if( $('#contact_tags').length ) {
        // https://github.com/amsify42/jquery.amsify.suggestags#suggestions-through-ajax
        $.getJSON( '/ajax/tags', function(data) {
            $('input[name="contact_tags"]').amsifySuggestags({
                // showAllSuggestions: true,
                suggestions: data['tags']
            },'refresh');
        });
    }

    if( $('#test').length ) {
        $('#test').click( function(){
            confirmDialog('are you sure ?', (ans) => {
                if (ans) {
                   console.log("yes");
                } else {
                   console.log("no");
                }
            });
        });
    }

});