from flask import session
from passlib.hash import sha256_crypt


class AuthUtil(object):
    def login(self, password, stored_user) -> bool:
        if stored_user is None:
            return False
        success = sha256_crypt.verify(password, stored_user["password"])
        if success:
            session["username"] = stored_user["username"]
            session["fName"] = stored_user["fName"]
            session["role"] = stored_user["role"]
        return success

    @property
    def is_admin(self):
        '''
        example:

        >>> AuthUtil().is_admin
        True
        '''
        return self.is_logged_in and session["role"] == "admin"
            
    @property
    def is_engineer(self):
        '''
        example:

        >>> AuthUtil().is_engineer
        True
        '''
        return self.is_logged_in and session["role"] == "engineer"

    @property
    def is_manager(self):
        '''
        example:

        >>> AuthUtil().is_manager
        True
        '''
        return self.is_logged_in and session["role"] == "manager"

    def logout(self):
        session.pop("username", None)
        session.pop("fName", None)
        session.pop("role", None)

    @property
    def is_logged_in(self):
        '''
        example:

        >>> auth_util = AuthUtil()
        >>> auth_util.is_logged_in
        False
        '''
        return "username" in session
