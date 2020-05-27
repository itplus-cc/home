import time, datetime


class dateTools(object):
    out_datetime = None
    out_timestamp = None

    def __init__(self, in_date=None, formatStr=None):
        self.init(in_date, formatStr)

    def init(self, in_date, formatStr):
        if not in_date:
            self.out_datetime = datetime.datetime.now()
            self.out_timestamp = time.time()
            return
        if isinstance(in_date, datetime.datetime):
            self.out_datetime = in_date
            self.out_timestamp = time.mktime(self.out_datetime.timetuple())
            return
        if formatStr:
            try:
                self.out_datetime = datetime.datetime.strptime(in_date, formatStr)
            except Exception as e:
                raise Exception(f'时间格式错误  {e}')
            self.out_timestamp = time.mktime(self.out_datetime.timetuple())
            return
        try:
            in_date = float(in_date)
            self.out_datetime = datetime.datetime.fromtimestamp(in_date)
            self.out_timestamp = time.mktime(self.out_datetime.timetuple())
            return
        except Exception as e:
            raise Exception(f'时间格式错误  {e}')
    def now(self):
        self.out_datetime = datetime.datetime.now()
        self.out_timestamp = time.time()
        return self

    def offsetR(self, days=0, seconds=0, minutes=0, hours=0, weeks=0):
        self.out_datetime = self.out_datetime + datetime.timedelta(days=days, seconds=seconds, minutes=minutes,
                                                                   hours=hours, weeks=weeks)
        self.out_timestamp = time.mktime(self.out_datetime.timetuple())
        return self

    def offsetL(self, days=0, seconds=0, minutes=0, hours=0, weeks=0):
        self.out_datetime = self.out_datetime - datetime.timedelta(days=days, seconds=seconds, minutes=minutes,
                                                                   hours=hours, weeks=weeks)
        self.out_timestamp = time.mktime(self.out_datetime.timetuple())
        return self

    def format(self, formatStr="%Y-%m-%d %H:%M:%S"):
        return self.out_datetime.strftime(formatStr)

