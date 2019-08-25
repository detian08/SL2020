from odoo import api, fields, models, _



class ReportSaleDetails(models.AbstractModel):
  _inherit = 'report.point_of_sale.report_saledetails'

  @api.multi
  def _get_report_values(self, docids, data=None):
    data = dict(data or {})
    config_name = ''
    configs = self.env['pos.config'].browse(data['config_ids'])
    print(configs)
    data.update(self.get_sale_details(data['date_start'], data['date_stop'], configs))
    # data['config_name'] = configs.name
    for con_id in configs:
      if config_name =='':
        config_name = con_id.name
      else:
        config_name += ','+con_id.name
    data['config_name']=config_name
    print("sdsd222", data)
    return data