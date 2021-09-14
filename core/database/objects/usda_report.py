from copy import deepcopy


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
        if 'report_date' in self._row:
            return self._row['report_date']
        return None

    def reportBeginDate(self):
        if 'report_begin_date' in self._row:
            return self._row['report_begin_date']
        return None

    def reportEndDate(self):
        if 'report_end_date' in self._row:
            return self._row['report_end_date']
        return None

    def publishedDate(self):
        if 'published_date' in self._row:
            return self._row['published_date']
        return None

    def officeName(self):
        if 'office_name' in self._row:
            return self._row['office_name']
        return None

    def officeState(self):
        if 'office_state' in self._row:
            return self._row['office_state']
        return None

    def officeCity(self):
        if 'office_city' in self._row:
            return self._row['office_city']
        return None

    def officeCode(self):
        if 'office_code' in self._row:
            return self._row['office_code']
        return None

    def marketType(self):
        if 'market_type' in self._row:
            return self._row['market_type']
        return None

    def marketTypeCategory(self):
        if 'market_type_category' in self._row:
            return self._row['market_type_category']
        return None

    def marketLocationName(self):
        if 'market_location_name' in self._row:
            return self._row['market_location_name']
        return None

    def marketLocationState(self):
        if 'market_location_state' in self._row:
            return self._row['market_location_state']
        return None

    def marketLocationCity(self):
        if 'market_location_city' in self._row:
            return self._row['market_location_city']
        return None

    def slugID(self):
        return self._row['slug_id']

    def slugName(self):
        if 'slug_name' in self._row:
            return self._row['slug_name']
        return None

    def reportTitle(self):
        if 'report_title' in self._row:
            return self._row['report_title']
        return None

    def group(self):
        if 'group' in self._row:
            return self._row['group']
        return None

    def category(self):
        if 'category' in self._row:
            return self._row['category']
        return None

    def commodity(self):
        if 'commodity' in self._row:
            return self._row['commodity']
        return None

    def reportClass(self):
        if 'class' in self._row:
            return self._row['class']
        return None

    def frame(self):
        if 'frame' in self._row:
            return self._row['frame']
        return None

    def muscleGrade(self):
        if 'muscle_grade' in self._row:
            return self._row['muscle_grade']
        return None

    def qualityGradeName(self):
        if 'quality_grade_name' in self._row:
            return self._row['quality_grade_name']
        return None

    def lotDesc(self):
        if 'lot_desc' in self._row:
            return self._row['lot_desc']
        return None

    def freight(self):
        if 'freight' in self._row:
            return self._row['freight']
        return None

    def priceUnit(self):
        if 'price_unit' in self._row:
            return self._row['price_unit']
        return None

    def age(self):
        if 'age' in self._row:
            return self._row['age']
        return None

    def pregnancyStage(self):
        if 'pregnancy_stage' in self._row:
            return self._row['pregnancy_stage']
        return None

    def weightCollect(self):
        if 'weight_collect' in self._row:
            return self._row['weight_collect']
        return None

    def offspringWeightEst(self):
        if 'offspring_weight_est' in self._row:
            return self._row['offspring_weight_est']
        return None

    def dressing(self):
        if 'dressing' in self._row:
            return self._row['dressing']
        return None

    def yieldGrade(self):
        if 'yield_grade' in self._row:
            return self._row['yield_grade']
        return None

    def headCount(self):
        if 'head_count' in self._row and self._row['head_count'] != None:
            if isinstance(self._row['head_count'], str):
                return self._row['head_count'].replace(',', '')
            else:
                return self._row['head_count']
        return None

    def avgWeightMin(self):
        if 'avg_weight_min' in self._row:
            return self._row['avg_weight_min']
        return None

    def avgWeightMax(self):
        if 'avg_weight_max' in self._row:
            return self._row['avg_weight_max']
        return None

    def avgWeight(self):
        if 'avg_weight' in self._row:
            return self._row['avg_weight']
        return None

    def avgPriceMin(self):
        if 'avg_price_min' in self._row:
            return self._row['avg_price_min']
        return None

    def avgPriceMax(self):
        if 'avg_price_max' in self._row:
            return self._row['avg_price_max']
        return None

    def avgPrice(self):
        if 'avg_price' in self._row:
            return self._row['avg_price']
        return None

    def weightBreakLow(self):
        if 'weight_break_low' in self._row:
            return self._row['weight_break_low']
        return None

    def weightBreakHigh(self):
        if 'weight_break_high' in self._row:
            return self._row['weight_break_high']
        return None

    def receipts(self):
        if 'receipts' in self._row and self._row['receipts'] != None:
            if isinstance(self._row['receipts'], str):
                return self._row['receipts'].replace(',', '')
            else:
                return self._row['receipts']
        return None

    def receiptsWeekAgo(self):
        if 'receipts_week_ago' in self._row and self._row['receipts_week_ago'] != None:
            if isinstance(self._row['receipts_week_ago'], str):
                return self._row['receipts_week_ago'].replace(',', '')
            else:
                return self._row['receipts_week_ago']
        return None

    def receiptsYearAgo(self):
        if 'receipts_year_ago' in self._row and self._row['receipts_year_ago'] != None:
            if isinstance(self._row['receipts_year_ago'], str):
                return self._row['receipts_year_ago'].replace(',', '')
            else:
                return self._row['receipts_year_ago']
        return None

    def commentsCommodity(self):
        if 'comments_commodity' in self._row:
            return self._row['comments_commodity']
        return None

    def reportNarrative(self):
        if 'report_narrative' in self._row:
            return self._row['report_narrative']
        return None

    def finalInd(self):
        if 'final_ind' in self._row:
            return self._row['final_ind']
        return None

    def purchaseSellingDesc(self):
        if 'purchase_selling_desc' in self._row:
            return self._row['purchase_selling_desc']
        return None

    def classDesc(self):
        if 'class_desc' in self._row:
            return self._row['class_desc']
        return None

    def gradeDesc(self):
        if 'grade_desc' in self._row:
            return self._row['grade_desc']
        return None

    def weightRangeLow(self):
        if 'weight_range_low' in self._row and self._row['weight_range_low'] != None:
            if isinstance(self._row['weight_range_low'], str):
                return self._row['weight_range_low'].replace(',', '')
            else:
                return self._row['weight_range_low']
        return None

    def weightRangeHigh(self):
        if 'weight_range_high' in self._row and self._row['weight_range_high'] != None:
            if isinstance(self._row['weight_range_high'], str):
                return self._row['weight_range_high'].replace(',', '')
            else:
                return self._row['weight_range_high']
        return None

    def dressedPct(self):
        if 'dressed_pct' in self._row:
            return self._row['dressed_pct']
        return None

    def priceRangeLow(self):
        if 'price_range_low' in self._row:
            return self._row['price_range_low']
        return None

    def priceRangeHigh(self):
        if 'price_range_high' in self._row:
            return self._row['price_range_high']
        return None

    def wtdAvgPrice(self):
        if 'wtd_avg_price' in self._row:
            return self._row['wtd_avg_price']
        return None

    def region(self):
        if 'region' in self._row:
            return self._row['region']
        return None

    def currentVolume(self):
        if 'current_volume' in self._row:
            if isinstance(self._row['current_volume'], str):
                return self._row['current_volume'].replace(',', '')
            else:
                return self._row['current_volume']
        return None

    def isNull(self, value):
        return value is None or value == 'null' or value == 'N/A' or value == 'n/a'

    def validateData(self):
        """Checks all the data to make sure None is uniform.
            (i.e. None vs. null vs. N/A)"""
        for item in self._row:
            if(self.isNull(item)):
                item = None
