class FileReader:
    
    def __init__(self, file_path):
        self._path = file_path
    
    def read(self):
        try:
            with open(self._path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return ''