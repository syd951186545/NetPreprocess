# _*_ coding:utf-8 _*_
import json

import codecs

__AUTHOR__ = "syd"


# DATA:2018/7/19
# PROJECT:Pyworkplace

class Transform:
    def __init__(self, inpath, outpath):
        self.inpath = inpath
        self.outpath = outpath
        # TODO

    def trans2maxtix(self):

        with codecs.open(self.inpath, "r", "utf-8") as f:
            with codecs.open(self.outpath, "w", "utf-8") as f2:
                for line in f:
                    i = 0
                    X_X = json.loads(line)
                    keys = X_X.keys()
                    for key in keys:
                        values = X_X.get(key)
                        for value in values:
                            i = i + 1
                            # if i < 20:
                            f2.writelines(key + " " + value + "\n")
                            # else:
                            #     return 0

    def trans2num(self):
        with codecs.open(self.inpath, "r", "utf-8") as f:
            with codecs.open(self.outpath, "w", "utf-8") as f2:
                for line in f:
                    i = 0
                    j = 0
                    p2num = {}
                    X_X = json.loads(line)
                    keys = X_X.keys()
                    for key in keys:
                        j = j + 1
                        p2num.update({key: j})
                    for key in keys:
                        values = X_X.get(key)
                        for value in values:
                            numvalues = p2num.get(value)
                            if numvalues:
                                i = i + 1
                                f2.writelines(str(p2num.get(key)) + " " + str(numvalues) + "\n")
                f2.writelines("numeber of paper:{}  number of edge:{}".format(j, i))


if __name__ == "__main__":
    inpath = "E:\ALLworkspace\Pyworkplace\dblp-ref\P_P.json"
    outpath = "E:\ALLworkspace\Pyworkplace\dblp-ref\P_P2mat.txt"
    datatrans = Transform(inpath, outpath)
    datatrans.trans2maxtix()
