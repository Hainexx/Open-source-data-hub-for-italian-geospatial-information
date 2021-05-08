import psycopg2 
import psycopg2.extras
import io
import os 
import traceback
import itertools
from io import StringIO

def get(dictionary, key, default=None, common_dictionary=None):
    if key in dictionary:
        return dictionary[key]
    elif common_dictionary is not None and key in common_dictionary:
        return common_dictionary[key]
    return default

def merge_dicts_priority(first, second):
    if first is None:
        return second
    if second is None:
        return first
    # common keys of second will be overwritten by first
    return {**second, **first}


class Query():
    def __init__(self, query, params=None, fast=False):
        self.query = query
        self.params = params
        self.fast = fast


class PostgreSQLManager():

    def __init__(self, user=None, password=None, host=None, port=None, database=None, variables_dict=None):
        super().__init__()
        variables_dict = merge_dicts_priority(variables_dict, os.environ)

        self.user =      get(variables_dict, "POSTGRESQL_USERNAME", default=None)    if user     is None else user 
        self.password =  get(variables_dict, "POSTGRESQL_PASSWORD", default=None)    if password is None else password 
        self.host =      get(variables_dict, "POSTGRESQL_HOST", default=None)        if host     is None else host 
        self.port =      get(variables_dict, "POSTGRESQL_PORT", default=None)        if port     is None else port 
        self.database =  get(variables_dict, "POSTGRESQL_DATABASE", default=None)    if database is None else database 


    def connect(self):
        # TODO IMPLEMENT RETRY POLICY
        # connection = psycopg2.connect(  user=os.getenv("POSTGRESQL_USERNAME"),
        #                                 password=os.getenv("POSTGRESQL_PASSWORD"),
        #                                 host=os.getenv("POSTGRESQL_HOST"),
        #                                 port=os.getenv("POSTGRESQL_PORT"),
        #                                 database=os.getenv("POSTGRESQL_DATABASE"))
        self.logger.info(f'Connecting to {self.user}@{self.host}:{self.port}/{self.database}.')
        self.connection = psycopg2.connect( user=self.user,
                                            password=self.password,
                                            host=self.host,
                                            port=self.port,
                                            database=self.database)

    
    def disconnect(self):
        if self.connection is not None:
            if not self.connection.closed:
                self.logger.info(f'Disconnecting from {self.user}@{self.host}:{self.port}/{self.database}.')
                self.connection.close()

    def query_execute_many(self, query: Query, commit=False, fetch=False, aslist=False, asdataframe=False, columns=None):

        cursor      = None
        try:
            connection = self.get_connection()

            cursor = connection.cursor()

            psycopg2.extras.execute_batch(cursor, query.query, query.params, page_size=500)

            if commit:
                connection.commit()

        except:
            print(traceback.format_exc())
        finally:
            cursor.close()


    def query_execute(self, query: Query, commit=False, fetch=False, aslist=False, asdataframe=False, columns=None):
        cursor      = None
        try:
            connection = self.get_connection()

            cursor = connection.cursor()

            if query.params is None:
                cursor.execute(query.query)
            else:
                cursor.execute(query.query, query.params)

            results = None

            if fetch:
                results = []
                row = cursor.fetchone()
                while row:
                    results_list = list()
                    for el in list(row):
                        if isinstance(el, str):
                            results_list.append(el.strip())
                        elif isinstance(el, float):
                            results_list.append(round(el, 7))  # TODO
                        else:
                            results_list.append(el)
                    results.append(results_list)
                    row = cursor.fetchone()
                    
            if commit:
                connection.commit()

            if results is not None and aslist:
                results = list(itertools.chain(*results))
            elif results is not None and asdataframe:
                import pandas
                results = pandas.DataFrame(results, columns=columns)

            return results
        except:
            print(traceback.format_exc())
        finally:
            cursor.close()


    def query_execute_list(self, query_list, commit=False):
        cursor      = None
        try:
            connection = self.get_connection()

            cursor = connection.cursor()

            for query in query_list:
                
                if query.params is None:
                    cursor.execute(query.query)
                else:
                    if len(query.params) > 0:
                        cursor.executemany(query.query, query.params)          
                    
            if commit:
                connection.commit()


        except:
            if cursor is not None:
                cursor.rollback()

            print(traceback.format_exc())
        finally:
            cursor.close()


    def query_execute_copy(self, df, destination_table, columns=None, commit=False):
        cursor      = None
        try:
            connection = self.get_connection()

            cursor = connection.cursor()
            
            f = StringIO()
            df.to_csv(f, sep=',', header=False, index=False, quoting=3)
            f.seek(0)

            cursor.copy_from(f, destination_table, columns=columns, sep=',')

            if commit:
                connection.commit()

        except:
            if connection is not None:
                print('ROLLBACK')
                connection.rollback()

            print(traceback.format_exc())
        finally:
            cursor.close()
