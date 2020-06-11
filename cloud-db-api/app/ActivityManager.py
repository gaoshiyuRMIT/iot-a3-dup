import logging
from .DBManager import DBManager

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ActivityManager(DBManager):
    def get_type_counts(self):
        sql = "select activity, count(*) as count from UserActivity group by activity"
        conn = self.conn
        res = []
        try:
            with self.getCursor(conn) as cur:
                cur.execute(sql)
                res = cur.fetchall()
        except Exception:
            logger.exception("getting user activity type and counts failed")
            raise
        return res

    def getMany(self, query):
        raise NotImplementedError
    def getOne(self, id):
        raise NotImplementedError
    def updateOne(self, id, new_val):
        raise NotImplementedError
    def deleteOne(self, id):
        raise NotImplementedError
    def addOne(self, new_val):
        raise NotImplementedError