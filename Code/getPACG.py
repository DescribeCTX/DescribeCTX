import os
import networkx as nx
import sys

import pdb

privacy = sys.argv[1] if len(sys.argv) > 1 else "sms"

# Sensitive API calls, refer to https://developer.android.com/reference/packages
sensitiveAPICall = {'calendar': ['startViewCalendarEventInManagedProfile()'],
					'camera': ['startPreview()', 'setFlashMode()', 'startRecording()', 'startCapture()'],
					'contact': ['getContact()','openContact()'],
					'location': ['getCurrentLocation()', 'getLastKnownLocation()', 'getLatitude()', 'getLongitude()', 'getProvider()', 'getAccuracy()', 'getAltitude()', 'getBearing()', 'getSpeed()'],
					'microphone': ['startRecording()', 'stop()'],
					'sms': ['getMessageBody()', 'receiveSmsMessage()'],
					'storage': ['getExternalStorageDirectory()', 'getDownloadCacheDirectory()', 'getRootDirectory()', 'getExternalStorageState()']}

sensitive_apis = sensitiveAPICall[privacy]

def create_subgraph(G, node): 
	edges = nx.dfs_predecessors(G, node) 
	nodes = [] 
	for k,v in edges.items(): 
		nodes.extend([k]) 
		nodes.extend(v) 
	print(nodes)
	return G.subgraph(nodes) 
# your app and call graph (.dot files) folder
apps = os.listdir(os.path.join('./activity_id_mapping', privacy))
dot_dir = os.path.join('./dot_output', privacy)
dot_files = os.listdir(dot_dir)
for app in apps:
	if (app == '.DS_Store'):
		continue
	if (os.path.exists('' + app) == True):
		print('exists')
		continue
	else:
		outPath = os.path.join('./cg', privacy)
		if not os.path.exists(outPath):
			os.makedirs(outPath)
		try:
			print(app)
			m2id = {}
			id2m = {}
			temp = open(dot_dir + '/' + app[:app.index('.txt')] + '/' + app[:app.index('.txt')] + '.dot', 'r')
			targets = []
			for line in temp:
				if 'label' not in line:
					continue
				line = line.strip('\n')
				m_id = line[2:line.index(' [')]
				m_name = line[line.index('"') + 1:line.rindex('"')]
				m2id[m_name] = m_id
				id2m[m_id] = m_name

			sensitive_apis_set = set(sensitive_apis)  
			targets = []
			for m_name in m2id:
				if any(api in m_name for api in sensitive_apis_set):
					targets.append(m_name)
			# breakpoint()

			
			G = nx.drawing.nx_pydot.read_dot(dot_dir + '/' + app[:app.index('.txt')] + '/' + app[:app.index('.txt')] + '.dot')
			# G = nx.Graph(read_dot(dot_dir + df))
			nodelist = list(G.nodes.data())
			#output file
			f2 = open('./cg/' + privacy + '/' + app, 'a')
			for m in targets:
				paths = nx.single_target_shortest_path(G, str(m2id[m]))
				path = {}
				for key in paths:
					temp = set(paths[key])
					if len(path) == 0:
						path[str(m2id[m])] = temp
					path[str(m2id[m])] = path[str(m2id[m])] | temp
				for i in path[str(m2id[m])]:
					f2.write(id2m[i] + '\t')
				f2.write('\n')
			# f.close()
			f2.close()
		except Exception as e:
			f = open('./cg/' + privacy + '/' + app, 'a')
			print(e)
			continue