odoo.define('pos_sale_agent.pos_screen',function(require){
"use strict";

var module = require('point_of_sale.models');
var screens = require('point_of_sale.screens');
var PosBaseWidget = require('point_of_sale.BaseWidget');
var core = require('web.core');
var rpc = require('web.rpc');
var models = module.PosModel.prototype.models;
var models = require('point_of_sale.models');
var QWeb = core.qweb;
var _t = core._t;
var gui = require('point_of_sale.gui');


screens.PaymentScreenWidget.include({

    validate_order: function(force_validation) {
         if (this.order_is_valid(force_validation)) {
            console.log(self);
            console.log(this);
        if (this.pos.get_agent()){
            this.finalize_validation();
        }
        else{
        this.gui.show_popup('error',{
                        'title': _t("Agent Not Found"),
                        'body':  _t("The order could not be sent to the server due to an unknown agent.Please select an Agent to validate the order"),
                    });
        }
        }

                }

    });

});