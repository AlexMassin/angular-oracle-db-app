# angular-oracle-db-app
# Frontend
## Stack
Lang: HTML, CSS, Javascript, Typescript <br>
Framework: Angular 9 <br>
Style: Material <br>

## Angular
### Installation
`$ sudo npm install -g @angular/cli` <br>
`$ sudo npm install --save-dev @angular-devkit/build-angular` <br>
`$ sudo ng update` <br>
`$ sudo npm update`

### Set Up Packages
`$ cd front-end` <br>
`$ sudo npm install`

### Start the Developmental Server
`$ cd front-end` <br>
`$ sudo npm start`

# Backend
## Stack
Lang: Python <br>
DB: Oracle <br>
DB Comms: SQLAlchemy <br>
Background Worker: Celery <br>
Message Broker: Redis <br>

## Oracle DB Connection Setup
Located in `back-end/modules/config.py`: <br>
Change username, password, etc

## Redis Server
### Installation
`$ sudo apt update` <br>
`$ sudo apt install redis-server`

### Prevent Server Startup on Boot
If Redis was not installed on a server or a container, remove it from automatically starting on boot.

`$ sudo systemctl disable redis-server`

### Starting/Stopping/Restarting Redis
`$ sudo service redis-server start` <br>
`$ sudo service redis-server stop` <br>
`$ sudo service redis-server restart`

<strong>Never use kill to stop the server!</strong>

### Configure Server
`$ sudo vim /etc/redis/redis.conf`

Change the following:
```
supervised no
```
To this: <br>
```
supervised systemd
```
### Test Server

`$ redis-cli ping`

### Monitor Server

`$ redis-cli --slave`

## Celery Worker
### Start Worker and Monitor
```sh
$ cd back-end
$ celery -A modules.apis.v1.db_controller.worker worker --loglevel=info
```

## Oracle DB
### Linking CX Oracle
> `instantclient_19_9` zip included in backend.

Running the following <strong>after unzipping</strong> will setup the required dependencies:
```sh
$ chmod 755 link_cx.sh
$ . link_cx.sh
```

### Starting the DB
Make sure OracleServiceORCL is running.

In SQLPlus:
```sh
username: "/" as sysdba
password:

startup
```

### Starting SQLDeveloper
Make sure the listener is running.

In PowerShell:
```powershell
> lsnrctl start
```

## Full Stack Scripts
### Start Everything
`. start_dev.sh` <br>
Note: Angular can take a few seconds to start up
### Stop Everything
`. stop_dev.sh`