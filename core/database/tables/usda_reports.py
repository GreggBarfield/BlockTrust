from .. import database
from ..objects.usda_report import USDAReport


class USDAReportsException(Exception):
    """Generic USDA reports exception."""

    def __init__(self, reason="unspecified"):
        """Constructor for UsersException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)

class USDAReports:
    """Model of a report retrieved from USDA api"""
    
    def __init__(self, db):
        self._db = db
        self._reports = dict()

    def get(self, report_id):
        """Gets a USDA Report by it's id.

        Params:
            report_id: USDAReports's ID

        Returns:
            A USDAReport object on success, or None on no match.
        """
        matching_reports = self._db.execute_d(
            """
                SELECT * FROM usda_report_data
                WHERE
                    id=%(id)s
            """,
            {
                "id": report_id
            }
        )

        if len(matching_reports) != 1:
            raise USDAReportsException()

        return USDAReport(self._db, matching_reports[0])

    def create_report(self, report: USDAReport):
        """Creates a new USDA report

        Params:
            USDAReport: Report to be added to the DB.
        
        Returns:
            The report id to be added to that report object.
        """
        report.validateData()

        result = self._db.execute(
            """
                INSERT INTO usda_report_data
                    (report_date, report_begin_date, report_end_date, 
                    published_date, office_name, office_state, office_city,
                    office_code, market_type, market_type_category, 
                    market_location_name, market_location_state, 
                    market_location_city, slug_id, slug_name, 
                    report_title, report_group, category, commodity, class, 
                    frame, muscle_grade, quality_grade_name, lot_desc, 
                    freight, price_unit, age, pregnancy_stage, weight_collect, 
                    offspring_weight_est, dressing, yield_grade, head_count, 
                    avg_weight_min, avg_weight_max, avg_weight, avg_price_min, 
                    avg_price_max, avg_price, weight_break_low, weight_break_high, 
                    receipts, receipts_week_ago, receipts_year_ago, 
                    comments_commodity, report_narrative, final_ind)
                    VALUES
                        (%(date)s, %(begin_date)s, %(end_date)s, %(publish_date)s, 
                        %(office_name)s, %(office_state)s, %(office_city)s, %(office_code)s,
                        %(market_type)s, %(market_type_category)s, %(market_location_name)s,
                        %(market_location_state)s, %(market_location_city)s, %(slug_id)s, 
                        %(slug_name)s, %(report_title)s, %(group)s, %(category)s, 
                        %(commodity)s, %(class)s, %(frame)s, %(muscle_grade)s, 
                        %(quality_grade_name)s, %(lot_desc)s, %(freight)s, 
                        %(price_unit)s, %(age)s, %(pregnancy_stage)s, 
                        %(weight_collect)s, %(offspring_weight_est)s, %(dressing)s, 
                        %(yield_grade)s, %(head_count)s, %(avg_weight_min)s, 
                        %(avg_weight_max)s, %(avg_weight)s, %(avg_price_min)s, 
                        %(avg_price_max)s, %(avg_price)s, %(weight_break_low)s,
                        %(weight_break_high)s, %(receipts)s, %(receipts_week_ago)s, 
                        %(receipts_year_ago)s, %(comments_commodity)s, %(report_narrative)s, 
                        %(final_ind)s) 
            """,
            {
                "date" : report.reportDate(),
                "begin_date" : report.reportBeginDate(),
                "end_date" : report.reportEndDate(),
                "publish_date" : report.publishedDate(),
                "office_name" : report.officeName(),
                "office_state" : report.officeState(),
                "office_city" : report.officeCity(),
                "office_code" : report.officeCode(),
                "market_type" : report.marketType(),
                "market_type_category" : report.marketTypeCategory(),
                "market_location_name" : report.marketLocationName(),
                "market_location_state" : report.marketLocationState(),
                "market_location_city" : report.marketLocationCity(),
                "slug_id" : report.slugID(),
                "slug_name" : report.slugName(),
                "report_title" : report.reportTitle(),
                "group" : report.group(),
                "category" : report.category(),
                "commodity" : report.commodity(),
                "class" : report.reportClass(),
                "frame" : report.frame(),
                "muscle_grade" : report.muscleGrade(),
                "quality_grade_name" : report.qualityGradeName(),
                "lot_desc" : report.lotDesc(),
                "freight" : report.freight(),
                "price_unit" : report.priceUnit(),
                "age" : report.age(),
                "pregnancy_stage" : report.pregnancyStage(),
                "weight_collect" : report.weightCollect(),
                "offspring_weight_est" : report.offspringWeightEst(),
                "dressing" : report.dressing(),
                "yield_grade" : report.yieldGrade(),
                "head_count" : report.headCount(),
                "avg_weight_min" : report.avgWeightMin(),
                "avg_weight_max" : report.avgWeightMax(),
                "avg_weight" : report.avgWeight(),
                "avg_price_min" : report.avgPriceMin(),
                "avg_price_max" : report.avgPriceMax(),
                "avg_price" : report.avgPrice(),
                "weight_break_low" : report.weightBreakLow(),
                "weight_break_high" : report.weightBreakHigh(),
                "receipts" : report.receipts(),
                "receipts_week_ago" : report.receiptsWeekAgo(),
                "receipts_year_ago" : report.receiptsYearAgo(),
                "comments_commodity" : report.commentsCommodity(),
                "report_narrative" : report.reportNarrative(),
                "final_ind" : report.finalInd(),
            }
        )

        # print("New USDAReport id: " + str(self._db._cursor.lastrowid))
        return self._db._cursor.lastrowid
