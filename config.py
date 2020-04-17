import os
import sqlite3

conn = sqlite3.connect ('inginious.sqlite')

c = conn.cursor ()

c.execute ("SELECT * FROM user_tasks WHERE succeeded = 'false' and task = 'palindrome'")
no = len(c.fetchall())   #info qui devrait être introduit dans le graphe
c.execute ("SELECT * FROM user_tasks WHERE succeeded = 'true' and task = 'palindrome'")
yes = len(c.fetchall())  #info qui devrait être introduit dans le graphe


conn.close()

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'inginious.sqlite')