from copy import deepcopy
from .. import database

class USDAReport:

    def __init__(self, row):
        """USDA Report constructor. 
        There are 48 columns in the row.

        Params:
            db: Database object
            row: A 'usda reports' row dictionary
        """
        self._row = deepcopy(row)

    def id(self):
        return self._id

    def reportDate(self):
        return self._row['report_date']

    def reportBeginDate(self):
        return self._row['report_begin_date']

    def reportEndDate(self):
        return self._row['report_end_date']

    def publishedDate(self):
        return self._row['published_date']

    def officeName(self):
        return self._row['office_name']

    def officeState(self):
        return self._row['office_state']

    def officeCity(self):
        return self._row['office_city']

    def officeCode(self):
        return self._row['office_code']

    def marketType(self):
        return self._row['market_type']

    def marketTypeCategory(self):
        return self._row['market_type_category']

    def marketLocationName(self):
        return self._row['market_location_name']

    def marketLocationState(self):
        return self._row['market_location_state']

    def marketLocationCity(self):
        return self._row['market_location_city']

    def slugID(self):
        return self._row['slug_id']

    def slugName(self):
        return self._row['slug_name']

    def reportTitle(self):
        return self._row['report_title']

    def group(self):
        return self._row['group']

    def category(self):
        return self._row['category']

    def commodity(self):
        return self._row['commodity']

    def reportClass(self):
        return self._row['class']

    def frame(self):
        return self._row['frame']

    def muscleGrade(self):
        return self._row['muscle_grade']

    def qualityGradeName(self):
        return self._row['quality_grade_name']

    def lotDesc(self):
        return self._row['lot_desc']

    def freight(self):
        return self._row['freight']

    def priceUnit(self):
        return self._row['price_unit']

    def age(self):
        return self._row['age']

    def pregnancyStage(self):
        return self._row['pregnancy_stage']

    def weightCollect(self):
        return self._row['weight_collect']

    def offspringWeightEst(self):
        return self._row['offspring_weight_est']

    def dressing(self):
        return self._row['dressing']

    def yieldGrade(self):
        return self._row['yield_grade']

    def headCount(self):
        return self._row['head_count']

    def avgWeightMin(self):
        return self._row['avg_weight_min']

    def avgWeightMax(self):
        return self._row['avg_weight_max']

    def avgWeight(self):
        return self._row['avg_weight']

    def avgPriceMin(self):
        return self._row['avg_price_min']

    def avgPriceMax(self):
        return self._row['avg_price_max']

    def avgPrice(self):
        return self._row['avg_price']

    def weightBreakLow(self):
        return self._row['weight_break_low']

    def weightBreakHigh(self):
        return self._row['weight_break_high']

    def receipts(self):
        return self._row['receipts']

    def receiptsWeekAgo(self):
        return self._row['receipts_week_ago']

    def receiptsYearAgo(self):
        return self._row['receipts_year_ago']

    def commentsCommodity(self):
        return self._row['comments_commodity']

    def reportNarrative(self):
        return self._row['report_narrative']

    def finalInd(self):
        return self._row['final_ind']

    def isNull(self, value):
        return value is None or value == 'null' or value == 'N/A' or value == 'n/a'

    def validateData(self):
        """Checks all the data to make sure None is uniform.
            (i.e. None vs. null vs. N/A)"""
        for item in self._row:
            if(self.isNull(item)):
                item = None
