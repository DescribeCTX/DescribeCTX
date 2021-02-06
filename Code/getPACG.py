import os
import networkx as nx

def create_subgraph(G, node): 
	edges = nx.dfs_predecessors(G, node) 
	nodes = [] 
	for k,v in edges.items(): 
		nodes.extend([k]) 
		nodes.extend(v) 
	print(nodes)
	return G.subgraph(nodes) 
# your app and call graph (.dot files) folder
apps = os.listdir('./Descriptions/Contacts/')
dot_dir = './APKCallGraph/dot_output/'
dot_files = os.listdir(dot_dir)
for app in apps:
	if (app == '.DS_Store'):
		continue
	if (os.path.exists('' + app) == True):
		print('exists')
		continue
	else:
		try:
			print(app)
			m2id = {}
			id2m = {}
			temp = open(dot_dir + app[:app.index('.txt')] + '/' + app[:app.index('.txt')] + '.dot', 'r')
			targets = []
			for line in temp.readlines():
				if 'label' not in line:
					continue
				line = line.strip('\n')
				m_id = line[2:line.index(' [')]
				m_name = line[line.index('"') + 1:line.rindex('"')]
				m2id[m_name] = m_id
				id2m[m_id] = m_name
				if 'enter sensitive API here' in m_name:
					targets.append(m_name)
			temp.close()
			G = nx.drawing.nx_pydot.read_dot(dot_dir + app[:app.index('.txt')] + '/' + app[:app.index('.txt')] + '.dot')
			# G = nx.Graph(read_dot(dot_dir + df))
			nodelist = list(G.nodes.data())
			#output file
			f2 = open('./cg/Contacts/' + app, 'w')
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
			f = open('./cg/Contacts/' + app, 'w')
			continue