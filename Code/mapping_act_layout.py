import os
import shutil
import codecs
import binascii
import sys
import traceback

privacy = sys.argv[1] if len(sys.argv) > 1 else "sms"

resourcedir = os.path.join('./apktool_output/', privacy)
mappingdir = os.path.join('./activity_id_mapping/', privacy)
mappings = os.listdir(mappingdir)


for app in mappings:
	if app == '.DS_Store':
		continue
	try:
		app = app[:app.index('.txt')]
		layout_id_mapping = {}
		layout_activity_mapping = {}
		print('Create mapping for ' + app)
		app_layout_id_mapping = resourcedir + '/' + app + '/res/values/public.xml'

		f = open(app_layout_id_mapping, 'r')
		for line in f.readlines():
			if ('public type=\"layout\"') in line:
				layout_id_hex = str(line)[str(line).index('id=') + 4:str(line).index('/>') - 2]
				layout_name = str(line)[str(line).index('name=') + 6:str(line).index(' id=') - 1]
				layout_id_int = int(layout_id_hex, 16)
				layout_id_mapping[str(layout_id_int)] = layout_name
		f.close()
		f1 = open(mappingdir + '/' + app + '.txt', 'r')
		for line in f1.readlines():
			line = line.strip('\n').split('\t')
			if line[1] in layout_id_mapping.keys():
				layout_name = layout_id_mapping[line[1]]
				activity_name = line[0]
				layout_activity_mapping[activity_name] = layout_name
		f1.close()

		outPath = os.path.join('./activity_layout_mapping', privacy)
		if not os.path.exists(outPath):
			os.makedirs(outPath)

		f2 = open('./activity_layout_mapping/' + privacy + '/' + app + '.txt', 'w')
		for key in layout_activity_mapping.keys():
			f2.write(key + '\t' + layout_activity_mapping[key] + '\n')
		f2.close()
	except Exception as e:
		print("An exception occurred: ", str(e))
		# print(traceback.format_exc())
		outPath = os.path.join('./activity_layout_mapping', privacy)
		if not os.path.exists(outPath):
			os.makedirs(outPath)

		f2 = open('./activity_layout_mapping/' + privacy + '/' + app + '.txt', 'w')
		f2.write('')
		f2.close()
		continue

