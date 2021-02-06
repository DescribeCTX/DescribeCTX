import os
import shutil
import codecs
import binascii
import sys

resourcedir = '/Users/shaoyang/Desktop/API_exp/apktool_output/2/'
mappingdir = '/Users/shaoyang/Desktop/API_exp/activity_id_mapping/2/'
# apps = os.listdir(resourcedir)
mappings = os.listdir(mappingdir)
# for app in apps:
# 	if app == '.DS_Store':
# 		continue
# 	app_res = os.listdir(resourcedir + app + '/')
# 	for res in app_res:
# 		if res != 'res':
# 			if os.path.isdir(resourcedir + app + '/' + res + '/'):
# 				shutil.rmtree(resourcedir + app + '/' + res)
# 			else:
# 				os.remove(resourcedir + app + '/' + res)
# 		else:
# 			all_res = os.listdir(resourcedir + app + '/' + res + '/')
# 			for res_folder in all_res:
# 				if res_folder == 'layout':
# 					continue
# 				elif res_folder == 'values':
# 					continue
# 				else:
# 					shutil.rmtree(resourcedir + app + '/' + res + '/' + res_folder)

for app in mappings:
	if app == '.DS_Store':
		continue
	try:
		app = app[:app.index('.txt')]
		layout_id_mapping = {}
		layout_activity_mapping = {}
		print('Create mapping for ' + app)
		app_layout_id_mapping = resourcedir + app + '.apk/res/values/public.xml'
		f = open(app_layout_id_mapping, 'r')
		for line in f.readlines():
			if ('public type=\"layout\"') in line:
				layout_id_hex = str(line)[str(line).index('id=') + 4:str(line).index('/>') - 2]
				layout_name = str(line)[str(line).index('name=') + 6:str(line).index(' id=') - 1]
				layout_id_int = int(layout_id_hex, 16)
				layout_id_mapping[str(layout_id_int)] = layout_name
		f.close()
		f1 = open(mappingdir + app + '.txt', 'r')
		for line in f1.readlines():
			line = line.strip('\n').split('\t')
			if line[1] in layout_id_mapping.keys():
				layout_name = layout_id_mapping[line[1]]
				activity_name = line[0]
				layout_activity_mapping[activity_name] = layout_name
		f1.close()
		f2 = open('./activity_layout_mapping/2/' + app + '.txt', 'w')
		for key in layout_activity_mapping.keys():
			f2.write(key + '\t' + layout_activity_mapping[key] + '\n')
		f2.close()
	except Exception as e:
		f2 = open('./activity_layout_mapping/2/' + app + '.txt', 'w')
		f2.write('')
		continue

