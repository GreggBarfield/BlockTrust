import xmlrpc.client
from ...config import HERDWHISTLE_API_KEY, HERDWHISTLE_API_ENDPOINT, HERDWHISTLE_DB, HERDWHISTLE_USERNAME, HERDWHISTLE_INVOICE_ID

class HerdWhistleAPI:

    def __init__(self):
        server_proxy = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(HERDWHISTLE_API_ENDPOINT))
        self.uid = server_proxy.authenticate(HERDWHISTLE_DB, HERDWHISTLE_USERNAME, HERDWHISTLE_API_KEY, {})
        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(HERDWHISTLE_API_ENDPOINT))

    def execute_remote_procedure_call(self, model_name, method_name, parameters, fields=None):
        if fields is not None:
            result = self.models.execute_kw(HERDWHISTLE_DB, self.uid, HERDWHISTLE_API_KEY, model_name, method_name, parameters, fields)
        else:
            result = self.models.execute_kw(HERDWHISTLE_DB, self.uid, HERDWHISTLE_API_KEY, model_name, method_name, parameters)
        return result

    def create_new_herdwhistle_customer_credentials(self, customer_details=None):
        if 'country_id' in customer_details:
            country_id = self.execute_remote_procedure_call('res.country', 'search', [[['name', '=', customer_details["country_id"]]]])
            if country_id:
                customer_details["country_id"] = country_id[0]
            else:
                customer_details["country_id"] = False
        if 'state_id' in customer_details:
            state_id = self.execute_remote_procedure_call('res.country.state', 'search', [[['name', '=', customer_details["state_id"]]]])
            if state_id:
                customer_details["state_id"] = state_id[0]
            else:
                customer_details["state_id"] = False
        herdwhistle_customer_id = self.execute_remote_procedure_call('res.partner', 'create', [customer_details])
        customer_details["parent_id"] = herdwhistle_customer_id
        customer_details["company_type"] = "person"
        customer_details["type"] = "delivery"
        herdwhistle_customer_shipping_id = self.execute_remote_procedure_call('res.partner', 'create', [customer_details])
        return herdwhistle_customer_id, herdwhistle_customer_shipping_id

    def verify_herdwhistle_customer_credentials(self, herdwhistle_customer_id, herdwhistle_customer_shipping_id):
        herdwhistle_customer_id = self.execute_remote_procedure_call('res.partner', 'search', [[['id', '=', herdwhistle_customer_id]]])
        herdwhistle_customer_shipping_id = self.execute_remote_procedure_call('res.partner', 'search', [[['id', '=', herdwhistle_customer_shipping_id]]])
        if not herdwhistle_customer_id or not herdwhistle_customer_shipping_id:
            return False
        return True

    def create_new_sale_order(self, herdwhistle_customer_id, herdwhistle_customer_shipping_id, shopping_cart):
        product_pricelist = self.execute_remote_procedure_call('product.pricelist', 'search', [[['name', 'ilike', "Blocktrust"]]])
        pricelist_id = product_pricelist[0]
        herdwhistle_products_list = []
        for product_details in shopping_cart.values():
            if "vendor_product_reference_id" in product_details:
                herdwhistle_products_list.append((0, 0, {
                    'product_id': product_details["vendor_product_reference_id"],
                    'product_uom_qty': product_details["quantity"]
                }))
        sale_order_parameters = [{
            'partner_id': herdwhistle_customer_id,
            'partner_shipping_id': herdwhistle_customer_shipping_id,
            'partner_invoice_id': HERDWHISTLE_INVOICE_ID,
            'pricelist_id': pricelist_id,
            'order_line': herdwhistle_products_list
        }]
        sale_order_id = self.execute_remote_procedure_call('sale.order', 'create', sale_order_parameters)
        return sale_order_id

    def get_sales_order_details(self, herdwhistle_order_id):
        order_details_fields = {'fields': ['name', 'partner_id', 'partner_shipping_id', 'partner_invoice_id', 'pricelist_id', 'order_line']}
        order_details = self.execute_remote_procedure_call('sale.order', 'read', [herdwhistle_order_id], fields=order_details_fields)
        return order_details

    def get_sale_order_details_with_eids(self, herdwhistle_order_line_id):
        order_details_fields = {'fields': ['product_template_id', 'name', 'product_uom_qty', 'product_uom', 'x_studio_tag_sequence_start', 'x_studio_tag_sequence_end']}
        order_details_with_eids = self.execute_remote_procedure_call('sale.order.line', 'read', [herdwhistle_order_line_id], fields=order_details_fields)
        return order_details_with_eids