uidev.views.Home = uidev.views.Page.extend({

	initialize : function() {
//		uidev.vent.once('render:home', this.render, this);
		uidev.log('home view initialised');
		this.setUp();
	}
});