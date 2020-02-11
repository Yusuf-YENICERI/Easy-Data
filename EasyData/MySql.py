#import mysql.connector

#MySql Part Start
class MySql(object):

    def __init__(self, **kwargs):
        self.db = mysql.connector.connect(**kwargs)
        self.cursor = self.db.cursor()
        self.commit = self.db.commit

    def makeDatabase(self, databaseName):
        self.databaseName = databaseName;
        try:
            self.cursor.execute("create database " + self.databaseName)
        except:
            self.cursor.execute("use " + self.databaseName)

    def makeTable(self, tableName, columns):
        try:
            self.tableName, self.columns = tableName, columns
            self.cursor.execute("create table " + tableName + " (" + columns + ");")
        except:
            return;

    def insertData(self, data):
        self.data = data;
        self.cursor.execute("insert into " + self.tableName + " values (" + ",".join(data) + ");")
        self.commit()


    @staticmethod
    def ex(command):
        self.cursor.execute(command)
        if command.find("insert") is not -1: self.commit()

    @staticmethod
    def insert(self, tableName, parameters):
        command = "insert into " + tableName + " values(%s)"
        self.cursor.execute(command, parameters)
#Mysql Part End

