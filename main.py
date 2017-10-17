from logging import exception

import MySQLdb
import Student
import Teacher
import Login
import SystemManager


if __name__ == '__main__':
    conn = MySQLdb.connect(user='root', passwd='password', db='test')
    log = Login.Login(conn)
    if log.main_func():
        account = log.get_login_account()
        if account[2] == 0:
            usr = SystemManager.SystemManager(conn, account[0], account[1])
            usr.main_func()
        elif account[2] == 1:
            usr = Teacher.Teacher(conn, account[0], account[1])
            usr.main_func()
        elif account[2] == 2:
            usr = Student.Student(conn, account[0], account[1])
            usr.main_func()
        else:
            conn.close()
            raise exception()
    conn.close()
