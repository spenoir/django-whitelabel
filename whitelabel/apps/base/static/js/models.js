uidev.BaseModel = Backbone.Model.extend({

	defaultParams: {
		offset:0,
		max_limit: 0
	},
	
	// you shouldn't need to override this method
	url: function() {
		if (this.get('resource_uri')) {
			return this.get('resource_uri');
		} else {
			if (this.get('id')) {
				debugger;
				return uidev.buildApiUrl([this.urlRoot(), this.get('id')], this.defaultParams);
			}
			else {
				return uidev.buildApiUrl([this.urlRoot()], this.defaultParams);
			}
		}
	},

	// override this method to return the specific resource for your model
	urlRoot: function() {
		return 'Please override this method to return a built api url using uidev.buildApiUrl';
	}
});