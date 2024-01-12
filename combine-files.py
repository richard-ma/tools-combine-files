# !/usr/bin/env python
# APP Framework 1.0
import copy
import csv
import os
import sys
import shutil
import requests
from pprint import pprint


class App:
    def __init__(self):
        self.title_line = sys.argv[0]
        self.counter = 1
        self.workingDir = None

    def printCounter(self, data=None):
        print("[%04d] Porcessing: %s" % (self.counter, str(data)))
        self.counter += 1

    def initCounter(self, value=1):
        self.counter = value

    def run(self):
        self.usage()
        self.process()
        self.pressAnyKeyToContinue()

    def usage(self):
        print("*" * 80)
        print("*", " " * 76, "*")
        print(" " * ((80 - 12 - len(self.title_line)) // 2),
              self.title_line,
              " " * ((80 - 12 - len(self.title_line)) // 2))
        print("*", " " * 76, "*")
        print("*" * 80)

    def input(self, notification, default=None):
        var = input(notification)

        if len(var) == 0:
            return default
        else:
            return var

    def readTxtToList(self, filename, encoding="GBK"):
        data = list()
        with open(filename, 'r+', encoding=encoding) as f:
            for row in f.readlines():
                # remove \n and \r
                data.append(row.replace('\n', '').replace('\r', ''))
        return data

    def readCsvToDict(self, filename, encoding="GBK"):
        data = list()
        with open(filename, 'r+', encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def writeCsvFromDict(self, filename, data, fieldnames=None, encoding="GBK", newline=''):
        if fieldnames is None:
            fieldnames = data[0].keys()

        with open(filename, 'w+', encoding=encoding, newline=newline) as f:
            writer = csv.DictWriter(f,
                                    fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def addSuffixToFilename(self, filename, suffix):
        filename, ext = os.path.splitext(filename)
        return filename + suffix + ext

    def getWorkingDir(self):
        return self.workingDir

    def setWorkingDir(self, wd):
        self.workingDir = wd
        return self.workingDir

    def getFilesFromDir(self, path, only_file=True, filter_with_ext=''):
        for file in os.listdir(path):
            if only_file:
                if os.path.isfile(os.path.join(path, file)):
                    if len(filter_with_ext) == 0:
                        yield file
                    elif len(filter_with_ext) > 0 and file.endswith(filter_with_ext):
                        yield file
                    else:
                        continue
                else:
                    continue
            else:
                yield file

    def setWorkingDirFromFilename(self, filename):
        return self.setWorkingDir(os.path.dirname(filename))

    def pressAnyKeyToContinue(self):
        os.system('pause')

    def process(self):
        pass


class MyApp(App):
    def __init__(self):
        super().__init__()
        self.settings = {
            'input_dir': '.',
            'output_file': 'output.csv',
        }

    def process(self):
        # set input
        input_dir = self.settings['input_dir']
        # pprint(input_dir)

        # set working directory
        self.setWorkingDir(input_dir)
        # pprint(self.workingDir)

        # set output
        output_filename = self.settings['output_file']
        # pprint(output_filename)

        # get files
        output_data = list()

        for file in self.getFilesFromDir(input_dir, filter_with_ext='csv'):
            filename = os.path.join(input_dir, file)
            print("Processing: %s" % (filename))
            # read data
            data = self.readCsvToDict(filename, encoding='UTF-8-sig')
            for line in data:
                output_data.append(line)

        print("Writing to file: %s" % (output_filename))
        # write data
        self.writeCsvFromDict(output_filename, output_data, encoding='UTF-8-sig')


if __name__ == "__main__":
    app = MyApp()
    app.run()
