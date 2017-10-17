import MySQLdb
import os


class Student:
    def __init__(self, conn, account, passwd):
        cur = conn.cursor()
        sqlcmd = "select Name,Gender,Birth,Academy,Major,Grade,TeacherNo from StudentInfo where StudentNo = '%s'" % account
        cur.execute(sqlcmd)
        res = cur.fetchone()
        sqlcmd = "select Name from TeacherInfo where TeacherNo = '%s'" % res[6]
        cur.execute(sqlcmd)
        TeacherName = cur.fetchone()
        cur.close()

        self.width = 150
        self.conn = conn
        self.account = account
        self.Password = passwd
        self.Name = res[0]
        self.Gender = res[1]
        self.Birth = res[2]
        self.Accademy = res[3]
        self.Major = res[4]
        self.Grade = res[5]
        self.Teacher = TeacherName[0]

    def main_func(self):
        info = ''
        while True:
            self.main_surface(info)
            choice = raw_input('What to do?')
            choice = choice.upper()
            if choice != 'P' and choice != 'M' and choice != 'Q':
                info = 'Error Action!'
                continue
            if choice == 'P':
                info = self.personal_info()
            elif choice == 'M':
                info = self.operat_message()
            else:
                break

    def personal_info(self):
        info = ''
        while True:
            self.personal_info_surface(info)
            choice = raw_input('What to do?')
            choice = choice.upper()
            if choice != 'C' and choice != 'Q':
                info = 'Error Action!'
                continue
            if choice == 'C':
                info = self.change_personal_info()
            else:
                break
        return info

    def change_personal_info(self):
        NewGender = self.Gender
        NewBirth = self.Birth
        NewPw = self.Password
        while True:
            choice = raw_input('Change Gender?(y/n)')
            choice = choice.lower()
            if choice == 'y':
                NewGender = raw_input('New Gender:')
                break
            elif choice == 'n':
                break
            else:
                pass
        while True:
            choice = raw_input('change Born Date?(y/n)')
            choice = choice.lower()
            if choice == 'y':
                NewBirth = raw_input('New Born Date:')
                break
            elif choice == 'n':
                break
            else:
                pass
        while True:
            choice = raw_input('change Password?(y/n)')
            choice = choice.lower()
            if choice == 'y':
                NewPw = raw_input('New Password:')
                break
            elif choice == 'n':
                break
            else:
                pass
        info = 'Change Success!'
        cur = self.conn.cursor()
        if NewGender != self.Gender or NewBirth != self.Birth:
            sqlcmd = "update StudentInfo set Gender = '%s',Birth = '%s' where StudentNo = '%s'" % (
                NewGender, NewBirth, self.account)
            if cur.execute(sqlcmd) == 0:
                self.conn.rollback()
                cur.close()
                return 'Change Fail!'
        if NewPw != self.Password:
            sqlcmd = "update LoginAccount set Password = '%s' where Account='%s'" % (NewPw, self.account)
            if cur.execute(sqlcmd) == 0:
                self.conn.rollback()
                cur.close()
                return 'Change Fail!'
            else:
                self.conn.commit()
        self.Gender = NewGender
        self.Birth = NewBirth
        self.Password = NewPw
        cur.close()
        return 'Change Success!'

    def operat_message(self):
        info = ''
        while True:
            self.message_surface(info)
            self.message_list()
            choice = raw_input('What to do?')
            choice = choice.upper()
            if choice == 'M':
                msg = input('Message Id:')
                info = self.message_info(msg)
            elif choice == 'Q':
                break
            else:
                info = 'Error Action!'
        return info

    def message_list(self):
        cur = self.conn.cursor()
        print ''
        sqlcmd = "select Id,SenderName,SendTime,Title from AllMessage where statu = 'pass' and MsgLevel = 1"
        if cur.execute(sqlcmd) == 0:  return
        print '-' * self.width
        while True:
            temp = cur.fetchone()
            if not temp: break;
            print '%3d%-20s%-50s%s' % (temp[0], temp[1], temp[3], temp[2])
            print '-' * self.width
        cur.close()

    def message_info(self, msg_no):
        cur = self.conn.cursor()
        sqlcmd = "select SenderName,SendTime,Title,Content from AllMessage where Id = %d" % msg_no
        if cur.execute(sqlcmd) == 0:
            cur.close()
            return 'Read Fail!'
        article = cur.fetchone()
        cur.close()
        os.system('cls')
        print '=' * self.width
        print ' ' * ((self.width - len(article[2])) / 2), article[2]
        head = article[0] + '     ' + str(article[1])
        print ' ' * ((self.width - len(head)) / 2), head
        print '-' * self.width
        print article[3]
        print '=' * self.width
        raw_input('Press any key to return!')
        return ''

    def quit(self):
        pass

    def main_surface(self, info):
        os.system('cls')
        print '=' * self.width
        title = 'Welcome %s!' % self.Name
        body1 = '[P]Personal Information'
        body2 = '[M]Message'
        body3 = '[Q]quit'
        print ' ' * ((self.width - len(title)) / 2), title
        print ' ' * ((self.width - len(body1)) / 2), body1
        print ' ' * ((self.width - len(body1)) / 2), body2
        print ' ' * ((self.width - len(body1)) / 2), body3
        print ' ' * ((self.width - len(info)) / 2), info
        print '=' * self.width

    def message_surface(self, info):
        os.system('cls')
        print '=' * self.width
        title = 'MESSAGES'
        body1 = '[M]Message Detail'
        body2 = '[Q]quit'
        print ' ' * ((self.width - len(title)) / 2), title
        print ' ' * ((self.width - len(body1)) / 2), body1
        print ' ' * ((self.width - len(body1)) / 2), body2
        print ' ' * ((self.width - len(info)) / 2), info
        print '=' * self.width

    def personal_info_surface(self, info):
        os.system('cls')
        print '=' * self.width
        title = 'PERSONAL INFORMATION'
        body1 = '[C]Change Information'
        body2 = '[Q]quit'
        print ' ' * ((self.width - len(title)) / 2), title
        print ' ' * ((self.width - len(body1)) / 2), body1
        print ' ' * ((self.width - len(body1)) / 2), body2
        print ' ' * ((self.width - len(info)) / 2), info
        print '-' * self.width
        body3 = '          Name: %s' % self.Name
        body4 = 'Student Number: %s' % self.account
        body5 = '        Gender: %s' % self.Gender
        body6 = '         Birth: %s' % self.Birth
        body7 = '      Accademy: %s' % self.Accademy
        body8 = '         Major: %s' % self.Major
        body9 = '         Grade: %s' % self.Grade
        body10 = '       Teacher: %s' % self.Teacher
        print ' ' * ((self.width - len(body6)) / 2), body3
        print ' ' * ((self.width - len(body6)) / 2), body4
        print ' ' * ((self.width - len(body6)) / 2), body5
        print ' ' * ((self.width - len(body6)) / 2), body6
        print ' ' * ((self.width - len(body6)) / 2), body7
        print ' ' * ((self.width - len(body6)) / 2), body8
        print ' ' * ((self.width - len(body6)) / 2), body9
        print ' ' * ((self.width - len(body6)) / 2), body10
        print '=' * self.width


if __name__ == '__main__':
    conn = MySQLdb.connect(user='root', passwd='password', db='test')
    stu = Student(conn, '3', '123456')
    stu.main_func()
    conn.close()
