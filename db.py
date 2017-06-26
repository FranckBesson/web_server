# -*- coding: utf-8 -*-
import psycopg2, re, os

class Db:
  """Connexion à la base de données postgres de l'environnement Heroku."""

  def __init__(self):
    """Initiate a connection to the default postgres database."""
    self.conn = psycopg2.connect(
        database="d2nvt9m6b7m9ug",
        user="bnrajpvobvykxm",
        password="4006d0e5cb49a16653bb01c161212c206b09cc6d929ad59f497a93d212675e03",
        host="ec2-107-22-162-158.compute-1.amazonaws.com",
        port="5432"
    )
    self.cur = self.conn.cursor()

  def describeRow(self, row, columns, subkeys = None):
    dRow = dict()
    if subkeys == None:
      for (i,cName) in enumerate(columns):
        dRow[cName] = row[i]
    else:
      for (i,cName) in enumerate(columns):
        k = cName if cName not in subkeys else subkeys[cName]
        if k != "":
          dRow[k] = row[i]
    return dRow

  def rowcount(self):
    return self.cur.rowcount

  def lastrowid(self):
    return self.cur.lastrowid()

  def fetchall(self, subkeys = None):
    rows = []
    line = self.fetchone()
    while line != None:
      rows.append(line)
      line = self.fetchone()
    return rows

  def fetchone(self, subkeys = None):
    row = self.cur.fetchone()
    if row != None:
      columns = map(lambda d: d[0], self.cur.description)
      row = self.describeRow(row, columns, subkeys)
    return row

  def execute(self, sql, sqlParams=None):
    if sqlParams == None:
      self.cur.execute(sql)
    else:
      sql = re.sub(r"@\(([^\)]+)\)", "%(\g<1>)s", sql)
      self.cur.execute(sql, sqlParams)
    self.conn.commit()

  def select(self, sql, sqlParams=None, subkeys=None):
    self.execute(sql, sqlParams)
    return self.fetchall(subkeys)

  def close(self):
    self.cur.close()
    self.conn.close()

  def executeFile(self, filename):
    f = file(filename, "r")
    sql = f.read()
    f.close()
    self.execute(sql)

