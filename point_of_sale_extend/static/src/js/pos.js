odoo.define('point_of_sale_extend.pos', function(require) {
    "use strict";

    var models = require('point_of_sale.models');

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function() {
            _super_order.initialize.apply(this, arguments);
            if (this.pos.config.invoicing_mnd) {
                this.to_invoice = true;
            } else {
                this.to_invoice = false;
            }
        },

    });
});