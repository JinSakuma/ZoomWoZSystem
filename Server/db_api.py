import MySQLdb
import pandas as pd


class DB_API():
    def __init__(self, config):
        self.host = config['DB']['host']
        self.db_name = config['DB']['db_name']
        self.user = config['DB']['user']
        self.passwd = config['DB']['password']

    def sql_execute(self, sql_order, columns):
        connector = MySQLdb.connect(host=self.host, db=self.db_name, user=self.user, passwd=self.passwd, use_unicode=True, charset="utf8")
        cursor = connector.cursor()
        try:
            cursor.execute(sql_order)
            result = cursor.fetchall()
            df = pd.DataFrame(result, columns=columns)
        finally:
            cursor.close()
            connector.commit()
            connector.close()

        return df

    def search_movie(self):
        sql_order = "SELECT * FROM main"
        columns = ["movie_id", "title", "pronounciation", "evaluation", "vote", "popularity", "date"]
        df = self.sql_execute(sql_order, columns=columns)
        return df

    def search_movie_by_id(self, movie_id):
        sql_order = "SELECT * FROM main WHERE movie_id = '{}'".format(movie_id)
        columns = ["movie_id", "title", "pronounciation", "evaluation", "vote", "popularity", "date"]
        df = self.sql_execute(sql_order, columns=columns)
        return df

    def search_movie_by_title(self, title):
        sql_order = "SELECT * FROM main WHERE title LIKE '%{}%'".format(title)
        columns = ["movie_id", "title", "pronounciation", "evaluation", "vote", "popularity", "date"]
        df = self.sql_execute(sql_order, columns=columns)
        return df

    def search_movie_by_genre(self, genre_id):
        sql_order = "SELECT * FROM main WHERE movie_id = ANY (SELECT movie_id FROM genre WHERE genre_id = '{}')".format(genre_id)
        columns = ["movie_id", "title", "pronounciation", "evaluation", "vote", "popularity", "date"]
        df = self.sql_execute(sql_order, columns=columns)
        return df

    def search_movie_by_crew(self, person_id, job_id=None):
        if job_id is None:
            sql_order = "SELECT * FROM main WHERE movie_id = ANY (SELECT movie_id FROM crew WHERE person_id = '{}')".format(person_id)
        else:
            sql_order = "SELECT * FROM main WHERE movie_id = ANY (SELECT movie_id FROM crew WHERE person_id = '{}' and job_id = '{}')".format(person_id, job_id)
        columns = ["movie_id", "title", "pronounciation", "evaluation", "vote", "popularity", "date"]
        df = self.sql_execute(sql_order, columns=columns)
        return df

    def get_genre(self, movie_id):
        sql_order = "SELECT genre_id FROM genre WHERE movie_id = '{}'".format(movie_id)
        columns = ["genre_id"]
        df = self.sql_execute(sql_order, columns=columns)
        return df

    def get_crew(self, movie_id, job_id):
        sql_order = "SELECT name_en, name_ja FROM person WHERE person_id = ANY (SELECT person_id FROM crew WHERE movie_id = '{}' and job_id = '{}')".format(movie_id, job_id)
        columns = ["name_en", "name_ja"]
        df = self.sql_execute(sql_order, columns=columns)
        return df

    def get_tips(self, movie_id):
        sql_order = "SELECT tips, tag FROM tips WHERE  movie_id = '{}'".format(movie_id)
        columns = ["tips", "tag"]
        df = self.sql_execute(sql_order, columns=columns)
        return df

    def get_review(self, movie_id):
        sql_order = "SELECT review FROM reviews WHERE  movie_id = '{}'".format(movie_id)
        columns = ["review"]
        df = self.sql_execute(sql_order, columns=columns)
        return df

    def get_credit(self, person_id):
        sql_order = "SELECT title FROM main WHERE movie_id = ANY (SELECT movie_id FROM crew WHERE person_id = '{}')".format(person_id)
        columns = ["title"]
        df = self.sql_execute(sql_order, columns=columns)
        return df

    def person2id(self, person):
        sql_order = "SELECT person_id FROM person WHERE name_en = '{}'".format(person)
        columns = ["person_id"]
        df = self.sql_execute(sql_order, columns=columns)
        if len(df) > 0:
            pid = df['person_id'].iloc[0]
        else:
            pid = None

        return pid

    def id2person(self, person_id):
        sql_order = "SELECT name_en, name_ja FROM person WHERE person_id = '{}'".format(person_id)
        columns = ["name_en", "name_ja"]
        df = self.sql_execute(sql_order, columns=columns)
        if len(df) > 0:
            name = df['name_en'].iloc[0]
        else:
            name = None
        return name

    def id2genre(self, genre_id):
        sql_order = "SELECT genre FROM genre_ids WHERE genre_id = '{}'".format(genre_id)
        columns = ["genre"]
        df = self.sql_execute(sql_order, columns=columns)
        if len(df) > 0:
            genre = df['genre'].iloc[0]
        else:
            genre = None

        return genre

    def genre2id(self, genre):
        sql_order = "SELECT genre_id FROM genre_ids WHERE genre = '{}'".format(genre)
        columns = ["genre_id"]
        df = self.sql_execute(sql_order, columns=columns)
        if len(df) > 0:
            genre_id = df['genre_id'].iloc[0]
        else:
            genre_id = None

        return genre_id
