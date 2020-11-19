# @author Alex Gomes
# @create date 2020-11-09 20:02:13
# @modify date 2020-11-18 21:58:16
# @desc [Entry point for the backend.]

from modules import app

if __name__ == '__main__':
    app.run(debug=True)
