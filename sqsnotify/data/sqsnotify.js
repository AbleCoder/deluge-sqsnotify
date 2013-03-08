SQSNotifyPlugin = Ext.extend(Deluge.Plugin, {
	constructor: function(config) {
		config = Ext.apply({
			name: "SQSNotify"
		}, config);
		SQSNotifyPlugin.superclass.constructor.call(this, config);
	},

	onDisable: function() {
		Deluge.Preferences.removePage(this.prefsPage);
	},

	onEnable: function() {
		this.prefsPage = new ExamplePreferencesPanel();
		this.prefsPage = Deluge.Preferences.addPage(this.prefsPage);
	}
});
new SQSNotifyPlugin();
