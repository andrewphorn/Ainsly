try:
    from colorama import init, Fore, Back, Style
    init()
    colored = True
except ImportError:
    colored = False

import datetime, time

class LoggerClass(object):
    def __log(self,text):
        ts = "[%s]" % datetime.date.today().strftime("%d-%m-%Y %H:%M:%S")

    def log(self,text):
        self.__log(text)

    def error(self,text):
        self.__log(text)

    def debug(self,text):
        self.__log(text)