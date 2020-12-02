# @author Alex Gomes
# @create date 2020-11-09 22:07:53
# @modify date 2020-12-01 23:18:35
# @desc [Config for the API versions and any necessary components.]

config = {
    'LATEST_API_VERSION': 'api/v1',
    'CELERY_BROKER_URL': 'redis://localhost:6379/0',
    'CELERY_RESULT_BACKEND': 'redis://localhost:6379/0',

    'SQL_DIALECT': 'oracle',
    'SQL_DRIVER': 'cx_oracle',
    'USERNAME': 'c##alex',
    'PASSWORD': 'cps510project',
    'HOST': 'localhost',
    'PORT': 1521,
    'SID': 'orcl',

    'CX_LIB': r'/mnt/c/Users/Alex/Documents/GitHub/angular-oracle-db-app/back-end/instantclient_19_9',

    'ERR_EXCPTS': ['This result object does not return rows. It has been closed automatically.']
}