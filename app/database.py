from config import settings
import pyodbc
from datetime import datetime
from utils import fmt_date

class DB:
    def __init__(self):
        self.connParams = settings.odbc_connection_string
        self.connection = None


    def connect(self):
        self.connection = pyodbc.connect(self.connParams, autocommit=True)

    def disconnect(self):
        self.connection.close()

    def get_trend(self,
                  trend_name: str,
                  start_date: datetime|None = None,
                  end_date: datetime|None = None
                  ) -> dict | None:
        if start_date is None and end_date is None:
            raise Exception('You must specify either start_date or end_date')

        if start_date is None:
            date = end_date
            result = self.get_trend_by_point(trend_name, date)
        elif end_date is None:
            date = start_date
            result = self.get_trend_by_point(trend_name, date)
        else:
            self.connect()
            cursor = self.connection.cursor()
            start_value_sql = f"SELECT ts, value FROM Trend WHERE pv = '{trend_name}' AND ts <= '{fmt_date(start_date)}' ORDER BY ts DESC LIMIT 1;"
            cursor.execute(start_value_sql)
            start_value = cursor.fetchone()
            period_value_sql = f"""
                    SELECT ts, value FROM Trend 
                    WHERE pv = '{trend_name}' AND ts > '{fmt_date(start_date)}' AND ts <= '{fmt_date(end_date)}'
                    ORDER BY ts;
                """
            cursor.execute(period_value_sql)
            period_values = cursor.fetchall()
            result = {trend_name: [{'ts': start_value.ts, 'value': start_value.value}]}
            result[trend_name].extend([{'ts': row.ts, 'value': row.value} for row in period_values])
            self.disconnect()
        return result

    def get_trend_by_point(self,
                      trend_name: str,
                      date: datetime
                      ) -> dict | None:
        sql = f"SELECT ts, value FROM Trend WHERE pv = '{trend_name}' AND ts <= '{fmt_date(date)}' ORDER BY ts DESC LIMIT 1;"
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(sql)
        result = {trend_name: [{'ts': row.ts, 'value': row.value} for row in cursor]}
        self.disconnect()
        return result


