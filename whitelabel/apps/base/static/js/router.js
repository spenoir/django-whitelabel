uidev.Router = Backbone.Router.extend({

	routes: {
		":slug/": "Page",
		"": "Page"
	},

	Page: function(slug) {
		if (_.isUndefined(slug)) {
			slug = 'home';
		}
		uidev.log('routing to slug: '+ slug);

		if (_.isUndefined(uidev.base)) {
			uidev.base = new uidev.views.Base({'slug': slug});
		}

		var viewName = slug.charAt(0).toUpperCase() + slug.substr(1, slug.length),
			view = uidev.views[viewName];
			// here we set a var so that we only load a page tpl once
			(globals.pageLoad) ?
				globals.pageLoad = globals.pageLoad:
				globals.pageLoad = false;
		if (!_.isUndefined(view)) {
			return new view({'slug': slug});
		} else {
			uidev.log('no view found for this slug');
			return false;
		}

	}

});