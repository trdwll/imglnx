$(function(){
	$('.progress').hide();
	$("#upload_browse").click(function() {
		$("#uploadF").trigger('click');
	});

	$('#upload').fileupload({
		dropZone: $('#drop'),
		send: function(e, data) {
			$('.progress').show();
		},
		progressall: function (e, data) {
			var progress = data.loaded / data.total * 100;
			$('#pbar').css('width', progress+'%').attr('aria-valuenow', progress);
			$('#progress').text(progress.toFixed(2)+'% / 100.00%');
		},
		done: function(e, data) {
			//console.log(data.result);
			if (data.result['status'] == 200) {
				window.location = data.result['image'] != undefined ? data.result['image'] : "/";
			} else { 
				$('#errors').html('<div class="alert alert-danger">'+data.result['error']+'</div>');
			}
			$('.progress').hide();
			$('#progress').empty();
		}
	});

	$("#upload_url").click(function() {
		swal({
			title: "Upload via URL",
			text: "Paste your url here:",
			type: "input",
			showCancelButton: true,
			closeOnConfirm: false,
			animation: "slide-from-top",
			inputPlaceholder: "Type in a URL"
		},
		function(inputValue){
			if (inputValue === false) return false;

			var pattern = /^((http|https):\/\/)/;

			if (inputValue === "" || !pattern.test(inputValue)) {
				swal.showInputError("You need to write a valid URL!");
				return false;
			}

			/* Get rid of the hardcoded url later and change the getElementsByName to something a bit better */
			$.post('/upload/url', { 'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value, 'image': inputValue })
			.done(function(data) {
				console.log(data);
				if (data.error) {
					createAlert('error', data.error);
					return;
				}

				swal({
					title: "Done!",
					text: "The image was uploaded!",
					type: "success"
				},function() {
					window.location = data['image'] != undefined ? data['image'] : "/"
				});
			})
			.fail(function(data) {
				createAlert('error', 'wut');
			});
		});
	});
});