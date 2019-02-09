/* While hardcoding urls in here isn't the best - it'll have to do for now. */
$(function(){
	var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;

	/* === Images/Albums === */

	/* Create Album */
	$('#create-album').click(function() {
		swal({
			title: "Create a new Album",
			text: "",
			type: "input",
			showCancelButton: true,
			closeOnConfirm: false,
			animation: "slide-from-top",
			inputPlaceholder: "Type in a name for your Album"
		}, function(inputValue) {
			if (inputValue === false || inputValue.length > 32) return false;

			$.post('/account/albums/', { 'csrfmiddlewaretoken': csrf_token, 'title': inputValue })
			.done(function(data) {
				swal("Done!", "The Album "+inputValue+" was successfully created!", "success");

				redirect('/account/images');
			})
			.fail(function(data) {
				createAlert('error', 'Something went wrong!');
			});
		});
	});

	/* Delete Album */
	$('.delete-album').click(function() {
		var selectedAlbum = this.name;
		swal({
			title: "Delete an album?",
			text: "Are you sure you want to delete the ("+selectedAlbum+") album?",
			type: "info",
			animation: "slide-from-top",
			showCancelButton: true,
			confirmButtonColor: "#DB4105",
			confirmButtonText: "Yes! Delete it!",
			closeOnConfirm: true,
			allowEscapeKey: true,
			allowOutsideClick: true
		}, function(isConfirm) {
			if (!isConfirm) return;

			$.post('/account/albums/delete/', { 'csrfmiddlewaretoken': csrf_token, 'album': selectedAlbum })
			.done(function(data) {
				swal("Done!", selectedAlbum+" was succesfully deleted!", "success");

				redirect('/account/albums/');
			})
			.fail(function(data) {
				createAlert('error', 'Something went wrong!');
			});
		});
	});

	/* Delete Image */
	$('.delete-image').click(function() {
		var name = this.name;
		swal({
			title: "Are you sure you want to delete the image?",
			text: "Once the image (<a href=\"https://i.imglnx.com/"+name+"\"><em>"+name+"</em></a>) has been deleted it's gone for good!",
			type: "error",
			animation: "slide-from-top",
			showCancelButton: true,
			confirmButtonColor: "#DB4105",
			confirmButtonText: "Yes! Delete it!",
			closeOnConfirm: true,
			allowEscapeKey: true,
			allowOutsideClick: true,
			html: true
		}, function(isConfirm) {
			if (!isConfirm) return;
			$.post('/account/images/', { 'csrfmiddlewaretoken': csrf_token, 'images[]': name, 'del': true })
			.done(function(data) {
				swal("Done!", "It was succesfully deleted!", "success");
				var elem = $('.wrapper[name="'+name+'"]');
				elem.fadeOut(2000, function() { $(this).remove(); });
			})
			.fail(function(data) {
				createAlert('error', 'Something went wrong!');
			});
		});
	});

	/* Delete Image from Album */
	$('.remove-image-album').click(function() {
		var selectedImage = this.name;
		swal({
			title: "Remove from album?",
			text: "Are you sure you want to remofe the ("+selectedImage+") from the album?",
			type: "info",
			animation: "slide-from-top",
			showCancelButton: true,
			confirmButtonColor: "#DB4105",
			confirmButtonText: "Yes! Remove it!",
			closeOnConfirm: true,
			allowEscapeKey: true,
			allowOutsideClick: true
		}, function(isConfirm) {
			if (!isConfirm) return;

			$.post('/account/albums/remove/', { 'csrfmiddlewaretoken': csrf_token, 'image': selectedImage })
			.done(function(data) {
				swal("Done!", selectedImage+" was succesfully removed from the album!", "success");

				redirect('/account/albums/');
			})
			.fail(function(data) {
				createAlert('error', 'Something went wrong!');
			});
		});
	});

	/* Add image to album*/
	$('#add-to-album').click(function() {
		var imagesSelected = $(':checkbox:checked:not("#checkAll")').map(function() { return this.name; }).get();
		var album = $('#albums').val();

		if (imagesSelected == null || imagesSelected.length == 0) {
			createAlert('error', 'You didn\'t select any images! You goof ball.');
			return;
		}

		console.log('Selected album: ' + album);
		console.log('Selected images: ' + imagesSelected);
		
		swal({
			title: "Are you sure you want to add the selected images to the album?",
			text: "",
			type: "info",
			animation: "slide-from-top",
			showCancelButton: true,
			confirmButtonColor: "#DB4105",
			confirmButtonText: "Yes!",
			closeOnConfirm: true,
			allowEscapeKey: true,
			allowOutsideClick: true,
			html: true
		}, function(isConfirm) {
			if (isConfirm) {
				if (!isConfirm) return;
				
				$.post('/account/images/add/', { 'csrfmiddlewaretoken': csrf_token, 'images[]': imagesSelected, 'alb': album })
				.done(function(data) {
					swal("Added!", "Your images have been added successfully!", "success");

					redirect('/account/images/');
				})
				.fail(function(data) {
					createAlert('error', 'Something went wrong!');
				});
			} else {
				swal("Cancelled!", "Your images have not been added!", "error");
			}
		});
	});

	/* Delete Selected Images */
	$('#delete-selection').click(function() {
		var imagesSelected = $(':checkbox:checked:not("#checkAll")').map(function() { return this.name; }).get();

		if (imagesSelected == null || imagesSelected.length == 0) {
			createAlert('error', 'You didn\'t select any images! You goof ball.');
			return;
		} else if (imagesSelected.length <= 1) {
			createAlert('error', 'You need to select multiple images to delete them using this button!');
			return;
		}

		console.log('Selected images: ' + imagesSelected);
		
		swal({
			title: "Are you sure you want to delete the selected images?",
			text: "Once the images have been deleted they're gone for good!",
			type: "error",
			animation: "slide-from-top",
			showCancelButton: true,
			confirmButtonColor: "#DB4105",
			confirmButtonText: "Yes! Delete all ("+imagesSelected.length+") of them!",
			closeOnConfirm: true,
			allowEscapeKey: true,
			allowOutsideClick: true,
			html: true
		}, function(isConfirm) {
			if (isConfirm) {
				if (!isConfirm) return;
				
				$.post('/account/images/', { 'csrfmiddlewaretoken': csrf_token, 'images[]': imagesSelected, 'del': true })
				.done(function(data) {
					swal("Deleted!", "Your images have been deleted successfully!", "success");
					$.each(imagesSelected, function(index, value) {
						var elem = $('.wrapper[name="'+value+'"]');
						elem.fadeOut(2000, function() { $(this).remove(); });
					});
				})
				.fail(function(data) {
					createAlert('error', 'Something went wrong!');
				});
			} else {
				swal("Cancelled!", "Your images have not been deleted!", "error");
			}
		});
	});

	/* === Dashboard === */

	/* Download Archive */
	$('#download-archive').click(function() {
		swal({
			title: "Download your archive?",
			text: "This can take a little while since we're going to gather all of your images so please be patient while our cats work hard!",
			type: "info",
			showCancelButton: true,
			confirmButtonColor: "#DD6B55",
			confirmButtonText: "Yes!",
			closeOnConfirm: true
		}, function(isConfirm) {
			if (!isConfirm) return;
			$.post('/account/download/', { 'csrfmiddlewaretoken': csrf_token })
			.done(function(data) {
				swal("Done!", "You've successfully downloaded your archive!", "success");
				
				$.get('/account/download/', { 'csrfmiddlewaretoken': csrf_token })
				.done(function(data) {
					swal("Done!", "You've successfully downloaded your archive!", "success");

					redirect('/account/');
				})
				.fail(function(data) {
					createAlert('error', 'Something went wrong with downloading your archive!');
				});
			})
			.fail(function(data) {
				createAlert('error', 'Something went wrong!');
			});
		});
	});

	/* Delete Account */
	$('#delete-me').click(function() {
		swal({
			title: "kthxbai",
			text: "Once your account and data has been deleted - it's gone for good!",
			type: "warning",
			showCancelButton: true,
			confirmButtonColor: "#DD6B55",
			confirmButtonText: "Yes, delete my account!",
			closeOnConfirm: true
		}, function(isConfirm) {
			if (!isConfirm) return;

			$.post('/account/delete/', { 'csrfmiddlewaretoken': csrf_token })
			.done(function(data) {
				swal("Done!", "Your account has been deleted!", "success");

				redirect('/deleted-account');
			})
			.fail(function(data) {
				createAlert('error', 'Something went wrong!');
			});
		});
	});

	/* Delete API Key */
	$('.delete-api-key').click(function() {
		var key = this.name;
		swal({
			title: "Delete this API Key?",
			text: "",
			type: "info",
			showCancelButton: true,
			confirmButtonColor: "#DD6B55",
			confirmButtonText: "Yes!",
			closeOnConfirm: true
		}, function(isConfirm) {
			if (!isConfirm) return;

			$.post('/api/delete/', { 'csrfmiddlewaretoken':  csrf_token, 'api_key': key })
			.done(function(data) {
				createAlert('success', 'You\'ve successfully deleted your API Key!');
				redirect('/account/');
			})
			.fail(function(data) {
				createAlert('error', 'Something went wrong!');
			});
		});
	});


	/* Miscellaneous */
	$('#checkAll').click(function () {    
		$('input:checkbox').prop('checked', this.checked);    
	});

	$('.toggle-visibility').click(function() {
		var image = this.name;
		$.post('/account/images/change/', { 'image': image, 'csrfmiddlewaretoken': csrf_token })
		.done(function(data) {
			createAlert('success', 'Changed visibility of '+image+'!');

			redirect('/account/images/');
		})
		.fail(function(data) {
			createAlert('error', 'Something went wrong!');
		});
	});
});
