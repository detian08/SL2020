odoo.define("pos_hide_search.hide_search", function (require) {
    "use strict";
    var PosBaseWidget = require('point_of_sale.chrome');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');

    var QWeb = core.qweb;

    PosBaseWidget.Chrome.include({
        renderElement:function () {

            var self = this;
            this._super(this);
            this.flag = 1

            if(self.pos.config){
                if(self.pos.config.hide_search){
                      var appBanners = document.getElementsByClassName('searchbox');
                    console.log("self:", appBanners)
                     setTimeout(function(){ 
                    $(window).load(function(){ /*code here*/ })
                     appBanners[0].style.visibility = 'hidden';
                      }, 1000);                
                 }
            }
        }
    });
});