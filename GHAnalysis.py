import json
import os
import argparse


class Init_data:
    def __init__(self, dic_addr: int = None, reload: int = 0):
        if reload == 1:
            self.__init(dic_addr)
        if dic_addr is None and not os.path.exists('1.json') and not os.path.exists('2.json') and not os.path.exists('3.json'):
            raise RuntimeError('error: init failed')
        x = open('1.json', 'r', encoding='utf-8').read()
        self.CountOfPerP = json.loads(x)
        x = open('2.json', 'r', encoding='utf-8').read()
        self.CountOfPerR = json.loads(x)
        x = open('3.json', 'r', encoding='utf-8').read()
        self.CountAll = json.loads(x)

    def __init(self, dic_addr: str):
        self.CountOfPerP = {}
        self.CountOfPerR = {}
        self.CountAll = {}
        json_list = []
        for root, dic, files in os.walk(dic_addr):
            for f in files:
                if f[-5:] == '.json':
                    json_path = f
                    x = open(dic_addr+'\\'+json_path,
                             'r', encoding='utf-8').read()
                    str_list = [_x for _x in x.split('\n') if len(_x) > 0]
                    for i, _str in enumerate(str_list):
                        try:
                            json_list.append(json.loads(_str))
                        except:
                            pass
        records = self.__database(json_list)
        for i in records:
            if not self.CountOfPerP.get(i['actor__login'], 0):
                self.CountOfPerP.update({i['actor__login']: {}})
                self.CountAll.update({i['actor__login']: {}})
            self.CountOfPerP[i['actor__login']][i['type']
                                         ] = self.CountOfPerP[i['actor__login']].get(i['type'], 0)+1
            if not self.CountOfPerR.get(i['repo__name'], 0):
                self.CountOfPerR.update({i['repo__name']: {}})
            self.CountOfPerR[i['repo__name']][i['type']
                                       ] = self.CountOfPerR[i['repo__name']].get(i['type'], 0)+1
            if not self.CountAll[i['actor__login']].get(i['repo__name'], 0):
                self.CountAll[i['actor__login']].update({i['repo__name']: {}})
            self.CountAll[i['actor__login']][i['repo__name']][i['type']
                                                          ] = self.CountAll[i['actor__login']][i['repo__name']].get(i['type'], 0)+1
        with open('1.json', 'w', encoding='utf-8') as f:
            json.dump(self.CountOfPerP,f)
        with open('2.json', 'w', encoding='utf-8') as f:
            json.dump(self.CountOfPerR,f)
        with open('3.json', 'w', encoding='utf-8') as f:
            json.dump(self.CountAll,f)

    def __parseDict(self, d: dict, prefix: str):
        _d = {}
        for k in d.keys():
            if str(type(d[k]))[-6:-2] == 'dict':
                _d.update(self.__parseDict(d[k], k))
            else:
                _k = f'{prefix}__{k}' if prefix != '' else k
                _d[_k] = d[k]
        return _d

    def __database(self, a: list):
        records = []
        for d in a:
            _d = self.__parseDict(d, '')
            records.append(_d)
        return records

    def Result_Of_Users(self, user: str, event: str) -> int:
        if not self.CountOfPerP.get(user,0):
            return 0
        else:
            return self.CountOfPerP[user].get(event,0)

    def Result_Of_Repos(self, repo: str, event: str) -> int:
        if not self.CountOfPerR.get(repo,0):
            return 0
        else:
            return self.CountOfPerR[repo].get(event,0)

    def Result_Of_UsersAndRepos(self, user: str, repo: str, event: str) -> int:
        if not self.CountOfPerP.get(user,0):
            return 0
        elif not self.CountAll[user].get(repo,0):
            return 0
        else:
            return self.CountAll[user][repo].get(event,0)


class Run:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.Init_data = None
        self.argInit()
        print(self.analyse())

    def argInit(self):
        self.parser.add_argument('-i', '--init')
        self.parser.add_argument('-u', '--user')
        self.parser.add_argument('-r', '--repo')
        self.parser.add_argument('-e', '--event')

    def analyse(self):
        if self.parser.parse_args().init:
            self.Init_data = Init_data(self.parser.parse_args().init, 1)
            return 0
        else:
            if self.Init_data is None:
                self.Init_data = Init_data()
            if self.parser.parse_args().event:
                if self.parser.parse_args().user:
                    if self.parser.parse_args().repo:
                        res = self.Init_data.Result_Of_UsersAndRepos(
                            self.parser.parse_args().user, self.parser.parse_args().repo, self.parser.parse_args().event)
                    else:
                        res = self.Init_data.Result_Of_Users(
                            self.parser.parse_args().user, self.parser.parse_args().event)
                elif self.parser.parse_args().repo:
                    res = self.Init_data.Result_Of_Repos(
                        self.parser.parse_args().repo, self.parser.parse_args().event)
                else:
                    raise RuntimeError('error: argument -l or -c are required')
            else:
                raise RuntimeError('error: argument -e is required')
        return res


if __name__ == '__main__':
    a = Run()