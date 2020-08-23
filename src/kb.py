class Knowledge_base:
    def __init__(self):
        self.KB = []

    def add(self,sentence):
        if sentence not in self.KB:
            self.KB.append(sentence)

    def check(self,query):
        pass