# %%
import os.path
import tempfile

class File:
    def __init__(self, file_name):
        self.file_name = file_name
        if not os.path.exists(self.path):
            f = open(file_name, 'w').close()

    def __str__(self):
        return self.file_name
        
    def __add__(self, obj):
        new_text = self.read() + obj.read()
        new_path = os.path.join(
            tempfile.gettempdir(),
            next(tempfile._get_candidate_names())
        )
        new_obj = File(new_path)
        new_obj.write(new_text)
        return new_obj
    
    def __iter__(self):
        self.cursor = 0
        return self
    
    def __next__(self):
        with open(self.file_name) as f:
            f.seek(self.cursor)
            line = f.readline()
            if not line:
                raise StopIteration
            self.cursor = f.tell()
        return line

    def read(self):
        with open(self.file_name, 'r') as f:
            return f.read()
    
    def write(self, text):
        with open(self.file_name, 'w') as f:
            return f.write(text)
    
# %%
"""
directory = '/mnt/c/Users/atkal/my_projects/python_intermediate/file_handler/'
path_to_file = directory + 'test'
print(os.path.exists(path_to_file))
file_obj = File(path_to_file)
print(os.path.exists(path_to_file))

print(file_obj.read())

file_obj.write('some text')
print(file_obj.read())

file_obj.write('other text')
print(file_obj.read())

file_obj_1 = File(path_to_file + '_1')
file_obj_2 = File(path_to_file + '_2')
file_obj_1.write('line 1\n')
file_obj_2.write('line 2\n')
new_file_obj = file_obj_1 + file_obj_2
print(isinstance(new_file_obj, File))
print(new_file_obj)
print(new_file_obj.read())

for line in new_file_obj:
    print(ascii(line))"""