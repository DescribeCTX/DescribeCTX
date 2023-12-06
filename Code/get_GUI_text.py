import os
import shutil
import xml.etree.ElementTree as ET

import sys


def parse_xml(root, id_list, text_list):
	children = root.getchildren()
	if len(children) == 0:
		return
	else:
		for child in children:
			attribs = child.attrib
			for key in attribs.keys():
				if '}text' in key:
					if key.rindex('text') == len(key) - 4:
						if attribs[key] not in text_list:
							text_list.append(attribs[key])
				if '}src' in key:
					if key.rindex('src') == len(key) - 3:
						if attribs[key] not in id_list:
							id_list.append(attribs[key])
			parse_xml(child,id_list,text_list)



privacy = sys.argv[1] if len(sys.argv) > 1 else "sms"

def main(dir):
	apps = os.listdir(dir)
	for app in apps:
		if (app == '.DS_Store'):
			continue
		print(app)
		# os.mkdir('./UI_Context/Contacts/' + app[:app.index('.txt')] + '/')
		f = open('./activity_layout_mapping/' + privacy + '/' + app, 'r')
		app_activities_layouts = {}
		app_activities = []
		for line in f.readlines():
			line = line.strip('\n').split('\t')
			app_activities_layouts[line[0]] = line[1]
			app_activities.append(line[0])
		f.close()

		if len(app_activities_layouts) == 0:
			continue
		else:
			apk_context_text = []
			for activity in app_activities_layouts.keys():
				layout = app_activities_layouts[activity]
				apk_res_dir = './apktool_output/'
				apk_name = app[:app.index('.txt')]
				activity_xml = apk_res_dir + privacy + '/' + apk_name + '/res/layout/' + layout + '.xml'

				try:
					tree = ET.parse(activity_xml)
				except Exception as e:
					continue
				apkdata_text = []
				apkdata_id = []
				parse_xml(tree.getroot(), apkdata_id, apkdata_text)
				for text in apkdata_text:
					if '@string' in text:
						string_id = text[text.index('/') + 1:]
						f_string = open(apk_res_dir + privacy + '/' + apk_name + '/res/values/strings.xml', 'r')
						for line in f_string.readlines():
							if string_id not in line:
								continue
							try:
								string_value = str(line)[str(line).index('>') + 1:str(line).index('</')]
								apk_context_text.append(string_value)
							except Exception as e:
								print("An exception occurred: ", str(e))
								# import pdb; pdb.set_trace()
								continue
					else:
						apk_context_text.append(text)
			
			outPath = os.path.join('./GUI', privacy)
			if not os.path.exists(outPath):
				os.makedirs(outPath)

			f_out = open(outPath + '/' + app, 'w')
			for text in apk_context_text:
				f_out.write(text + ' ')
			f_out.close()

			


if __name__ == 	"__main__":
	app_dir = os.path.join('./activity_layout_mapping/', privacy)
	main(app_dir)
