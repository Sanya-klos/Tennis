import pymysql.cursors

# print("Enter user name: ")
# user = input()
# print("Enter your password: ")
# password = input()


def mySqlConnect(name='ScoreDataBase'):
    try:

        if name is None:
            # if you want to create schema:
            try:
                DB = pymysql.connect(user='root', password='1234',
                                     host='localhost')
                return DB
            except:
                print("Error! Invalid password or user entered")
        else:
            # if you have already created scheme:
            try:
                DB = pymysql.connect(user='root', password='1234',
                                     host='localhost', database=name)
                return DB
            except:
                print("Error! Invalid password or user entered")
    except pymysql.Error as e:
        print('Error: ' + str(e))
        return False
