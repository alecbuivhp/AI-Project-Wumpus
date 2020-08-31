class Knowledge_base:
    def __init__(self):
        self.KB = []

    def add(self, sentence):
        if sentence not in self.KB:
            self.KB.append(sentence)

    def compare(self, query1, query2):
        if len(query1) == 1:
            for item in query2:
                if query1[0][0] == "~" and item[0:] == query1[0][1:]:
                    query2.remove(item)
                elif item[0] == "~" and item[1:] == query1[0][0:]:
                    query2.remove(item)


    def check(self,query):
        KB_temp = self.KB.copy()
        KB_temp.append(query)
        for item1 in KB_temp:
            if len(item1) > 0:
                for item2 in KB_temp:
                    self.compare(item1,item2)
            else:
                return True
        return False


    def remove(self,sentence):
        for clause in self.KB:
            if len(clause) == 0:
                self.KB.remove(clause)
            for item in clause:
                if item == sentence or item == ('~'+item):
                    self.KB.remove(item)
