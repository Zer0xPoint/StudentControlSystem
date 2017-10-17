import os
import MySQLdb
import time


def login_surface(info):
    os.system('')
    width = 50
    title = 'LOGIN'
    body1 = '[A]Admin'
    body2 = '[T]Teacher'
    body3 = '[S]Student'
    body4 = '[Q]quit'
    print '=' * width
    print ' ' * ((width - len(title)) / 2), title
    print ' ' * ((width - len(body1)) / 2), body1
    print ' ' * ((width - len(body1)) / 2), body2
    print ' ' * ((width - len(body1)) / 2), body3
    print ' ' * ((width - len(body1)) / 2), body4
    print ' ' * ((width - len(info)) / 2), info
    print '-' * width


class Login:
    def __init__(self, conn):
        self.account = ''
        self.password = ''
        self.level = 2
        self.conn = conn

    def main_func(self):
        err = ''
        while True:
            login_surface(err)
            level = raw_input('Access:')
            level = level.upper()
            if level == 'A':
                self.level = 0
            elif level == 'T':
                self.level = 1
            elif level == 'S':
                self.level = 2
            elif level == 'Q':
                return False
            else:
                err = 'Error Action!'
                continue
            self.account = raw_input('Account:')
            self.password = raw_input('Password:')
            if self.check_account():
                err = 'Login Success!'
                # login_surface(err)
                print 'Please wait...'
                time.sleep(3)
                return True
            else:
                err = 'Login Failed!'

    def get_login_account(self):
        return [self.account, self.password, self.level]

    def check_account(self):
        cur = self.conn.cursor()
        sqlcmd = "select Account,Password,AccountLevel from LoginAccount where Account = '%s'" % self.account
        if cur.execute(sqlcmd) == 0:
            return True
        temp = cur.fetchone()
        cur.close()
        if temp[1] == self.password and temp[2] == self.level:
            return True
        else:
            return False

    def quit(self):
        pass


if __name__ == '__main__':
    conn = MySQLdb.connect(user='root', passwd='password', db='test')
    a = Login(conn)
    a.main_func()
    a.quit()
    conn.close()
