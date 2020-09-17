import argparse
import json
import os
class InputData:

    def __init__(self, path: str = None):
        self.__dir_addr = path

        if path:
            print("初次运行初始化")
            if not os.path.exists(self.__dir_addr):
                raise RuntimeError("Path doesn't exist.")
            self.Init()
            self.Analysis()
            self.__save2json()
        else:
            self.sovle()

    def Init(self):
        self.__dicts = []
        for root, dirs, files in os.walk(self.__dir_addr):
            for file in files:
                if file[-5:] == '.json' and file[-6:] != '1.json' and file[-6:] != '2.json' and file[-6:] != '3.json':
                    with open(file, 'r', encoding='utf-8') as f:
                        self.__jsons = [x for x in f.read().split('\n') if len(x) > 0]
                        for self.__json in self.__jsons:
                            self.__dicts.append(json.loads(self.__json))

    def Analysis(self):
        self.__types = ['PushEvent', 'IssueCommentEvent', 'IssuesEvent', 'PullRequestEvent']
        self.CountOfPerP = {}
        self.CountOfPerR = {}
        self.CountOfPerPperR = {}

        for self.__dict in self.__dicts:
            # 如果属于四种事件之一 则增加相应值
            if self.__dict['type'] in self.__types:
                self.__event = self.__dict['type']
                self.__name = self.__dict['actor']['login']
                self.__repo = self.__dict['repo']['name']
                self.CountOfPerP[self.__name + self.__event] = self.CountOfPerP.get(self.__name + self.__event, 0) + 1
                self.CountOfPerR[self.__repo + self.__event] = self.CountOfPerR.get(self.__repo + self.__event, 0) + 1
                self.CountOfPerPperR[self.__name + self.__repo + self.__event] = self.CountOfPerPperR.get(
                    self.__name + self.__repo + self.__event, 0) + 1

    def __save2json(self):
        with open("1.json", 'w', encoding='utf-8') as f:
            json.dump(self.CountOfPerP, f)
        with open("2.json", 'w', encoding='utf-8') as f:
            json.dump(self.CountOfPerR, f)
        with open("3.json", 'w', encoding='utf-8') as f:
            json.dump(self.CountOfPerPperR, f)
        print("Save to json files successfully!")

    def sovle(self):
        self.CountOfPerP = {}
        self.CountOfPerR = {}
        self.CountOfPerPperR = {}
        with open("1.json", encoding='utf-8') as f:
            self.CountOfPerP = json.load(f)
        with open("2.json", encoding='utf-8') as f:
            self.CountOfPerR = json.load(f)
        with open("1.json", encoding='utf-8') as f:
            self.CountOfPerPperR = json.load(f)

    # get value from dictionary

    def get_cnt_user(self, user: str, event: str) -> int:
        return self.CountOfPerP.get(user + event, 0)

    def get_cnt_repo(self, repo: str, event: str) -> int:
        return self.CountOfPerR.get(repo + event, 0)

    def get_cnt_user_and_repo(self, user, repo, event) -> int:
        return self.CountOfPerPperR.get(user + repo + event, 0)
def run():
    my_parser = argparse.ArgumentParser(description='analysis the json file')
    my_parser.add_argument('-i', '--init', help='json file path')
    my_parser.add_argument('-u', '--user', help='username')
    my_parser.add_argument('-r', '--repo', help='repository name')
    my_parser.add_argument('-e', '--event', help='type of event')
    args = my_parser.parse_args()

    if args.init:
        my_InputData = InputData(path=args.init)
    else:
        my_InputData = InputData()
        if args.event:
            if args.user:
                if args.repo:
                    print(my_InputData.get_cnt_user_and_repo(args.user, args.repo, args.event))
                else:
                    print(my_InputData.get_cnt_user(args.user, args.event))
            else:
                if args.repo:
                    print(my_InputData.get_cnt_repo(args.repo, args.event))
                else:
                    print("missing argument: user or repo")
        else:
            print("missing argument: event")



if __name__ == '__main__':
    run()
