import { SalesGroupFields } from "../../../js/sales_groups/sales_group_fields.mjs";

$("#marketing-delivery-location-type").select2({data: SalesGroupFields.commonDeliveryLocationTypes, multiple: false});