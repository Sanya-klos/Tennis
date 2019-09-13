from getDB import mySqlConnect
import creating_db
import readCsv


def write_to_db():
    name = 'ScoreDataBase'
    DB = mySqlConnect(None)
    cursor = DB.cursor()
    cursor.execute('CREATE DATABASE IF NOT  EXISTS `{}`'.format(name))
    cursor.close()
    DB = mySqlConnect()
    column = creating_db.make_table(DB)
    my_scores = readCsv.start('2018.csv')
    my_scores = my_scores[1:]
    cursor = DB.cursor()
    for data in my_scores:
        flag = 0
        last_element = len(data) - 1
        strs = str()
        for items in data:
            strs += '"'+items+'"'
            if flag != last_element:
                strs += ','
                flag += 1
        sql = 'insert into score2018({}) values({})'.format(column, strs)
        cursor.execute('insert into score2018({}) values({})'.format(column, strs))
