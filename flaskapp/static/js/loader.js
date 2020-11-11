var loader = {
	initialize : function () {
		var html = 
			'<div class="loading-overlay"></div>' +
			'<div class="loading-overlay-image-container">' +
				'<img src="../static/images/loading_image3.gif" class="loading-overlay-img"/>' +
			'</div>';

		// append our html to the DOM body
		$( 'body' ).append( html );
	},
	showLoader : function () {
		jQuery( '.loading-overlay' ).show();
		jQuery( '.loading-overlay-image-container' ).show();
	},
	hideLoader : function () {
		jQuery( '.loading-overlay' ).hide();
		jQuery( '.loading-overlay-image-container' ).hide();
	}
}

function loading() { // do things when the document is ready
    // initialize our loader overlay
    loader.initialize();
    loader.showLoader();
};