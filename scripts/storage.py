import os
import tempfile
import argparse
import sys
import json

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

parser = argparse.ArgumentParser()
parser.add_argument("--key")
parser.add_argument("--val")
args = parser.parse_args()
key = args.key
val = args.val

if val is None:
  with open(storage_path, 'r') as f:
    read_dict = json.load(f)
  val_list = read_dict.get(key, None)
  if val_list is None:
    print('value with key ' + key + ' not found')
  else:
    print(', '.join(val_list))
  sys.exit()

with open(storage_path, 'w') as f:
  if os.stat(storage_path).st_size == 0:
    write_dict = {}
  else:
    write_dict = json.load(f)
  if key in write_dict:
    write_dict[key].append(val)
  else:
    write_dict[key] = [val]
  json.dump(write_dict, f)