import readCsv


# class Create_schema:
#     def __init__(self, name='yahoo', DB=True):
#
#         self.name = name
#         self.DB = DB
#
#     def drop_db_ifexists(self):
#         try:
#             cursor = self.DB.cursor()
#             cursor.execute('DROP DATABASE IF EXISTS `yahoo`')
#             cursor.close()
#
#         except:
#             print('Uknown database yahoo')
#
#     def create_schema(self):
#         cursor = self.DB.cursor()
#         cursor.execute('CREATE SCHEMA `{}`'.format(self.name))
#         cursor.close()
#         print('Database is created!')
#
#     def yahoo_company(self):
#         cursor = self.DB.cursor()
#         cursor.execute("CREATE TABLE `yahoo`.`company` "
#                        "( `id` INT NOT NULL AUTO_INCREMENT,"
#                        " `name` VARCHAR(120) NULL,"
#                        "`symbol` VARCHAR(45) NULL,"
#                        "`sector_name` VARCHAR(45) NULL,"
#                        "`price` float NULL,"
#                        "`volume` VARCHAR(45) NULL,"
#                        "`beta` float NULL,"
#                        "`eps` float NULL,"
#                        "`link` VARCHAR(150) NULL,"
#                        "PRIMARY KEY (`id`)) "
#                        "ENGINE = MyISAM;"
#                        )
#         cursor.close()
#         print('"company" table is created')
#
#     def yahoo_datasummary(self):
#         cursor = self.DB.cursor()
#         cursor.execute("CREATE TABLE `yahoo`.`datasummary` ("
#                        "`id` INT NOT NULL AUTO_INCREMENT,"
#                        "`tag` VARCHAR(45) NULL,"
#                        "`value` VARCHAR(45) NULL,"
#                        "`date` VARCHAR(45) NULL,"
#                        "`period` VARCHAR(45) NULL,"
#                        "`company` VARCHAR(45) NULL,"
#                        "PRIMARY KEY (`id`))"
#                        "ENGINE = MyISAM;")
#         cursor.close()
#         print('"datasummary" table is created')
#
#     def yahoo_historical(self):
#         print('"historical" table is created')
#         cursor = self.DB.cursor()
#         cursor.execute("CREATE TABLE `yahoo`.`historical` "
#                        "(`id` INT NOT NULL AUTO_INCREMENT,"
#                        "`company` VARCHAR(120) NULL,"
#                        "`open` VARCHAR(45) NULL,"
#                        "`high` VARCHAR(45) NULL,"
#                        "`low` VARCHAR(45) NULL,"
#                        "`close` VARCHAR(45) NULL,"
#                        "`date` DATE NULL,"
#                        "PRIMARY KEY (`id`))"
#                        "ENGINE = MyISAM;")
#         cursor.close()
#
#     def yahoo_snp(self):
#         print('"snp" table is created')
#         cursor = self.DB.cursor()
#         cursor.execute("CREATE TABLE `yahoo`.`snp` "
#                        "(`id` INT NOT NULL AUTO_INCREMENT,"
#                        "`date` DATE NULL,"
#                        "`close` VARCHAR(45) NULL,"
#                        "PRIMARY KEY (`id`))"
#                        "ENGINE = MyISAM;")
#
#     def stronf_and_weak(self):
#         cursor = self.DB.cursor()
#         cursor.execute("CREATE TABLE `yahoo`.`strong_and_weak`"
#                        " (`id` INT NOT NULL,"
#                        "`company` VARCHAR(99) NULL,"
#                        "`status` VARCHAR(45) NULL,"
#                        "PRIMARY KEY (`id`)) "
#                        "ENGINE = MyISAM;")
#         print('strong_and_weak table is created')


def make_table(DB):
    data = readCsv.start('2018.csv')
    rows = data[0]
    strs = str()
    flag = 0
    last_element = len(rows) - 1
    cursor = DB.cursor()
    cursor.execute('drop table if exists score2018')
    cursor.execute('CREATE TABLE `score2018` '
                   '(`id` INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (`id`)) '
                   'ENGINE = MyISAM;')
    for data in rows:
        cursor.execute("ALTER TABLE `score2018` "
                       "ADD COLUMN `{}` VARCHAR(80);".format(data))
        strs += '`'+data+'`'
        if flag != last_element:
            strs += ','
            flag += 1
    cursor.close()
    print('"score2018" table is created')
    return strs
