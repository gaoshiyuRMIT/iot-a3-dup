import logging
from .DBManager import DBManager
from .employee_manager import EmployeeManager

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class EngineerManager(DBManager):
    TABLE_NAME = "Engineer join Employee on Engineer.username = Employee.username"
    PK = "Engineer.username"

    def getOne(self, username):
        sql = f"select * from {self.TABLE_NAME} where {self.PK} = %s"
        values = [username]
        conn = self.conn
        try:
            with self.getCursor(conn) as cur:
                cur.execute(sql, values)
                return cur.fetchone()
        except Exception:
            logger.exception("getting one engineer by username failed")
            raise

    def get_one_by_mac_address(self, mac_addr):
        sql = f"select * from {self.TABLE_NAME} where mac_address = %s"
        vals = [mac_addr]
        conn = self.conn
        try:
            with self.getCursor(conn) as cur:
                cur.execute(sql, vals)
                return cur.fetchone()
        except Exception:
            logger.exception("getting one engineer by mac address failed")
            raise

    def getMany(self, query: dict):
        raise NotImplementedError

    def updateOne(self, username: str, new_val: dict) -> bool:
        raise NotImplementedError

    def deleteOne(self, username: str) -> bool:
        raise NotImplementedError

    def addOne(self, new_val: dict) -> bool:
        raise NotImplementedError