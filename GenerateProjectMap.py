#!/usr/bin/env python3

from os import listdir, path
from collections import namedtuple, OrderedDict

import xml.etree.ElementTree as ET
import xml.dom.minidom

class GitProject():
	def __init__(self, _path, _name, _readmeFileName, _remoteOrigin):
		self.path = _path
		self.name = _name
		self.readmeFileName = _readmeFileName
		self.remoteOrigin = _remoteOrigin

projects = OrderedDict()

def CheckDir(dir):
	bHasGitProject = False

	subdirs = []

	bIsGitProject = False
	readmeFileName = None
	bHasLicense = False
	for f in listdir(dir):
		filePath = path.join(dir, f)
		if path.isfile(filePath):
			if f.lower().startswith("readme"):
				readmeFileName = f
			if f == "LICENSE.txt":
				bHasLicense = True
		elif path.isdir(filePath):
			if f == ".git":
				bIsGitProject = True
			else:
				subdirs.append(filePath)

	if bIsGitProject:
		project = GitProject(dir.replace('/mnt/d/Code', 'D:\\Code', 1).replace('/', '\\'), path.basename(dir), readmeFileName, None)
		dirname = path.dirname(dir).replace('/mnt/d/Code', 'D:\\Code', 1).replace('/', '\\')
		if dirname in projects:
			projects[dirname].append(project)
		else:
			projects[dirname] = [project]
		bHasGitProject = True

		if readmeFileName == None:
			print("Warning: '" + dir + "' is a git project but has no readme!")
		if not bHasLicense:
			print("Warning: '" + dir + "' is a git project but has no license!")
	else:
		for subdir in subdirs:
			bHasGitProject = bHasGitProject | CheckDir(subdir)

	if not bHasGitProject:
		print("Warning: '" + dir + "' has no git projects under it!")

	return bHasGitProject

def OutputToConsole():
	for folderName, parentFolders in projects.items():
		print(folderName)
		print('=' * len(folderName))
		print('`')
		for i, project in enumerate(parentFolders):
			prefix = ' |-'
			print(prefix, project.name, project.readmeFileName)
		print()

def OutputXMLForSourceTree():
	root = ET.Element('ArrayOfTreeViewNode', {'xmlns:xsd': 'http://www.w3.org/2001/XMLSchema', 'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'})

	for folderName, parentFolders in projects.items():
		folder = ET.SubElement(root, 'TreeViewNode', {'xsi:type':'BookmarkFolderNode'})
		ele = ET.SubElement(folder, 'Level')
		ele.text = '0'
		ele = ET.SubElement(folder, 'IsExpanded')
		ele.text = 'false'
		ele = ET.SubElement(folder, 'IsLeaf')
		ele.text = 'false'
		ele = ET.SubElement(folder, 'Name')
		ele.text = path.basename(folderName)

		children = ET.SubElement(folder, 'Children')

		for project in parentFolders:
			repo = ET.SubElement(children, 'TreeViewNode', {'xsi:type':'BookmarkNode'})
			ele = ET.SubElement(repo, 'Level')
			ele.text = '1'
			ele = ET.SubElement(repo, 'IsExpanded')
			ele.text = 'false'
			ele = ET.SubElement(repo, 'IsLeaf')
			ele.text = 'true'
			ele = ET.SubElement(repo, 'Name')
			ele.text = project.name
			ele = ET.SubElement(repo, 'Children')
			ele = ET.SubElement(repo, 'CanSelect')
			ele.text = 'true'
			ele = ET.SubElement(repo, 'Path')
			ele.text = project.path
			ele = ET.SubElement(repo, 'RepoType')
			ele.text = 'Git'

		ele = ET.SubElement(folder, 'CanSelect')
		ele.text = 'true'

	tree = ET.ElementTree(root)

	xmlStr = ET.tostring(root, encoding='utf-8', method='xml')
	xmlStr = xml.dom.minidom.parseString(xmlStr).toprettyxml(indent='  ')
	with open("/mnt/c/Users/Riley/AppData/Local/Atlassian/SourceTree/bookmarks.xml", 'w') as f:
		f.write(xmlStr)

def main():
	CheckDir(r"/mnt/d/Code")
	print()
	print("===============")
	print()
	OutputToConsole()
	OutputXMLForSourceTree()

if __name__ == "__main__":
	main()
