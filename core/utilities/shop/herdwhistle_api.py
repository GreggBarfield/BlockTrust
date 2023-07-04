import xmlrpc.client
from ...config import HERDWHISTLE_API_KEY, HERDWHISTLE_API_ENDPOINT, HERDWHISTLE_DB, HERDWHISTLE_USERNAME, HERDWHISTLE_INVOICE_ID

class HerdWhistleAPI:

    def __init__(self):
        server_proxy = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(HERDWHISTLE_API_ENDPOINT))
        self.uid = server_proxy.authenticate(HERDWHISTLE_DB, HERDWHISTLE_USERNAME, HERDWHISTLE_API_KEY, {})
        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(HERDWHISTLE_API_ENDPOINT))

    def execute_remote_procedure_call(self, model_name, method_name, parameters):
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
        herdwhistle_customer_shipping_id = self.execute_remote_procedure_call('res.partner', 'create', [customer_details])
        print(herdwhistle_customer_id)
        print(herdwhistle_customer_shipping_id)
        return herdwhistle_customer_id, herdwhistle_customer_shipping_id

    def verify_herdwhistle_customer_credentials(self, herdwhistle_customer_id, herdwhistle_customer_shipping_id):
        herdwhistle_customer_id = self.execute_remote_procedure_call('res.partner', 'search', [[['id', '=', herdwhistle_customer_id]]])
        herdwhistle_customer_shipping_id = self.execute_remote_procedure_call('res.partner', 'search', [[['id', '=', herdwhistle_customer_shipping_id]]])
        if not herdwhistle_customer_id or not herdwhistle_customer_shipping_id:
            return False
        return True

    def create_new_sale_order(self, herdwhistle_customer_id, herdwhistle_customer_shipping_id, products_list):
        product_pricelist = self.execute_remote_procedure_call('product.pricelist', 'search', [[['name', 'ilike', "Blocktrust"]]])
        pricelist_id = product_pricelist[0]
        herdwhistle_products_list = []
        for product in products_list:
            herdwhistle_products_list.append((0, 0, {
                'product_id': product["vendor_product_reference_id"],
                'product_uom_qty': product["quantity"]
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

