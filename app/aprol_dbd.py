from database import DB
from datetime import datetime
from pprint import pprint

def main():
    db = DB()
    trend1 = db.get_trend(
        'jichai_techno_008_count_and_store_MUX_LREAL',
        start_date=datetime(2025, 10, 1)
    )
    trend2 = db.get_trend(
        'jichai_techno_012_count_and_store_MUX_LREAL',
        start_date=datetime(2025, 10, 1),
        end_date=datetime(2025, 10, 10)
    )
    pprint(trend1)
    pprint(trend2)


if __name__ == '__main__':
    main()