import os
import sqlite3

class FlatFileStorage:

    def __init__(self, location='pastebin'):

        if not os.path.isdir(location):
            os.makedirs(location)

        if not os.path.isdir(os.path.join(location, 'metadata')):
            os.makedirs(os.path.join(location, 'metadata'))

        self.location = location
        # fill a hash where keys are ids of previously downloaded pastes for fast
        # de-duping lookups
        self.archived_scrape_pastes = { x[0:-4]: None for x in os.listdir(location) \
                                                      if len(x) == 8 + 4 and '.txt' in x }
        self.archived_trending_pastes = dict() \
            if not os.path.isdir(os.path.join(location, 'trending')) \
            else { x[0:-4]: None for x in os.listdir(os.path.join(location, 'trending')) \
                                 if len(x) == 8 + 4 and '.txt' in x }

    def has_paste_content(self, table, key):
        if table == 'trending_paste_content': return key in self.archived_trending_pastes
        else: return key in self.archived_scrape_pastes

    def save_paste_content(self, table, key, content):
        folder = self.location
        if table == 'trending_paste_content':
            folder = os.path.join(self.location, 'trending')
            if not os.path.isdir(folder):
                os.makedirs(folder)  
        filename = os.path.join(folder, '{}.txt'.format(key))
        with open(filename, 'wb') as f:
            f.write(content)
        if table == 'trending_paste_content': self.archived_trending_pastes[key] = None
        else: self.archived_scrape_pastes[key] = None

    def save_paste_reference(self, table, key, timestamp, size, expires, title, syntax, user=None, hits=None):
        column = 'user' if table == 'paste' else 'hits'
        value  = user if table == 'paste' else hits
        with open(os.path.join(self.location, 'metadata', '{}.txt'.format(key)), 'w') as f:
            data = 'key: {}\n'.format(key) + \
                   'timestamp: {}\n'.format(timestamp) + \
                   'size: {}\n'.format(size) + \
                   'expires: {}\n'.format(expires) + \
                   'title: {}\n'.format(title) + \
                   'syntax: {}\n'.format(syntax) + \
                   '{}: {}\n'.format(column, value)
            f.write(data)

class SQLite3Storage:
    def __init__(self, location='pastebin.db'):
        self.connection = sqlite3.connect(location)

    def initialize_tables(self, trending=False):

        try:
          self.connection.execute(
              '''
              CREATE TABLE IF NOT EXISTS paste (
                  paste_key CHAR(8) PRIMARY KEY,
                  timestamp TIMESTAMP,
                  size INT,
                  expires TIMESTAMP,
                  title TEXT,
                  syntax TEXT,
                  user TEXT NULL
              );
              '''
          )
        except sqlite3.OperationalError as err:
          print("[!] Error accessing database file: {}".format(err))
          print("[!] Fatal Error: Exiting...")
          exit(1)

        self.connection.execute(
            '''
            CREATE TABLE IF NOT EXISTS paste_content (
                paste_key CHAR(8) PRIMARY KEY,
                raw_content TEXT
            );
            '''
        )

        if trending:
            self.connection.execute(
                '''
                CREATE TABLE IF NOT EXISTS trending_paste (
                    paste_key CHAR(8) PRIMARY KEY,
                    timestamp TIMESTAMP,
                    size INT,
                    expires TIMESTAMP,
                    title TEXT,
                    syntax TEXT,
                    hits INT NULL
                );
                '''
            )

            self.connection.execute(
                '''
                CREATE TABLE IF NOT EXISTS trending_paste_content (
                    paste_key CHAR(8) PRIMARY KEY,
                    raw_content TEXT
                );
                '''
            )

    def has_paste_content(self, table, key):
        cursor = self.connection.cursor()

        cursor.execute('SELECT COUNT(*) FROM {} WHERE paste_key = ?'.format(table), (key,))

        paste_content_count = cursor.fetchone()[0]
        return paste_content_count > 0

    def save_paste_reference(self, table, key, timestamp, size, expires, title, syntax, user=None, hits=None):
        column = 'user' if table == 'paste' else 'hits'
        value  = user if table == 'paste' else hits
        self.connection.execute(
            '''
            INSERT OR REPLACE INTO {}
              (paste_key, timestamp, size, expires, title, syntax, {})
            VALUES
              (?, ?, ?, ?, ?, ?, ?)
            '''.format(table, column),
            (
                key,
                timestamp,
                size,
                expires,
                title,
                syntax,
                value,
            )
        )

#        self.connection.commit()

        try:
          self.connection.commit()
        except:
          print("no")
          raise

    def save_paste_content(self, table, key, content):
        self.connection.execute(
            '''
            INSERT OR REPLACE INTO {}
              (paste_key, raw_content)
            VALUES
              (?, ?)
            '''.format(table),
            (
                key,
                content,
            )
        )
