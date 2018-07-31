# _*_ coding:utf-8 _*_
# __AUTHOR__ = "syd"
# DATA:2018/7/18
# PROJECT:Pyworkplace

import json
import codecs


class DBLPPreprocess:
    """DBLP .json preprocessing"""

    def __init__(self, path):
        self.path = path
        # self.path2 = path2
        self.P_P = {}
        self.P_V = {}
        self.P_A = {}
        self.A_P = {}
        self.V_P = {}
        self.importanceOfvenue = 150  # 筛选会议论文数量高于此数的会议
        self.selectedVenues = ["SIGMOD", "ICDE", "VLDB", "EDBT",
                               "PODS", "ICDT", "DASFAA", "SSDBM", "CIKM", "KDD",
                               "ICDM", "SDM", "PKDD", "PAKDD", "IJCAI", "AAAI",
                               "NIPS", "ICML", "ECML", "ACML", "IJCNN", "UAI",
                               "ECAI", "COLT", "ACL", "KR", "CVPR", "ICCV",
                               "ECCV", "ACCV", "MM", "ICPR", "ICIP", "ICME",
                               "high performance computing and communications"]

        venues1 = ["SIGMOD", "ICDE", "VLDB", "EDBT",
                   "PODS", "ICDT", "DASFAA", "SSDBM", "CIKM"]

        venues2 = ["KDD", "ICDM", "SDM", "PKDD", "PAKDD"]

        venues3 = ["IJCAI", "AAAI", "NIPS", "ICML", "ECML",
                   "ACML", "IJCNN", "UAI", "ECAI", "COLT", "ACL", "KR"]

        venues4 = ["CVPR", "ICCV", "ECCV", "ACCV", "MM",
                   "ICPR", "ICIP", "ICME"]

    def getrelation(self):
        """
        整理出需要关系类型
        :return:
        """
        i = 0
        with codecs.open(self.path, "r", 'utf-8') as f:
            # with codecs.open(self.path2, "r", 'utf-8') as f2:
            # for line in f and f2 and f3 and f4:

            for line in f:
                data = json.loads(line)
                #  一条完整的信息应该包含id ,author,venue,ref
                if 'id' in data and "authors" in data \
                        and 'venue' in data and 'references' in data:
                    paperid = data.get('id')
                    authors = data.get("authors")
                    venue = data.get('venue')
                    references = data.get('references')

                    # 一条完整的信息,其各值不能是空的
                    if len(references) != 0 and len(venue) != 0 \
                            and len(authors) != 0:
                        venue = venue.replace(" ", "_")
                        j = 0
                        while j < len(authors):
                            authors[j] = authors[j].replace(" ", "_")
                            j = j + 1

                        for author in authors:
                            curauthor = self.A_P.setdefault(author, [])
                            curauthor.append(paperid)

                        curven = self.V_P.setdefault(venue, [])
                        curven.append(paperid)

                        p_a = {paperid: authors}
                        p_v = {paperid: venue}
                        p_p = {paperid: references}

                        self.P_A.update(p_a)
                        self.P_V.update(p_v)
                        self.P_P.update(p_p)

                        i = i + 1
                        if i % 100 == 0:
                            print("处理了{}条有效信息".format(i))
        return

    def picknode(self):
        """
        选择具有信息的P,,例如:如果一篇论文的引文不是我们的P节点(没有作者会议等信息),我们将其删掉
        :return:
        """
        print("#############论文P筛选##############")
        print(len(self.P_P))
        paperids = self.P_P.keys()
        for paperid in paperids:
            refpaperids = self.P_P.get(paperid)
            for refpaperid in refpaperids:
                if refpaperid not in list(paperids):
                    print("删除:不在数据集中的仅被引用的论文P:{}".format(refpaperid))
                    refpaperids.remove(refpaperid)
            # if len(refpaperids)!=0:
            self.P_P.pop(paperid)
            self.P_P.update({paperid: refpaperids})
        print(len(self.P_P))
        # with codecs.open("E:\\ALLworkspace\\Pyworkplace\\dblp-ref\\P_P.json", "w", "utf-8") as wf:
        #     pp = json.dumps(self.P_P)
        #     wf.write(pp)

        return

    def pickvenue(self):
        print("#############会议V筛选##############")
        # 从V_P中删除会议,更新V_P
        removevenue = []
        venues = self.V_P.keys()
        i = len(venues)
        for venue in venues:
            if len(self.V_P.get(venue)) <= self.importanceOfvenue:
                i = i - 1
                removevenue.append(venue)
        print(removevenue)
        for rv in removevenue:
            self.V_P.pop(rv)
            print("删除:论文数量较少的会议V:{}".format(rv))
        print("保留会议V数:{}".format(i))

        # 更新P_*
        venues2 = self.V_P.keys()
        paperids = self.P_V.keys()
        removepaper = []
        for paperid in paperids:
            if self.P_V.get(paperid) not in venues2:
                removepaper.append(paperid)
        for rv in removepaper:
            # 从V_P中删除了会议,更新V_P
            self.P_V.pop(rv)
            self.P_P.pop(rv)
            self.P_A.pop(rv)
            print("删除:发表在已删除会议上的论文P:{}".format(rv))
        print("保留论文P数:{}".format(len(self.P_P)))

        # 更新A_P
        removeauthor = []
        authors = self.A_P.keys()
        paperidsall = self.P_V.keys()
        for author in authors:
            paperids = self.A_P.get(author)
            for pap in paperids:
                if pap not in paperidsall:
                    paperids.remove(pap)

            if len(self.A_P.get(author)) == 0:
                removeauthor.append(author)
        for rv in removeauthor:
            self.A_P.pop(rv)
            print("删除:已删除论文的作者A:{}".format(rv))
        print("保留论文P数:{}".format(len(self.P_P)))
        print("保留会议V数:{}".format(i))
        print("保留作者A数:{}".format(len(self.A_P)))




    def output(self):
        """
        将关系pp,pv,pa,ap,vp输出到文件
        :return:
        """
        with codecs.open("E:\\ALLworkspace\\Pyworkplace\\dblp-ref\\P_P.json", "w", "utf-8") as wf:
            pp = json.dumps(self.P_P)
            wf.write(pp)
        with codecs.open("E:\\ALLworkspace\\Pyworkplace\\dblp-ref\\P_A.json", "w", "utf-8") as wf:
            pa = json.dumps(self.P_A)
            wf.write(pa)
        with codecs.open("E:\\ALLworkspace\\Pyworkplace\\dblp-ref\\P_V.json", "w", "utf-8") as wf:
            pv = json.dumps(self.P_V)
            wf.write(pv)
        with codecs.open("E:\\ALLworkspace\\Pyworkplace\\dblp-ref\\A_P.json", "w", "utf-8") as wf:
            ap = json.dumps(self.A_P)
            wf.write(ap)
        with codecs.open("E:\\ALLworkspace\\Pyworkplace\\dblp-ref\\V_P.json", "w", "utf-8") as wf:
            vp = json.dumps(self.V_P)
            wf.write(vp)

        with codecs.open("E:\\ALLworkspace\\Pyworkplace\\dblp-ref\\number.json", "w", "utf-8") as wf:
            numberofpapers = len(self.P_P)
            numberofauthors = len(self.A_P)
            numberofvenues = len(self.V_P)

            dic = {"numberofPapers": numberofpapers, \
                   "numberofAuthors": numberofauthors, \
                   "numberofVenues": numberofvenues,
                   # "P_A":len(self.P_A),
                   # "P_V":len(self.P_V)
                   }
            wf.write(json.dumps(dic))
        return


if __name__ == "__main__":
    path = "E:\\ALLworkspace\\Pyworkplace\\dblp-ref\\DBLPdataset\\dblp-ref-3.json"
    path2 = "E:\\ALLworkspace\\Pyworkplace\\dblp-ref\\DBLPdataset\\dblp-ref-1.json"
    dblpref = DBLPPreprocess(path)
    dblpref.getrelation()  # 获取完整的APV关系信息
    # dblpref.picknode()  # 筛选P的应用论文,更新P_P,P_P的关系太少,不推荐用
    dblpref.pickvenue()  # 刷选保留的会议V,更新V_P,同时再次会更新其他所有关系

    dblpref.output()  # 输出
