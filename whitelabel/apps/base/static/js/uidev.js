(function() {
	return ("uidev" in window && uidev.constructor === Object) ? null : (

		function($) {

			return window.uidev = {

				// useful for getting underscore.js templates
				getTpl: function(tplID, context) {
					return _.template($(tplID).html(), context);
				},

				buildApiUrl: function(resourceName, params) {
					// This function constructs an API url for a given resource
					// It assumes that you always want to append the format=json
					// @resourceName: (String) The name of a tastypie resource [required]
					// @params: (Object) Query string parameters [optional]

					// queries with a q parameter should use the Search API
					if(params && params.q) {
						return ap.buildSearchApiUrl(resourceName, params, no_json);
					}

					if(params && (params.hasOwnProperty('latest_date_gte') || params.hasOwnProperty('latest_date_lte'))) {
						$.extend(params, {'order_by': 'latest_date'});
					}

					var parsedJsonApi = $.url(globals.API_URL),
						newApiUrl = parsedJsonApi.segment(),
						qs = { format: 'json' };

					params = $.extend(params, qs);
					qs = decodeURIComponent($.param(params, true));

					// Push each required resource to the new URL
					$.each(resourceName, function(index, urlPart) {
						newApiUrl.push(urlPart);
					});

					if (newApiUrl.length) {
						return '/' + newApiUrl.join('/') + '/?' + qs; // return '/api/ext/ap/artwork?format=json';
					} else {
						return 'invalid resource name';
					}
				},

				// self initialising function to initialise the app
				initApp: (function() {

					$(document).ready(function() {

						window.app = Backbone.View.extend();

						window.app.router = new uidev.Router();
						Backbone.history.start({pushState: true});
					});

				})(),

				// will be used in log function
				pageStartTime: new Date().getTime(),

				log: function(msg, level) {
					if (globals.DEBUG && window.console) {
						// default log level
						if (typeof(level) == 'undefined') {
							level = 'log';
						}

						var timeDiff = new Date().getTime() - uidev.pageStartTime;

						if (typeof(msg) == 'string') {
							console[level](timeDiff + "ms | " + msg);
						} else {
							console['info']('Non-string log at: ' + timeDiff + "ms");
							console[level](msg);
						}
					}
				},

				vent: _.extend({}, Backbone.Events),

				// maps the 'sub classes' of uidev for namespacing
				views: {}
			}

		}(window.jQuery));

})();