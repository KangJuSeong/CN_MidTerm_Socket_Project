DB_PATH = "./DB.txt"


class DataBaseManager():

    def __init__(self):
        self.db = open(DB_PATH, 'r')

    def readData(self):
        self.db = open(DB_PATH, 'r')
        data = self.db.readlines()
        self.disConnect()
        return data

    def writeData(self, data):
        self.db = open(DB_PATH, 'w')
        self.db.write(data)
        self.disConnect()

    def selectDB(self):
        data = {}
        read_data = self.readData()
        for line in read_data:
            line = line[:-1]
            k, v = line.split(':')
            data[k] = v
        return data

    def insertDB(self, insert_k, insert_v):
        data = self.selectDB() 
        str_data = ""
        insert_flag = True
        for k, v in data.items():
            if k == insert_k:
                insert_flag = False
            str_data += f"{k}:{v}\n"
        if insert_flag:
            str_data += f"{insert_k}:{insert_v}\n"
        self.writeData(str_data)
        
        if insert_flag:
            return self.selectDB()
        else:
            return "Aleady Exist Key"

    def updateDB(self, target_k, update_v):
        data = self.selectDB()
        str_data = ""
        update_flag = False
        for k, v in data.items():
            if k == target_k:
                str_data += f"{target_k}:{update_v}\n"
                update_flag = True
            else:
                str_data += f"{k}:{v}\n"
        self.writeData(str_data)

        if update_flag:
            return self.selectDB() 
        else:
            return "Not Exist Key"

    def disConnect(self):
        self.db.close()


if __name__ == '__main__':
    db_manager = DataBaseManager()
    print(db_manager.updateDB('test', 'four'))
