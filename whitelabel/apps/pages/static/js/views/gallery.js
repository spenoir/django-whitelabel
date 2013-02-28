uidev.views.Gallery = uidev.views.Page.extend({

	initialize : function() {
		uidev.log('gallery view initialised');

		this.galleryHandler();
	},

	galleryHandler : function() {
		var self = this;

		if (!_.isUndefined(uidev.GALLERY_IMAGES)) {
			this.galleryImagesCollection = uidev.GALLERY_IMAGES;

			this.buildContext({
				'gallery_images': self.galleryImagesCollection.models
			});

			$.each(this.galleryImagesCollection.models, function() {
				self.loadImage(this);
			});

			return this.setUp();

		} else {
			this.galleryImagesCollection = new uidev.GalleryImages();

			$('article').html($('.loading').fadeIn(1000));

			this.galleryImagesCollection.fetch({
				success: function(collection, response, options) {


					self.buildContext({
						'gallery_images': self.galleryImagesCollection.models
					});

					$.each(collection.models, function() {
						self.loadImage(this);
					});

					return self.setUp();
				}
			});

		}

	},

	loadImage : function(imgModel) {
		// very simple img preloading
        var tempImg = new Image();
        tempImg.src = imgModel.get('image');
		return tempImg;
	}
});