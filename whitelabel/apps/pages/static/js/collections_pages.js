uidev.Pages = uidev.CollectionBase.extend({

	model: uidev.Page,

	url: function() {
		return uidev.buildApiUrl(['page']);
	}
});

uidev.GalleryImages = uidev.CollectionBase.extend({

	model: uidev.GalleryImage,

	comparator: function(item) {
		var date = new Date(item.get('date'));
		return -date;
	},

	url: function() {
		return uidev.buildApiUrl(['galleryimage']);
	}
});