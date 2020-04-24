
// --------------------------------------------------------
// Globals
// --------------------------------------------------------

var path_contacts = '/contacts';
var path_export = '/export';

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
// GET CHECKED
// --------------------------------------------------------
function getChecked() {
    var ids = [];

    $('.contact_check').each(function() {
        if( $(this).prop('checked') ) {
            ids.push( $(this).attr('data-id') );
        }
    });

    return( ids );
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

        if(search) window.location.href = path_contacts + '/search/' + search;        
        return false;
    });

    // run autocompletion on tag input
    if( $('#contact_tags').length ) {
        // https://github.com/amsify42/jquery.amsify.suggestags#suggestions-through-ajax
        $.getJSON( path_export + '/tags', function(data) {
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

    // export contact as vCard
    if( $('.vcard_btn').length ) {
        $('.vcard_btn').click( function(event){
            event.preventDefault();
            window.location.href = path_export + '/vcard/' + $(this).attr('data-id'); 
        });
    }

    // check/uncheck all contacts
    if( $('#contact_checkall').length ) {
        $('#contact_checkall').click( function(event){
            flag = $('#contact_checkall').prop('checked');
            $('.contact_check').each(function() {
                $(this).prop('checked',flag);
            });
        });
    }

    // bulk - export json
    if( $('#bulk_export_json').length ) {
        $('#bulk_export_json').click( function(event){
            event.preventDefault();
            // get contacts ids
            ids = getChecked()
            // submit form
            $('#bulk_export_format').val('json');
            $('#bulk_export_contacts').val(ids);
            $('#bulk_export_form').submit();
        });
    }

    // bulk - export csv
    if( $('#bulk_export_csv').length ) {
        $('#bulk_export_csv').click( function(event){
            event.preventDefault();
            // get contacts ids
            ids = getChecked()
            // submit form
            $('#bulk_export_format').val('csv');
            $('#bulk_export_contacts').val(ids);
            $('#bulk_export_form').submit();
        });
    }

    // bulk - add tags
    if( $('#bulk_tag_add').length ) {
        $('#bulk_tag_add').click( function(event){
            event.preventDefault();
            // get contacts ids
            ids = getChecked()
            // call bulk function
            $.post( path_contacts + '/bulk', {
                method: 'add',
                contacts: ids,
                tags: $('#actions_tags').val()
            }, function(data, status){
                window.location.href = '/';
            });
        });
    }

    // bulk - del tags
    if( $('#bulk_tag_del').length ) {
        $('#bulk_tag_del').click( function(event){
            event.preventDefault();
            // get contacts ids
            ids = getChecked()
            // call bulk function
            $.post( path_contacts + '/bulk', {
                method: 'del',
                contacts: ids,
                tags: $('#actions_tags').val()
            }, function(data, status){
                window.location.href = '/';
            });
        });
    }

    // actions - input tags autocompletion
    if( $('#actions_tags').length ) {
        $.getJSON( path_export + '/tags', function(data) {
            $('input[name="actions_tags"]').amsifySuggestags({
                suggestions: data['tags'],
                defaultTagClass: 'btn-sm',
            },'refresh');
        });
    }


});

