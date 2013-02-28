uidev.views.Page = Backbone.View.extend({

	el: $('body'),

	events: {
	},

	tpl: '',

	initialize: function() {
		// NOTE: Override these method from a subclass ideally
	},

	setUp: function() {
		var self = this;

		if (_.isUndefined(this.options.slug)) {
			this.options.slug = 'home';
		}

		uidev.log('Page.setUp called');

		return this.setUpHeader();
	},

	setUpHeader: function() {
		var self = this,
			selected = this.getSelectedItem();

		this.applyTemplate(this.options.slug);
		uidev.log('page rendered with slug: '+this.options.slug);

		this.setMenuCurrent(selected);

		return $('document').attr('title', globals.pageTitle);
	},

	getPageData: function() {
		var self = this, slug;
		return _.find(PAGES.models, function(el) {
			(el.get('slug').length > 0) ? slug = el.get('slug') : slug = 'home';
			return slug === self.options.slug;
		})
	},

	buildContext: function(data) {
		// build context for js tpl
		(_.isUndefined(this.context)) ?
			this.context = globals:
			$.extend(this.context, globals);

		$.extend(this.context, data);

		return this.context;
	},

	applyTemplate: function(slug) {
		var self = this;
		if (!slug) {
			slug = this.options.slug;
		}

		// render the template for the article content
		var template = Mustache.template(slug),
			pageData = self.getPageData().attributes;

		// add this pages content from backend
		if (pageData.content) {
			this.tpl += pageData.content;
		};

		this.buildContext({'page': pageData});
		// globals is set in base html tpl

		this.tpl += template.render(self.context);
		uidev.log('Applying template with slug: '+ slug);
		uidev.log('HTML: '+ this.tpl.replace(/\n/g,''));

		return $(this.el).find('article').hide().html(this.tpl).fadeIn('fast');
	},

	getSelectedItem: function() {
		var self = this;
		return _.filter(this.$('nav li'), function(el) {
			return el.className === self.options.slug;
		});
	},

	setMenuCurrent: function(elem) {
		this.$('nav li a').removeClass('active');
		return $(elem).find('a').addClass('active');
	}

});
