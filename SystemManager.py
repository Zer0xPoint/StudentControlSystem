import MySQLdb
import os


class SystemManager:
    def __init__(self, conns, account, pw):
        self.conn = conns
        self.width = 150
        self.account = account
        # cur = self.conn.cursor()
        self.password = pw

    def main_func(self):
        info = ''
        while True:
            self.main_surface(info)
            choice = raw_input('What to do?')
            choice = choice.upper()
            if choice == 'T':
                self.operat_teacher()
            elif choice == 'M':
                self.operat_message()
            elif choice == 'S':
                self.operat_student()
            elif choice == 'Q':
                break
            else:
                info = 'Error Action!'

    def operat_teacher(self):
        info = ''
        while True:
            self.teacher_info_surface(info)
            self.scan_teacher_info()
            print '-' * self.width
            choice = raw_input('What to do?')
            choice = choice.upper()
            if choice == 'R':
                info = self.reg_teacher()
            elif choice == 'C':
                info = self.change_teacher_info()
            elif choice == 'I':
                info = self.init_teacher_password()
            elif choice == 'D':
                info = self.delete_teacher()
            elif choice == 'Q':
                break
            else:
                info = 'Error Acction!'

    def scan_teacher_info(self):
        cur = self.conn.cursor()
        sqlcmd = "select T.Id,T.Name,T.TeacherNo,T.Gender,T.Birth,P.PositionName,T.Salary from TeacherInfo T,PositionList P where T.PositionNo = P.PositionNo"
        cur.execute(sqlcmd)
        print '%3s|%20s|%12s|%8s|%15s|%15s|%15s' % (
            'Id', 'Name', 'TeacherNo', 'Gender', 'BornDate', 'Position', 'Salary')
        while True:
            res = cur.fetchone()
            if not res: break
            print '%3d|%20s|%12s|%8s|%15s|%15s|%15.2f' % (res[0], res[1], res[2], res[3], res[4], res[5], res[6])
        print '-' * self.width
        cur.close()

    def reg_teacher(self):
        cur = self.conn.cursor()
        print ''
        title = '    Register New Teacher'
        print title
        name = raw_input('           Name:')
        number = raw_input(' Teacher Number:')
        gender = raw_input('         Gender:')
        birth = raw_input('      Born Date:')
        self.print_position_info()
        position = input('Position Number:')
        salary = input('         Salary:')
        sqlcmd = "insert into TeacherInfo(Name,TeacherNo,Gender,Birth,PositionNo,Salary) values('%s','%s','%s','%s',%d,%f)" % (
            name, number, gender, birth, position, salary)
        res = cur.execute(sqlcmd)
        info = 'Register Success!'
        if res == 0:
            info = 'Register Fail!'
            self.conn.rollback()
        else:
            sqlcmd = 'select Password from DefaultPassword where AccountLevel = 1'
            if cur.execute(sqlcmd) == 0:
                info = 'Register Fail!'
                self.conn.rollback()
            else:
                pw = cur.fetchone()
                sqlcmd = "insert into LoginAccount(Account,Password,AccountLevel) values('%s','%s',1)" % (number, pw[0])
                if cur.execute(sqlcmd) == 0:
                    info = 'Register Fail!'
                    self.conn.rollback()
                else:
                    self.conn.commit()
        cur.close()
        return info

    def change_teacher_info(self):
        cur = self.conn.cursor()
        print ''
        title = '     Change Teacher Information'
        print title
        teacherNo = raw_input('TeacherNo:')
        sqlcmd = "select Name,TeacherNo,Gender,Birth,PositionNo,Salary from TeacherInfo where TeacherNo = '%s'" % teacherNo
        res = cur.execute(sqlcmd)
        info = 'Change Success!'
        if res == 0:
            info = 'Cannot find this teacher'
        else:
            temp = cur.fetchone()
            print 'old information: %s %s %s %s %d %.2f' % (temp[0], temp[1], temp[2], temp[3], temp[4], temp[5])
            name = raw_input('           Name:')
            number = raw_input(' Teacher Number:')
            gender = raw_input('         Gender:')
            birth = raw_input('      Born Date:')
            self.print_position_info()
            position = input('Position Number:')
            salary = input('         Salary:')
            sqlcmd = "update TeacherInfo Set Name='%s',TeacherNo='%s',Gender='%s',Birth='%s',PositionNo=%d,Salary=%.2f where TeacherNo = '%s'" % (
                name, number, gender, birth, position, salary, teacherNo)
            res = cur.execute(sqlcmd)
            if res == 0:
                info = 'Change Fail!'
                self.conn.rollback()
            else:
                if number != temp[1]:
                    sqlcmd = "update LoginAccount set Account='%s' where Account='%s'" % (number, temp[1])
                    if cur.execute(sqlcmd) == 0:
                        info = 'Change Fail!'
                        self.conn.rollback()
                    else:
                        self.conn.commit()
                else:
                    self.conn.commit()
        cur.close()
        return info

    def init_teacher_password(self):
        cur = self.conn.cursor()
        sqlcmd = 'select Password from DefaultPassword where AccountLevel = 1'
        info = 'Initial Success!'
        if cur.execute(sqlcmd) == 0:
            info = 'Initial Fail'
            self.conn.rollback()
        else:
            newPw = cur.fetchone()
            if not newPw:
                info = 'Initial Fail'
                self.conn.rollback()
            else:
                teacherNo = raw_input('Teacher Number:')
                sqlcmd = "select Password from LoginAccount where Account = '%s'" % teacherNo
                if 0 == cur.execute(sqlcmd):
                    info = 'Initial Fail'
                    self.conn.rollback()
                else:
                    oldPw = cur.fetchone()
                    if oldPw[0] != newPw[0]:
                        sqlcmd = "update LoginAccount set Password='%s' where Account = '%s'" % (newPw[0], teacherNo)
                        if cur.execute(sqlcmd) == 0:
                            info = 'Initial Fail'
                            self.conn.rollback()
                        else:
                            self.conn.commit()
        cur.close()
        return info

    def delete_teacher(self):
        cur = self.conn.cursor()
        print '    Delete Teacher'
        teacher_no = raw_input('Teacher Number:')
        sqlcmd = "delete from TeacherInfo where TeacherNo = '%s'" % teacher_no
        res = cur.execute(sqlcmd)
        info = 'Delete Success!'
        if res == 0:
            info = 'Delete Fail!'
            self.conn.rollback()
        else:
            sqlcmd = "delete from LoginAccount where Account = '%s'" % teacher_no
            res = cur.execute(sqlcmd)
            if res == 0:
                info = 'Delete Fail!'
                self.conn.rollback()
            else:
                self.conn.commit()
        cur.close()
        return info

    def print_position_info(self):
        cur = self.conn.cursor()
        cur.execute('select PositionNo,PositionName from PositionList')
        pos = []
        while True:
            tp = cur.fetchone()
            if not tp: break;
            pos.append(tp)
        print ' ' * 10, '-' * 30
        print ' ' * 10, 'POSTIONS'
        print ' ' * 10, '-' * 30
        it = pos.__iter__()
        while True:
            try:
                temp = it.next()
                print ' ' * 10, temp[0], ' : ', temp[1]
            except:
                break
        print ' ' * 10, '-' * 30
        cur.close()

    def operat_student(self):
        info = ''
        while True:
            self.student_info_surface(info)
            self.scan_student_info()
            print '-' * self.width
            choice = raw_input('What to do?')
            choice = choice.upper()
            if choice == 'R':
                info = self.reg_student()
            elif choice == 'C':
                info = self.change_student_info()
            elif choice == 'I':
                info = self.init_student_password()
            elif choice == 'D':
                info = self.delete_student()
            elif choice == 'Q':
                break
            else:
                info = 'Error Acction!'

    def scan_student_info(self):
        cur = self.conn.cursor()
        sqlcmd = "select S.Id,S.Name,S.StudentNo,S.Gender,S.Birth,S.Grade,S.Academy,S.Major,T.Name from StudentInfo S,TeacherInfo T where S.TeacherNo = T.TeacherNo"
        cur.execute(sqlcmd)
        print '%3s|%20s|%15s|%8s|%15s|%5s|%20s|%20s|%20s' % (
            'Id', 'Name', 'Student Number', 'Gender', 'Born Date', 'Grade', 'Academy', 'Major', 'Teacher')
        while True:
            res = cur.fetchone()
            if not res: break
            print '%3d|%20s|%15s|%8s|%15s|%5s|%20s|%20s|%20s' % (
                res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7], res[8])
        print '-' * self.width
        cur.close()

    def reg_student(self):
        cur = self.conn.cursor()
        print ''
        title = '    Register New Student'
        print title
        name = raw_input('          Name:')
        number = raw_input('Student number:')
        gender = raw_input('        Gender:')
        birth = raw_input('     Born Date:')
        grade = raw_input('         Grade:')
        academy = raw_input('       Academy:')
        major = raw_input('         Major:')
        teacher = raw_input('Teacher Number:')
        sqlcmd = "insert into StudentInfo(Name,StudentNo,Gender,Birth,Grade,Academy,Major,TeacherNo) values('%s','%s','%s','%s','%s','%s','%s','%s')" % (
            name, number, gender, birth, grade, academy, major, teacher)
        res = cur.execute(sqlcmd)
        info = 'Register Success!'
        if res == 0:
            info = 'Register Fail!'
            self.conn.rollback()
        else:
            sqlcmd = 'select Password from DefaultPassword where AccountLevel = 2'
            if cur.execute(sqlcmd) == 0:
                info = 'Register Fail!'
                self.conn.rollback()
            else:
                pw = cur.fetchone()
                sqlcmd = "insert into LoginAccount(Account,Password,AccountLevel) values('%s','%s',2)" % (number, pw[0])
                if cur.execute(sqlcmd) == 0:
                    info = 'Register Fail!'
                    self.conn.rollback()
                else:
                    self.conn.commit()
        cur.close()
        return info

    def change_student_info(self, ):
        cur = self.conn.cursor()
        print ''
        title = '     Change Student Information'
        print title
        studentNo = raw_input('Student Number:')
        sqlcmd = "select Name,StudentNo,Gender,Birth,Grade,Academy,Major,TeacherNo from StudentInfo where StudentNo = '%s'" % studentNo
        res = cur.execute(sqlcmd)
        info = 'Change Success!'
        if res == 0:
            info = 'Cannot find this student'
        else:
            temp = cur.fetchone()
            print 'old information: |%s| |%s| |%s| |%s| |%s| |%s| |%s| |%s|' % (
                temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7])
            name = raw_input('          Name:')
            number = raw_input('Student Number:')
            gender = raw_input('        Gender:')
            birth = raw_input('     Born Date:')
            grade = raw_input('         Grade:')
            academy = raw_input('       Academy:')
            major = raw_input('         Major:')
            teacher = raw_input('Teacher Number:')
            sqlcmd = "update StudentInfo Set Name='%s',StudentNo='%s',Gender='%s',Birth='%s',Grade='%s',Academy='%s',Major='%s',TeacherNo='%s' where StudentNo = '%s'" % (
                name, number, gender, birth, grade, academy, major, teacher, studentNo)
            if cur.execute(sqlcmd) == 0:
                info = 'Change Fail!'
                self.conn.rollback()
            else:
                if number != temp[1]:
                    sqlcmd = "update LoginAccount set Account='%s' where Account='%s'" % (number, temp[1])
                    if cur.execute(sqlcmd) == 0:
                        info = 'Change Fail!'
                        self.conn.rollback()
                    else:
                        self.conn.commit()
                else:
                    self.conn.commit()
        cur.close()
        return info

    def init_student_password(self):
        cur = self.conn.cursor()
        sqlcmd = 'select Password from DefaultPassword where AccountLevel = 2'
        info = 'Initial Success!'
        if cur.execute(sqlcmd) == 0:
            info = 'Initial Fail'
            self.conn.rollback()
        else:
            newPw = cur.fetchone()
            if not newPw:
                info = 'Initial Fail'
                self.conn.rollback()
            else:
                studentNo = raw_input('Student Number:')
                sqlcmd = "select Password from LoginAccount where Account = '%s'" % studentNo
                cur.execute(sqlcmd)
                oldPw = cur.fetchone()
                if oldPw[0] != newPw[0]:
                    sqlcmd = "update LoginAccount set Password='%s' where Account = '%s'" % (newPw[0], studentNo)
                    if cur.execute(sqlcmd) == 0:
                        info = 'Initial Fail'
                        self.conn.rollback()
                    else:
                        self.conn.commit()
        cur.close()
        return info

    def delete_student(self, ):
        cur = self.conn.cursor()
        print '    Delete Student'
        studentNo = raw_input('Student Number:')
        sqlcmd = "delete from StudentInfo where StudentNo = '%s'" % studentNo
        res = cur.execute(sqlcmd)
        info = 'Delete Success!'
        if res == 0:
            info = 'Delete Fail!'
            self.conn.rollback()
        else:
            sqlcmd = "delete from LoginAccount where Account = '%s'" % studentNo
            res = cur.execute(sqlcmd)
            if res == 0:
                info = 'Delete Fail!'
                self.conn.rollback()
            else:
                self.conn.commit()
        cur.close()
        return info

    def operat_message(self):
        info = ''
        while True:
            self.message_surface(info)
            self.message_list()
            choice = raw_input('What to do?')
            choice = choice.upper()
            if choice == 'D':
                info = self.delete_message()
            elif choice == 'P':
                info = self.create_message()
            elif choice == 'C':
                info = self.check_message()
            elif choice == 'M':
                msg = input('Message Id:')
                info = self.message_info(msg)
            elif choice == 'Q':
                break
            else:
                info = 'Error Action!'

    def message_info(self, msg_no):
        cur = self.conn.cursor()
        sqlcmd = "select SenderName,SendTime,Title,Content from AllMessage where Id = %d" % msg_no
        if cur.execute(sqlcmd) == 0:
            cur.close()
            return 'Read Fail!'
        article = cur.fetchone()
        cur.close()
        os.system('')
        print '=' * self.width
        print ' ' * ((self.width - len(article[2])) / 2), article[2]
        head = article[0] + '     ' + str(article[1])
        print ' ' * ((self.width - len(head)) / 2), head
        print '-' * self.width
        print article[3]
        print '=' * self.width
        raw_input('Press any key to return!')
        return ''

    def message_list(self):
        cur = self.conn.cursor()
        print ''
        sqlcmd = "select Id,SenderName,SendTime,Title from AllMessage where statu = 'pass'"
        if cur.execute(sqlcmd) == 0:
            return
        print '-' * self.width
        while True:
            temp = cur.fetchone()
            if not temp:
                break
            print '%3s    %-20s%-50s%s' % (temp[0], temp[1], temp[3], temp[2])
            print '-' * self.width
        cur.close()

    def create_message(self):
        print ''
        print '    Publish Messsage'
        title = raw_input('Message Title:')
        path = raw_input('Message Path:')
        fp = open(path, 'r')
        body = fp.read()
        fp.close()
        sqlcmd = "insert into AllMessage(MsgLevel,SenderNo,SenderName,SendTime,Title,Content,statu) values(0,'%s','Admin',now(),'%s','%s','pass')" % (
            self.account, title, body)
        cur = self.conn.cursor()
        info = 'Publish Success!'
        if 0 == cur.execute(sqlcmd):
            info = 'Publish Fail'
            self.conn.rollback()
        else:
            self.conn.commit()
        cur.close()
        return info

    def delete_message(self):
        print ''
        print '    Delete Message'
        MsgNo = input('Message id = ')
        cur = self.conn.cursor()
        sqlcmd = "delete from AllMessage where Id = %d" % MsgNo
        info = 'Delete Success!'
        if cur.execute(sqlcmd) == 0:
            info = 'Delete Fail'
            self.conn.rollback()
        else:
            self.conn.commit()
        cur.close()
        return info

    def check_message(self):
        cur = self.conn.cursor()
        MsgCount = cur.execute(
            "select Id,SenderNo,SenderName,SendTime,Title,Content from AllMessage where statu = 'wait'")
        info = 'All Messages Were Checked!'
        msg_info = 'You have %d messages need to check!' % MsgCount
        while MsgCount > 0:
            self.wait_message_surface(msg_info)
            msg = cur.fetchone()
            print ' ' * ((self.width - len(msg[4])) / 2), msg[4]
            print 'Sender Name:', msg[2], '     Sender Number:', msg[1], '   Time:', msg[3]
            print msg[5]
            print '-' * self.width
            choice = raw_input('What to do?')
            choice = choice.upper()
            MsgCount -= 1
            msg_info = 'You have %d messages need to check!' % MsgCount
            if choice == 'I':
                continue
            elif choice == 'P':
                sqlcmd = "update AllMessage set statu = 'pass' where Id = %d" % msg[0]
                if cur.execute(sqlcmd) == 0:
                    msg_info = 'Check Fail!'
                    self.conn.rollback()
                else:
                    self.conn.commit()
            elif choice == 'F':
                sqlcmd = "update AllMessage set statu = 'fail' where Id = %d" % msg[0]
                if cur.execute(sqlcmd) == 0:
                    msg_info = 'Check Fail!'
                    self.conn.rollback()
                else:
                    self.conn.commit()
            elif choice == 'Q':
                break
            else:
                info = 'Error Action!'
        cur.close()
        if MsgCount != 0:
            info = 'Still have %d Messages wait for dealing!' % MsgCount
        return info

    def main_surface(self, info):
        os.system('')
        title = 'Welcome, Administor!'
        body1 = '[T]Teachers Information'
        body2 = '[S]Students Information'
        body3 = '[M]Message  Information'
        body4 = '[Q]quit'
        print '=' * self.width
        print ' ' * ((self.width - len(title)) / 2), title
        print ' ' * ((self.width - len(body1)) / 2), body1
        print ' ' * ((self.width - len(body1)) / 2), body2
        print ' ' * ((self.width - len(body1)) / 2), body3
        print ' ' * ((self.width - len(body1)) / 2), body4
        print ' ' * ((self.width - len(info)) / 2), info
        print '=' * self.width

    def student_info_surface(self, info):
        os.system('')
        title = 'STUDENT LIST'
        body1 = '[R]Register New Student'
        body2 = '[C]Change Student Information'
        body3 = '[I]Initial Student Password'
        body4 = '[D]Delete Student Information'
        body5 = '[Q]quit'
        print '=' * self.width
        print ' ' * ((self.width - len(title)) / 2), title
        print ' ' * ((self.width - len(body1)) / 2), body1
        print ' ' * ((self.width - len(body1)) / 2), body2
        print ' ' * ((self.width - len(body1)) / 2), body3
        print ' ' * ((self.width - len(body1)) / 2), body4
        print ' ' * ((self.width - len(body1)) / 2), body5
        print ' ' * ((self.width - len(info)) / 2), info
        print '=' * self.width

    def teacher_info_surface(self, info):
        os.system('')
        title = 'TEACHER LIST'
        body1 = '[R]Register New Teacher'
        body2 = '[C]Change Teacher Information'
        body3 = '[I]Initial Teacher Password'
        body4 = '[D]Delete Teacher Information'
        body5 = '[Q]quit'
        print '=' * self.width
        print ' ' * ((self.width - len(title)) / 2), title
        print ' ' * ((self.width - len(body1)) / 2), body1
        print ' ' * ((self.width - len(body1)) / 2), body2
        print ' ' * ((self.width - len(body1)) / 2), body3
        print ' ' * ((self.width - len(body1)) / 2), body4
        print ' ' * ((self.width - len(body1)) / 2), body5
        print ' ' * ((self.width - len(info)) / 2), info
        print '=' * self.width

    def message_surface(self, info):
        os.system('')
        title = 'MESSAGE LIST'
        body1 = '[P]Publish Message'
        body2 = '[C]Check   Message'
        body3 = '[D]Delete  Message'
        body4 = '[M]Message Detail'
        body5 = '[Q]quit'
        print '=' * self.width
        print ' ' * ((self.width - len(title)) / 2), title
        print ' ' * ((self.width - len(body1)) / 2), body1
        print ' ' * ((self.width - len(body1)) / 2), body2
        print ' ' * ((self.width - len(body1)) / 2), body3
        print ' ' * ((self.width - len(body1)) / 2), body4
        print ' ' * ((self.width - len(body1)) / 2), body5
        print ' ' * ((self.width - len(info)) / 2), info
        print '=' * self.width

    def wait_message_surface(self, info):
        os.system('')
        title = 'CHECK MESSAGE'
        body1 = '[I]Ignore'
        body2 = '[P]Pass'
        body3 = '[F]Fail'
        body4 = '[Q]quit'
        print '=' * self.width
        print ' ' * ((self.width - len(title)) / 2), title
        print ' ' * ((self.width - len(body1)) / 2), body1
        print ' ' * ((self.width - len(body1)) / 2), body2
        print ' ' * ((self.width - len(body1)) / 2), body3
        print ' ' * ((self.width - len(body1)) / 2), body4
        print ' ' * ((self.width - len(info)) / 2), info
        print '=' * self.width


if __name__ == '__main__':
    conn = MySQLdb.connect(user='root', passwd='password', db='test')
    sm = SystemManager(conn, '1', '123456')
    sm.main_func()
    conn.close()
