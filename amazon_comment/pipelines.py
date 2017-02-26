# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector

import mysql.connector
from mysql.connector import errorcode
from amazon_comment.items import AmazonProductItem
from amazon_comment.items import AmazonCommentItem


class AmazonCommentPipeline(object):

    config = {
        'user': 'root',
        'password': 'root',
        'host': '127.0.0.1',
        'database': 'amazon'
    }


    def AmazonCommentPipeline(self):
        self.open_connection()


    def open_connection(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with username or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database dosen't exist")
            else:
                print(err)


    def close_connection(self):
        self.close()


    def process_item(self, item, spider):
        cursor = self.connection.cursor()

        if isinstance(item, AmazonProductItem):
            add_product = ("INSERT INTO product (amazon_product_id, img_url, detail_url, title, "
                           "update_time, create_time) VALUES (%s, %s, %s, %s, now(), now())") % \
                          (item['amazon_product_id'], item['img_url'], item['detail_url'], item['title'])
            cursor.execute(add_product)
        elif isinstance(item, AmazonCommentItem):
            add_comment = ("INSERT INTO comment (amazon_product_id, score, user, date, comment, support_peoples, "
                           "update_time, create_time) VALUES (%s, %s, %s, %s, %s, %s, now(), now())") % \
                          (item['amazon_product_id'], item['score'], item['user'], item['date'], item['comment'],
                           item['support_peoples'])
            cursor.execute(add_comment)
        return item
