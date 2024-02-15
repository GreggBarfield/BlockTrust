import datetime

def generate_sales_group_search_summary_email_body(user_search_results):
    email_body = """
        <style>
            table.customTable {border-spacing:0 !important;border-collapse:collapse !important;
            table-layout:fixed !important;margin: 0 auto !important;padding: 15 px;}
            table.customTable th{ display:table-cell;vertical-align:middle;font-weight:bold;padding:8px;
            background-color: #88888829;}
            table.customTable td { display: table-cell;padding: 15px; }
        </style>
        <table class="customTable">
            <thead><tr>
            <th>Name</th><th>No. Head</th><th>Category/Sex</th><th>Breed</th>
            <th>Weight</th><th>Market Name/Location</th><th>Sale Date</th>
            </tr></thead><tbody>"""
    for search_result in user_search_results:
        search_result_row = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" %(
            search_result["group_name"],
            search_result["reported"]["count"],
            search_result["category"],
            ",".join(search_result["reported"]["breeds"]),
            search_result["reported"]["weight"],
            search_result["delivery_location"] if search_result["delivery_location_type"] else search_result["delivery_location_type"],
            datetime.datetime.fromtimestamp(search_result["sale_date"]).strftime('%Y-%m-%d')
        )
        email_body += search_result_row
    email_body += "</tbody></table>"
    email_body+="<div><a href='https://blocktrustnetwork.com/login' target='_blank'>Login</a> to see details.</div>"
    return email_body