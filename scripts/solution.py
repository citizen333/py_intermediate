class File:
    def __init__(self, file_name):
        self.file_name = file_name
        
    def read(self):
        with open(self.file_name, 'r') as f:
            file_text = f.read()
        return file_text
    
    def write(self, text):
        with open(self.file_name, 'w') as f:
            f.wite(text)
    
    