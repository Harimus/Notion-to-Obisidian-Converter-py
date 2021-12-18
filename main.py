import os, sys, csv, shutil, re
from distutils.dir_util import copy_tree

UUID_count=32
MAX_filename_length=86 # Pages from Notion pages are often converted to shorter filenames

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

def csv_to_markdown_table(file_name: str):
  """In Notion, any Database page are saved as a Folder and CSV file with same name. 
  The Folder contains each page in database, and CSV contains the properties associated with it. 
  This function reads the csv, and return each row as dict, with keys as the first row (what each properties are called)."""
  assert '.csv' in file_name
  with open(file_name, newline='') as csvfile:
    csv_content = csv.reader(csvfile, delimiter=',', quotechar='"')
    first_row = next(csv_content)
    csv_list = []
    markdown_str = '|' + '|'.join(first_row) + '|\n'
    markdown_str = markdown_str + '|' + '|'.join(['---' for _ in range(len(first_row))]) + '|\n'
    for row in csv_content:
      row[0] = '[[' + row[0] + ']]' # assumes first element of .csv is Name, which is the filename
      markdown_str = markdown_str + '|' + '|'.join(row) + '|\n'
  return markdown_str

def csv_to_markdown_table_file(file_name: str, uuids: set):
  markdown_str = csv_to_markdown_table(file_name)
  file_uuid = get_uuid_from_filename(file_name)
  markdown_file = file_name.replace('.csv', '.md').replace(" " + file_uuid, '')
  for uuid in uuids:
    markdown_str =markdown_str.replace(r"%20"+uuid, '')
  with open(markdown_file, 'w') as f:
    f.write(markdown_str)


def remove_uuids_from_file(filename: str, uuids: set, replace_internal_links=False):
  regex_find = r"\[.*\]\((?!://)(.*)\)"
  regex_replace = r"[[\1]]"
  with open(filename, 'r') as f:
    content = f.read()
    for uuid in uuids:
      content = content.replace(r"%20"+uuid, '')
    if replace_internal_links: content = re.sub(regex_find, regex_replace, content)
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
      os.rename(full_path(file), full_path(file.replace(" "+file_uuid, '')))
    for csv_file in csv_filename:
      csv_to_markdown_table_file(full_path(csv_file), uuids)
      os.remove(full_path(csv_file))
    folder_uuid = get_uuid_from_filename(path)
    shutil.move(path, path.replace(" "+folder_uuid, ''))
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
