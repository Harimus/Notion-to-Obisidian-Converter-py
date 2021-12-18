# Notion-to-Obisidian-Converter-py
Minima Notion export to Obsidian Converter written in Python. Inspired by similar code made in Node/JS [Notion-to-Obsidian-Converter](https://github.com/connertennery/Notion-to-Obsidian-Converter) It only uses Python3 standard libraries, so no install is required on Ubuntu 20.04. (or any platform with python3)

## Usage

1. Download Notion data from Notion>Settings & Members>Settings>Export content>Export all workspace content
2. Unzip the data 
3. Get the script
4. Download this repository, or only download the `main.py` file. The file only depend on python standard library, so if you have python3, you're good to go. 
4. Run `python3 main.py absolute/path/to/notion_data_folder/ /fixed/data/folder/`
5. Move the new folder to your Obisidan directory 

## How it works

**Paths:**

The script searches through every path and removes the long uuid at the end of both the directory paths and the file paths.

**Difference from Notion-to-Obsidian-converter**

-   Markdown links are **NOT** converted from the default `[Link Text](Notion\Link\Path)` to `[[Link Text]]`, it only removed the UUID. This because the original Markdown linking seems to work just fine in Obsidian.
-   CSV files are **deleted**.

## Why

## Note

This code first creates a copy of the downloaded notion data, and then work on that copy. Keep in mind that this means that it use some diskspace, and you'll end up with two folders. (original & processed)
