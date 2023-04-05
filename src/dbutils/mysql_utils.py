#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/5 15:15
# @Author  : haifengzuishuai
# @Email   : dada0614@126.cm
# @File    : mysql_utils.py
from pymysql import connect
from pymysql.cursors import DictCursor  # 为了返回字典形式
"""
CREATE TABLE `random_file` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `file` varchar(500) DEFAULT NULL,
  `status` int(3) DEFAULT NULL COMMENT '1有效，2无效',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

"""

# 类和对象
# 对象是类的实例
# 类是抽象的
# 对象是具像的
class Random_file(object):
    def __init__(self):  # 创建对象同时要执行的代码
        self.conn = connect(
            host='127.0.0.1',
            port=1111,
            user='root',
            password='123123',
            database='work1',
            charset='utf8'
        )
        self.cursor = self.conn.cursor(DictCursor)  # 这个可以让他返回字典的形式

    def __del__(self):  # 释放对象同时要执行的代码
        self.cursor.close()
        self.conn.close()

    def get_random_file(self):
        self.conn.ping(reconnect=True)
        sql = 'select id,file from random_file  WHERE `status`!=2 ORDER BY RAND()  LIMIT 1;'
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def insert_filename(self, filename):
        try:
            self.conn.ping(reconnect=True)
            sql = "INSERT INTO `work1`.`random_file` (`file`, `status`) VALUES ('{}', 1);".format(filename)
            self.cursor.execute(sql)
            self.conn.commit()
            return '200'
        except Exception as e:
            print(e)
            return e

    def invalid_file(self, filename):
        try:
            self.conn.ping(reconnect=True)
            sql = "UPDATE `random_file` SET `status` = 2 WHERE `file` = '{}';".format(filename)
            self.cursor.execute(sql)
            self.conn.commit()
            return '200'
        except Exception as e:
            print(e)
            return e
