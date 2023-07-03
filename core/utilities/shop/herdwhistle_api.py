import xmlrpc.client
from ...config import HERDWHISTLE_API_KEY, HERDWHISTLE_API_ENDPOINT, HERDWHISTLE_DB, HERDWHISTLE_USERNAME, HERDWHISTLE_INVOICE_ID

class HerdWhistleAPI:

    def __init__(self):
        server_proxy = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(HERDWHISTLE_API_ENDPOINT))
        self.uid = server_proxy.authenticate(HERDWHISTLE_DB, HERDWHISTLE_USERNAME, HERDWHISTLE_API_KEY, {})
        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(HERDWHISTLE_API_ENDPOINT))

    def create_new_herdwhistle_customer_credentials(self, customer_details):
        if 'country_id' in customer_details:
            country_id = self.models.execute_kw(HERDWHISTLE_DB, self.uid, HERDWHISTLE_API_KEY, 'res.country', 'search', [[['name', '=', customer_details["country_id"]]]])
            if country_id:
                customer_details["country_id"] = country_id[0]
            else:
                customer_details["country_id"] = False
        herdwhistle_customer_id = self.models.execute_kw(HERDWHISTLE_DB, self.uid, HERDWHISTLE_API_KEY, 'res.partner', 'create', [customer_details])
        customer_details["parent_id"] = herdwhistle_customer_id
        herdwhistle_customer_shipping_id = self.models.execute_kw(HERDWHISTLE_DB, self.uid, HERDWHISTLE_API_KEY, 'res.partner', 'create', [customer_details])
        print(herdwhistle_customer_id)
        print(herdwhistle_customer_shipping_id)

    def verify_herdwhistle_customer_credentials(self, herdwhistle_customer_id, herdwhistle_customer_shipping_id):
        herdwhistle_customer_id = self.models.execute_kw(HERDWHISTLE_DB, self.uid, HERDWHISTLE_API_KEY, 'res.partner', 'search', [[['id', '=', herdwhistle_customer_id]]])
        herdwhistle_customer_shipping_id = self.models.execute_kw(HERDWHISTLE_DB, self.uid, HERDWHISTLE_API_KEY, 'res.partner', 'search', [[['id', '=', herdwhistle_customer_shipping_id]]])
        if not herdwhistle_customer_id or not herdwhistle_customer_shipping_id:
            return False
        return True