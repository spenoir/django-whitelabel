uidev.views.Base = Backbone.View.extend({

	el: $('body'),

	events: {
		'click nav li[class!="blog"] a' : 'navClickHandler'
	},

	initialize: function() {
		var self = this;

		this.safeMailto();

		uidev.log('base view rendered with slug: '+this.options.slug);
	},

	safeMailto: function() {
		//safe mailto's
		$('a[href*="[at]"][href*="[dot]"]').each(function() {

			var email = $(this)
				.attr('href')
				.split('[at]')
				.join('@')
				.split('[dot]')
				.join('.');

			$(this).attr('href', 'mailto:' + email.toLowerCase());

			if ($(this).text().length === 0) $(this).text(email);
		});
	},

	navClickHandler: function(event) {
		var self = this;
		if (!_.isUndefined(event)) {
			event.preventDefault();
		}

		this.options.slug = event.currentTarget.parentElement.className;
		// this conditional makes sure we only trigger the router
		// function once
		(_.isUndefined(this.triggerRouter)) ?
			this.triggerRouter = true:
			this.triggerRouter = false;

		return window.app.router.navigate(self.options.slug+'/', {trigger: true});
	}

});
