import requests
import codecs
import os
from slack_sdk import WebClient
from datetime import datetime

class Download:
    def __init__(self,channe_dic,channel_id_list):
        self.save_folder = r"\\registry\\"
        self.token = 'xoxb-'
        self.authorization = 'Bearer ' + self.token
        self.channel_dic = channel_dic
        self.channel_id_list = channel_id_list
        self.today = datetime.today()

    def create_folder(self):
        print("start:create_folder")
        for channel_id in self.channel_id_list:
            channel_name = self.channel_dic[channel_id][0]
            os.makedirs(self.save_folder + channel_name, exist_ok = True)
        print("end:create_folder")

    def get_content(self,url,save_name,channel_name):
        print("start:get_content")
        content = requests.get(url,allow_redirects=True,headers={'Authorization' : self.authorization}).content
        file_path = self.save_folder + channel_name + "\\" + save_name
        with open(file_path,'wb') as f:
            f.write(content)
        print("end:get_content")

    def download(self):
        print("start:download")
        self.create_folder()
        """
        for channel_id in self.channel_id_list:
            for file_list in self.channel_dic[channel_id][1]:
                channel_name = self.channel_dic[channel_id][0]
                ts = file_list['ts']
                delta = self.today - ts
                if delta.days > 3:
                    url = file_list['url']
                    save_name = file_list['name']
                    self.get_content(url,save_name,channel_name)
        """
        print("end:download")

class Read_message:
    def __init__(self):
        self.client = WebClient(token = os.environ.get("SLACK_BOT_TOKEN"))
        self.file_list = []
        self.ver_dic = {}

    def get_history(self,channel_id):
        print("start:get_history")
        result = self.client.conversations_history(channel = channel_id)
        conversation_history = result["messages"]
        print("end:get_hisotry")
        return conversation_history

    def edit_name(self,name):
        print("start:edit_name")
        type = name.split(".")[-1]

        """ version表記用
        name = name.rstrip("." + type)

        if name in self.ver_dic:
            self.ver_dic[name] = self.ver_dic[name] +1
        else:
            self.ver_dic[name] = 1
        name = name + "_ver" + str(self.ver_dic[name]) + "." + type
        """
        print("end:edit_name")
        return name,type

    def return_file_list(self,conversation_history):
        print("start:return_file_list")
        self.file_list = []
        for i in conversation_history:
            if 'files' in i:
                history_file = i['files'][0]

                name = history_file['name']
                result = self.edit_name(name)
                name = result[0]
                type = result[1]

                ts = datetime.fromtimestamp(history_file['timestamp'])
                url = history_file['url_private_download']

                dic = {'name':name,'type':type,'ts':ts,'url':url}
                self.file_list.append(dic)
        print("end:return_file_list")

    def get_channel_id(self):
        print("start:get_channel_id")
        self.channel_id_list = []
        self.channel_dic = {}
        result = self.client.conversations_list()
        conversations = result["channels"]
        for i in conversations:
            id = i["id"]
            name = i["name"]
            self.channel_id_list.append(id)
            self.channel_dic[id] = []
            self.channel_dic[id].append(name)
            try:
                self.client.conversations_join(channel = id)
            except:
                print(1)
        print("end:get_channel_id")

    def read_message(self):
        print("start:read_message")
        self.get_channel_id()
        for i in self.channel_id_list:
            try:
                print(i)
                conversation_history = self.get_history(i)
                self.return_file_list(conversation_history)
                self.channel_dic[i].append(self.file_list)
            except:
                print("ERROR")
        print("end:read_message")
        return self.channel_dic,self.channel_id_list

print("start")
print("start:Read_message")
read_message = Read_message()
result = read_message.read_message()
print("end:Read_message")
channel_dic = result[0]
channel_id_list = result[1]

print("start:Download")
download = Download(channel_dic,channel_id_list)
download.download()
print("end:Download")
print("finish")
