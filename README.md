# Notion-to-Obisidian-Converter-py
Minima Notion export to Obsidian Converter written in Python. Inspired by similar code made in Node/JS [Notion-to-Obsidian-Converter](https://github.com/connertennery/Notion-to-Obsidian-Converter) It only uses Python3 standard libraries, so no install is required on Ubuntu 20.04. (or any platform with python3)

## Usage

1. Download Notion data from Notion>Settings & Members>Settings>Export content>Export all workspace content
2. Unzip the data 
3. Download this repository, or only download the `main.py` file. The file only depend on python standard library, so if you have python3, you're good to go. 
4. Run `python3 main.py absolute/path/to/notion_data_folder/ /new/fixed/data/folder/`. This will create a new `folder` in `/new/fixed/data/`
5. Move the new folder to your Obisidan directory 

## How it works

### **Paths:**

The script searches through every path and removes the long uuid at the end of both the directory paths and the file paths.

### **Difference from Notion-to-Obsidian-converter**

-   Markdown links are **NOT** converted from the default `[Link Text](Notion\Link\Path)` to  Obsidian format `[[Link Text]]`, it only removed the UUID. This is because the original Markdown linking seems to work just fine in Obsidian, while Obsidian format is same yet seems like a silly lock-in to their format. Also path linking means pages/files with same name but different folder wont be confused.
-   CSV files are **replaced** with a markdown file with table. This is done naively and special characters might break things (most notably `|` in csv file)

## Limitations
-   Some internal links in notions are saved as `https://notion.so/1234566789`, and the last number is not tied to the uuid of the file, so we can't replace it with proper link. Some notion links contain page name, but right now this is not properly converted
-   Some pages from Notion with long page name, when saved to file gets its name shortened: A page called `Superlong_pagename_just_to_make_a_case_with_filler_characters` will be converted to `Superlong_pagename_just_to_make_a_cab9800f086ca541a4a1766bdbcf807bba.md`
**The cutoff length of a file seems to be 86 characters (including extension)**. This is not an issue for linking etc, but ends up looking tad bit ugly.

## Note

This code first creates a copy of the downloaded notion data, and then work on that copy. Keep in mind that this means that it use some diskspace, and you'll end up with two folders. (original & processed)

Trouble using it? Raise an issue on github!