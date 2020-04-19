
function go_clic() {
    alert('CLIC');
}

$( document ).ready(function() {

    // $('#search_button').click( function(){
    //     go_clic();
    // });

    $('#search_form').submit( function(event){
        // remove spaces, trailing commas and convert to lowercase
        var tags = $('#search_input').val().replace(/ /g,'').replace(/\,$/,'').toLowerCase();

        if(tags) window.location.href = '/contacts/tag/' + tags;
        
        event.preventDefault();
        return false;
    });

    if ( $("#contact_tags").length ) {
        // https://github.com/amsify42/jquery.amsify.suggestags#suggestions-through-ajax
        $.getJSON( "/ajax/tags", function(data) {
            $('input[name="contact_tags"]').amsifySuggestags({
                // showAllSuggestions: true,
                suggestions: data['tags']
            },'refresh');
        });
    }
});