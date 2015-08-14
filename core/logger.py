texts = {
    "error": "[ERROR]",
    "debug": "[DEBUG]",
    "warning": "[WARN]"
    }

try:
    from colorama import init, Fore, Back, Style
    init()
    texts = {
        "error": Fore.BLACK + Back.RED + texts["error"] + Fore.RESET + Back.RESET,
        "debug": Fore.GREEN + texts["debug"] + Fore.RESET,
        "warning": Fore.RED + Back.YELLOW + texts["warning"] + Fore.RESET + Back.RESET
    }
except ImportError:
    pass

import datetime, time

class LoggerClass(object):

    def __log(self,text, type=None):
        global texts
        ts = "[%s]" % datetime.date.fromtimestamp(time.time()).strftime("%d-%m-%Y %H:%M:%S")
        if type in texts.keys():
            ts = "%s %s" % (ts, texts[type])
        print("%s %s" % (ts, text))

    def log(self,text):
        self.__log(text)

    def error(self,text):
        self.__log(text)

    def debug(self,text):
        self.__log(text)