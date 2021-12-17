import os, sys, csv, shutil
from posixpath import abspath
from collections import OrderedDict
from distutils.dir_util import copy_tree

UUID_count=32
def process_notion(notion_folder: str):
  raise NotImplemented

def get_uuid_from_filename(file_name: str):
  raw_file_name = os.path.basename(file_name.split('.')[0]) #Folder (no .) works too
  if len(raw_file_name) > UUID_count:
    return raw_file_name[-UUID_count:]
  else:
    return ''

def get_all_uuid(root_folder: str):
  uuids = set()
  valid_files = ['.md', '.csv']
  for path, dirs, files in os.walk(root_folder):
    for file in files:
      if any([ vf in file for vf in valid_files]):
        file_uuid = get_uuid_from_filename(file)
        if file_uuid: uuids.add(file_uuid)
    path_uuid = get_uuid_from_filename(path) 
    if path_uuid: uuids.add(path_uuid)

  return uuids

def csv_to_list_dict(file_name: str):
  """In Notion, any Database page are saved as a Folder and CSV file with same name. 
  The Folder contains each page in database, and CSV contains the properties associated with it. 
  This function reads the csv, and return each row as dict, with keys as the first row (what each properties are called)."""
  assert '.csv' in file_name
  with open(file_name, newline='') as csvfile:
    csv_content = csv.reader(csvfile, delimiter=',', quotechar='"')
  first_row = next(csv_content)
  csv_list = []
  for row in csv_content:
    csv_dict = {key: '' for key in first_row}
    for key, value in zip(first_row, row):
      csv_dict[key] = value
    csv_list.append(csv_dict)
  return csv_list

def add_property_to_file(filename: str, property_dict: dict):
  """Prepend the content of dict (properties) on top of a File."""
  file_uuid = get_uuid_from_filename(filename)
  with open(filename, 'r') as f:
    content = f.read()
  str_property = '\n'.join([f"{key}: {value}" for key, value in property_dict.keys()])
  with open(filename, 'w') as f:
    f.write(str_property + '\n' + content)

def remove_uuids_from_file(filename, uuids):
  with open(filename, 'r') as f:
    content = f.read()
    for uuid in uuids:
      content = content.replace(uuid, '')
  with open(filename, 'w') as f:
    f.write(content)

def process_folder(folder: str, uuids: set):
  """Recursive function that process all files/subdirectories from given folder name.
  Depth first recursion, and changes the file/folder name by removing the uuid."""
  try:
    path, dirs, files = next(os.walk(folder))
    full_path = lambda x: os.path.join(path, x)
    print(f"Processing folder: {path} ")
    folder_name = os.path.basename(path)
    csv_filename = [f for f in files if '.csv' in f]
    for dir in dirs:
      process_folder(full_path(dir), uuids)
    md_files = [f for f in files if '.md' in f] # Only process markdown files. leaves png etc alone
    for file in md_files:
      file_uuid = get_uuid_from_filename(file)
      remove_uuids_from_file(full_path(file), uuids)
      os.rename(full_path(file), full_path(file.replace(file_uuid, '')))
    for csv_file in csv_filename:
      os.remove(full_path(csv_file))
    folder_uuid = get_uuid_from_filename(path)
    shutil.move(path, path.replace(folder_uuid, ''))
  except StopIteration:
    pass

if __name__ == '__main__':
  target_folder = './Notion_to_Obsidian/'
  if len(sys.argv) < 3:
    print(f"Error: Usage ")
    raise ValueError(f"Usage: python3 main.py /absolute/path/to/extracted/Notion_folder/ /absolute/path/to/save/new/folder")
  root_folder = sys.argv[1]
  target_folder =  sys.argv[2]
  copy_tree(root_folder, target_folder)
  all_uuids = get_all_uuid(target_folder)
  process_folder(target_folder, all_uuids)
  #notion_folder = sys.argv[1]
