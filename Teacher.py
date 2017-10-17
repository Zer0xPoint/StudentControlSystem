import MySQLdb


class Teacher:
    def __init__(self, conns, account, passwd):
        cur = conns.cursor()
        sqlcmd = "select Name,TeacherNo,Gender,Birth,PositionNo,Salary from TeacherInfo where TeacherNo = '%s'" % account
        cur.execute(sqlcmd)
        temp = cur.fetchone()
        sqlcmd = "select PositionName from PositionList where PositionNo = '%s'" % temp[1]
        cur.execute(sqlcmd)
        pos = cur.fetchone()
        cur.close()

        self.PositionName = pos[0]
        self.width = 150
        self.conn = conns
        self.Name = temp[0]
        self.TeacherNo = temp[1]
        self.Gender = temp[2]
        self.Birth = temp[3]
        self.PositionNo = temp[4]
        self.Salary = temp[5]
        self.Password = passwd

    def main_func(self):
        info = ''
        while True:
            self.main_surface(info)
            choice = raw_input('What to do?')
            choice = choice.upper()
            if choice == 'P':
                info = self.operate_personal_info()
            elif choice == 'M':
                info = self.operate_message()
            elif choice == 'Q':
                break
            else:
                info = 'Error Action'

    def operate_personal_info(self):
        info = ''
        while True:
            self.personal_info_surface(info)
            choice = raw_input('What to do?')
            choice = choice.upper()
            if choice == 'C':
                info = self.change_personal_info()
            elif choice == 'Q':
                break
            else:
                info = 'Error Action'
        return info

    def change_personal_info(self):
        new_gender = self.Gender
        NewBirth = self.Birth
        NewPw = self.Password
        cur = self.conn.cursor()
        while True:
            choice = raw_input('Change Gender?(y/n)')
            choice = choice.lower()
            if choice == 'y':
                new_gender = raw_input('New Gender:')
                break
            elif choice == 'n':
                break
            else:
                pass
        while True:
            choice = raw_input('Change Born Data?(y/n)')
            choice = choice.lower()
            if choice == 'y':
                NewBirth = raw_input('New Born Date:')
                break
            elif choice == 'n':
                break
            else:
                pass
        while True:
            choice = raw_input('Change Password?(y/n)')
            choice = choice.lower()
            if choice == 'y':
                NewPw = raw_input('New Password:')
                break
            elif choice == 'n':
                break
            else:
                pass
        if NewBirth != self.Birth or new_gender != self.Gender:
            sqlcmd = "update TeacherInfo set Birth='%s',Gender='%s' where TeacherNo = '%s'" % (
                NewBirth, new_gender, self.TeacherNo)
            if 0 == cur.execute(sqlcmd):
                self.conn.rollback()
                cur.close()
                return 'Changer Fail'
        if NewPw != self.Password:
            sqlcmd = "update LoginAccount set Password='%s' where Account='%s'" % (NewPw, self.TeacherNo)
            if 0 == cur.execute(sqlcmd):
                self.conn.rollback()
                cur.close()
                return 'Change Fail!'
            else:
                self.conn.commit()
        self.Gender = new_gender
        self.Password = NewPw
        self.Birth = NewBirth
        cur.close()
        return 'Change Success!'

    def message_list(self):
        cur = self.conn.cursor()
        print ''
        sqlcmd = "select Id,SenderName,SendTime,Title from AllMessage where statu = 'pass' and MsgLevel <= 1"
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
        print '=' * self.width
        print ' ' * ((self.width - len(article[2])) / 2), article[2]
        head = article[0] + '     ' + str(article[1])
        print ' ' * ((self.width - len(head)) / 2), head
        print '-' * self.width
        print article[3]
        print '=' * self.width
        raw_input('Press any key to return!')
        return ''

    def create_message(self):
        print ''
        print '    Publish Messsage'
        title = raw_input('Message Title:')
        path = raw_input('Message Path:')
        fp = open(path, 'r')
        body = fp.read()
        fp.close()
        sqlcmd = "insert into AllMessage(MsgLevel,SenderNo,SenderName,SendTime,Title,Content,statu) values(1,'%s','%s',now(),'%s','%s','wait')" % (
            self.TeacherNo, self.Name, title, body)
        cur = self.conn.cursor()
        info = 'Publish Success!'
        if 0 == cur.execute(sqlcmd):
            info = 'Publish Fail'
            self.conn.rollback()
        else:
            self.conn.commit()
        cur.close()
        return info

    def operate_message(self):
        info = ''
        while True:
            self.message_surface(info)
            self.message_list()
            choice = raw_input('What to do?')
            choice = choice.upper()
            if choice == 'P':
                info = self.create_message()
            elif choice == 'Y':
                info = self.personal_message()
            elif choice == 'M':
                msg = input('Message Id:')
                info = self.message_info(msg)
            elif choice == 'Q':
                break
            else:
                info = 'Error Action'
        return info

    def personal_message_list(self):
        cur = self.conn.cursor()
        sqlcmd = "select Id,SenderName,SendTime,Title from AllMessage where SenderNo='%s'" % self.TeacherNo
        if cur.execute(sqlcmd) != 0:
            print '-' * self.width
            while True:
                temp = cur.fetchone()
                if not temp: break;
                print '%3d%-20s%-50s%s' % (temp[0], temp[1], temp[3], temp[2])
                print '-' * self.width
        cur.close()

    def personal_message(self):
        info = ''
        while True:
            self.personal_message_surface(info)
            self.personal_message_list()
            choice = raw_input('What to do?')
            choice = choice.upper()
            if choice == 'M':
                msg = input('Message Id:')
                info = self.message_info(msg)
            elif choice == 'D':
                info = self.delete_message()
            elif choice == 'Q':
                break
            else:
                info = 'Error Action!'
        return info

    def delete_message(self):
        print ''
        print '    Delete Message'
        MsgNo = input('Message id = ')
        cur = self.conn.cursor()
        sqlcmd = "delete from AllMessage where Id = %d and SenderNo = '%s'" % (MsgNo, self.TeacherNo)
        info = 'Delete Success!'
        if cur.execute(sqlcmd) == 0:
            info = 'Delete Fail'
            self.conn.rollback()
        else:
            self.conn.commit()
        cur.close()
        return info

    def main_surface(self, info):
        title = "Welcome, %s" % self.Name
        body1 = '[P]Personal Information'
        body2 = '[M]Message Management'
        body3 = '[Q]quit'
        print '=' * self.width
        print ' ' * ((self.width - len(title)) / 2), title
        print ' ' * ((self.width - len(body1)) / 2), body1
        print ' ' * ((self.width - len(body1)) / 2), body2
        print ' ' * ((self.width - len(body1)) / 2), body3
        print ' ' * ((self.width - len(info)) / 2), info
        print '=' * self.width

    def personal_info_surface(self, info):
        title = 'Personal Information'
        body1 = '[C]Change Information'
        body2 = '[Q]quit'
        body3 = '     Name: %s' % self.Name
        body4 = '   Gender: %s' % self.Gender
        body5 = 'Born Date: %s' % self.Birth
        body6 = ' Position: %s' % self.PositionName
        body7 = '   Salary: %.2f' % self.Salary
        print '=' * self.width
        print ' ' * ((self.width - len(title)) / 2), title
        print ' ' * ((self.width - len(body1)) / 2), body1
        print ' ' * ((self.width - len(body1)) / 2), body2
        print ' ' * ((self.width - len(info)) / 2), info
        print '-' * self.width
        print ' ' * ((self.width - len(body3)) / 2), body3
        print ' ' * ((self.width - len(body3)) / 2), body4
        print ' ' * ((self.width - len(body3)) / 2), body5
        print ' ' * ((self.width - len(body3)) / 2), body6
        print ' ' * ((self.width - len(body3)) / 2), body7
        print '=' * self.width

    def message_surface(self, info):
        title = 'MESSAGE'
        body1 = '[P]Publish Message'
        body2 = '[Y]Your Message'
        body3 = '[M]Message Detail'
        body4 = '[Q]quit'
        print '=' * self.width
        print ' ' * ((self.width - len(title)) / 2), title
        print ' ' * ((self.width - len(body1)) / 2), body1
        print ' ' * ((self.width - len(body1)) / 2), body2
        print ' ' * ((self.width - len(body1)) / 2), body3
        print ' ' * ((self.width - len(body1)) / 2), body4
        print ' ' * ((self.width - len(info)) / 2), info
        print '=' * self.width

    def personal_message_surface(self, info):
        title = 'PERSONAL MESSAGE'
        body1 = '[M]Message Detail'
        body2 = '[D]Delete Message'
        body3 = '[Q]quit'
        print '=' * self.width
        print ' ' * ((self.width - len(title)) / 2), title
        print ' ' * ((self.width - len(body1)) / 2), body1
        print ' ' * ((self.width - len(body1)) / 2), body2
        print ' ' * ((self.width - len(body1)) / 2), body3
        print ' ' * ((self.width - len(info)) / 2), info
        print '=' * self.width


if __name__ == '__main__':
    conn = MySQLdb.connect(user='root', passwd='password', db='test')
    t = Teacher(conn, '2', '123456')
    t.main_func()
    conn.close()
