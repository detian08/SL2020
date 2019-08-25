odoo.define('pos_sale_agent.agent', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var Chrome = require('point_of_sale.chrome');
    var screens = require('point_of_sale.screens');
    var models = require('point_of_sale.models');
    var core = require('web.core');
    var db = require('point_of_sale.DB');
    var QWeb = core.qweb;
    var _t = core._t;

    QWeb.add_template('/pos_sale_agent/static/src/xml/agent.xml');

    models.load_models({
        model: 'sale.agent',
        fields: ['id', 'name', 'barcode', 'pin','code_agent'],
//    domain: [['team_ids', 'in', []]],
        domain: function (self) {
            return [['team_ids', 'in', [(self.config.crm_team_id) ? self.config.crm_team_id[0] : 0]]];
        },
        loaded: function (self, agents) {
            self.agents = agents;
        },
        after: 'pos.config',
    });

    Chrome.OrderSelectorWidget.include({

        renderElement: function () {
            var self = this;
            this._super();
            this.$el.each(function () {
                if ($(this).is('.agent')) {
                    $(this).click(function (event) {
                        self.click_agent();
                    });
                }
            });
            var agent = this.pos.get_agent();
            if (agent) this.pos.set_agent(agent);
        },

        ask_password: function (password) {
            var self = this;
            var ret = new $.Deferred();
            if (password) {
                this.pos.gui.show_popup('password', {
                    'title': _t('Password ?'),
                    confirm: function (pw) {
                        if (pw !== password) {
                            self.pos.gui.show_popup('error', _t('Incorrect Password'));
                            ret.reject();
                        } else {
                            ret.resolve();
                        }
                    },
                });
            } else {
                ret.resolve();
            }
            return ret;
        },

        select_agent: function (options) {
            options = options || {};
            var self = this;
            var def = new $.Deferred();

            var list = [];
            for (var i = 0; i < this.pos.agents.length; i++) {
                var agent = this.pos.agents[i];
                list.push({
                    'label': agent.name,
                    'item': agent,
                });
            }

            this.pos.gui.show_popup('selection', {
                title: options.title || _t('Select agent'),
                list: list,
                confirm: function (agent) {
                    def.resolve(agent);
                },
                cancel: function () {
                    def.reject();
                },
                is_selected: function (agent) {
                    return agent === self.pos.get_agent();
                },
            });

            return def.then(function (agent) {
                if (options.security && agent !== options.current_agent && agent.pin) {
                    return self.ask_password(agent.pin).then(function () {
                        return agent;
                    });
                } else {
                    return agent;
                }
            });
        },

        click_agent: function () {
            var self = this;
            this.select_agent({
                'security': true,
                'current_agent': this.pos.get_agent(),
                'title': _t('Change Agent'),
            }).then(function (agent) {
                self.pos.set_agent(agent);
                self.renderElement();
            });
        },

    });


    db.include({
        set_agent: function (agent) {
            // Always update if the user is the same as before
            //this.save('agent', agent || null);
            this.save('agent', null);
        },
        get_agent: function () {
            return this.load('agent');
        }
    });
    screens.ReceiptScreenWidget.include({
        click_next: function () {
            //var self = this;
            //console.log("do here what you want");
            //self.pos.set_agent(null);
            ////self.renderElement();
            //
            //return this._super.apply(this, arguments);
            var self = this;
            this._super();
            self.pos.set_agent(null);

        },
    });
    screens.ScreenWidget.include({

        get_agent: function (barcode) {
            for (var i = 0; i < this.pos.agents.length; i++) {
                if (barcode.code && barcode.code === this.pos.agents[i].barcode) {
                    return this.pos.agents[i];
                }
            }
            return null;
        },

//    error_barcode: function(){
//        this.gui.show_popup('error-barcode');
//    },
        barcode_agent_action: function (barcode) {
            var self = this,
                agent = this.get_agent(barcode);
            if (!agent) {
                return;
            }
            self.pos.set_agent(agent);
        },
        show: function () {
            var self = this;
            this._super();
            this.pos.barcode_reader.set_action_callback(
                'agent',
                _.bind(self.barcode_agent_action, self)
            );

        },
    });


    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var pos = models.PosModel.__super__.initialize.call(this, session, attributes);
            this.set({
                'agent': null,
            });
            var agents = [];
            return pos;
        },
        set_agent: function (agent) {

            if (agent != null) {

                this.set('agent', agent);
                $('.agent').text(agent.name);
                this.db.set_agent(agent);
            }
            else {
                this.set({
                    'agent': null,
                });
                $('.agent').text("Agent");

            }

        },
        get_agent: function () {
            return this.db.get_agent() || this.get('agent');
        },

    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function (attributes, options) {
            _super_order.initialize.apply(this, arguments);
            var agent = this.pos.get_agent();
            this.agent_id = (agent) ? agent.id : null;
        },
        init_from_JSON: function (json) {
            _super_order.init_from_JSON.apply(this, arguments);
            //this.agent_id = json.agent_id;
            var agent = this.pos.get_agent();
            this.agent_id = (agent) ? agent.id : null;
        },
        export_as_JSON: function () {
            var json = _super_order.export_as_JSON.apply(this, arguments);
            //json.agent_id = this.agent_id;
            var agent = this.pos.get_agent();
            json.agent_id = (agent) ? agent.id : null;

            return json;
        },

    });

});