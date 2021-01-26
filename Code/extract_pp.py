from rake_nltk import Rake
import stanfordnlp
import os
import nltk

from nltk.corpus import wordnet
import sys
# stanfordnlp.download('en')
# nlp = stanfordnlp.Pipeline()

# r = Rake()
FilePath = r"C:\Users\11497\Desktop\untitled\raw_pp"
dir_all = os.listdir(FilePath)
# count_rake = 0

def extract_nltk(file,file0,count_rake):
	print(file)
	sensitive_behavior = {'contact': ['address book', 'phone book','assign','ringtone','contacts'],
						  'microphone': ['microphone', 'record audio','voice','measure','speak','recognition'],
						  'location': ['location', 'gps','track','nearest','nearby','geographical location',' geo-location'],
						  'storage':['device storage','access external storage','download','external storage','save'],
						  # 'ReadPhoneState':['device id','read phone state','unique device identifier','device identifier','device identification code'],
						  # 'CallPhone':['call phone','phone call','phone calls'],
						  # 'ReadCallLog':['read call log','call log','call list','log data'],
						  'camera':['camera','take photo','take picture','record video', 'video recording'],
						  'calendar':['calendar access','event','calendar','reminder','calendar permission','access calendar','personal calendar','schedule'],
						  'SMS':['SMS',"send message",'text message']
						  }
	sensitive_permissions = {'contact': ['android.permission.READ_CONTACTS', 'android.permission.WRITE_CONTACTS'],
							 'microphone': ['android.permission.RECORD_AUDIO'],
							 'location': ['android.permission.ACCESS_FINE_LOCATION', 'android.permission.ACCESS_COARSE_LOCATION'],
							 'storage':['android.permission.READ_EXTERNAL_STORAGE','android.permission.WRITE_EXTERNAL_STORAGE'],
							 # 'read phone state':['android.permission.READ_PHONE_STATE'],
							 # 'CallPhone': ['CALL_PHONE','android.permission.CALL_PHONE'],
							 # 'ReadCallLog': ['READ_CALL_LOG', 'android.permission.READ_CALL_LOG'],
							 'camera':['android.permission.CAMERA'],
							 'calendar':['android.permission.READ_CALENDAR','android.permission.WRITE_CALENDAR'],
							 'SMS':['android.permission.READ_SMS','android.permission.SEND_SMS','android.permission.RECEIVE_SMS']
							 }
	sensitive_description = {'contact': [], 'microphone': [], 'location': [], 'storage':[],
							 # 'ReadPhoneState':[],'CallPhone':[],'ReadCallLog':[],
							 'camera':[], 'calendar':[],'SMS':[]}
	f = open(file,'rb')
	texts = []
	for line in f.readlines():
		line = line.decode().strip('\n').split('.')
		for temp in line:
			if temp == '':
				continue
			texts.append(temp)


	for text in texts:
		for key in sensitive_permissions:
			for permission in sensitive_permissions[key]:
				if permission in text:
					sensitive_description[key].append(text.lower())
		for key in sensitive_behavior:
			for behavior in sensitive_behavior[key]:
				if behavior in text:
					sensitive_description[key].append(text.lower())
		# text = text.lower()
		# r.extract_keywords_from_text(text)
		# key_words = r.get_ranked_phrases_with_scores()
		# for word in key_words:
			# if 'contact' in word[1]:
			# 	stan = nlp(word[1])
			# 	for s in stan.sentences:
			# 		for w in s.words:
			# 			if 'contact' not in w.text:
			# 				continue
			# 			if w.upos == 'NOUN':
			# 				if text not in sensitive_description['contact']:
			# 					sensitive_description['contact'].append(text)
			# if 'calendar' in word[1]:
			# 	if text not in sensitive_description['calendar']:
			# 		count_rake += 1
			# 		sensitive_description['calendar'].append(text)
			# if 'camera' in word[1]:
			# 	if text not in sensitive_description['camera']:
			# 		count_rake += 1
			# 		sensitive_description['camera'].append(text)
			# if 'contact' in word[1]:
			# 	if text not in sensitive_description['contact']:
			# 		count_rake += 1
			# 		sensitive_description['contact'].append(text)
			# if 'location' in word[1]:
			# 	if text not in sensitive_description['location']:
			# 		count_rake += 1
			# 		sensitive_description['location'].append(text)
			# if 'microphone' in word[1]:
			# 	if text not in sensitive_description['microphone']:
			# 		count_rake += 1
			# 		sensitive_description['microphone'].append(text)
			# if 'SMS' in word[1]:
			# 	if text not in sensitive_description['SMS']:
			# 		count_rake += 1
			# 		sensitive_description['SMS'].append(text)
			# if 'storage' in word[1]:
			# 	if text not in sensitive_description['storage']:
			# 		count_rake += 1
			# 		sensitive_description['storage'].append(text)
			# if 'read phone state' in word[1]:
			# 	if text not in sensitive_description['ReadPhoneState']:
			# 		sensitive_description['ReadPhoneState'].append(text)
			# if 'CallPhone' in word[1]:
			# 	if text not in sensitive_description['CallPhone']:
			# 		sensitive_description['CallPhone'].append(text)
			# if 'ReadCallLog' in word[1]:
			# 	if text not in sensitive_description['ReadCallLog']:
			# 		sensitive_description['ReadCallLog'].append(text)

# Output permission descriptions by category
	sen = "storage"
	temp = set(sensitive_description[sen])
	flag = 0
	for sent in temp:
		if len(sent)!=0:
			print(sent)
			flag = 1
		#print(sent2id[sent])
	if flag == 1:
		file = FilePath.replace('raw','extract')+"\\"+sen+"\\"+file0
		print(file)
		fw = open(file,'w',encoding='utf-8')
		for sent in temp:
			# if "contact information" in sent:
			fw.write(sent)

for file in dir_all:
	try:
		extract_nltk(FilePath+"\\"+file,file,count_rake)
	except:
		print("***Extract file failed!")