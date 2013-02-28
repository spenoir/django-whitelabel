uidev.CollectionBase = Backbone.Collection.extend({
	model: null,

	defaultParams: {
		offset:0,
		limit: 10
	},

	initialize: function(models, options) {

		if(!_.isUndefined(options)) {
			this.url = options.url;
		}
	}
});