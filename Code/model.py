import numpy as np  

import pandas as pd 
import re
from bs4 import BeautifulSoup 
from keras.preprocessing.text import Tokenizer 
from keras.preprocessing.sequence import pad_sequences
from keras.optimizers import Adam
from nltk.corpus import stopwords   
from tensorflow.keras.layers import Input, LSTM, Embedding, Dense, Concatenate, TimeDistributed, Bidirectional, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import Attention
import tensorflow as tf
from sklearn.model_selection import train_test_split
from attention import AttentionLayer, CoAttentionPara
import keras.backend as K
from numpy import array
from numpy import asarray
from numpy import zeros

data=pd.read_csv('./data1.csv',nrows = 1557, encoding= 'unicode_escape')
data['des'] = data['des'].apply(lambda x : '_START_ '+ x + ' _END_')

embeddings_dictionary = dict()

glove_file = open('./glove.6B.100d.txt', encoding = 'utf8')

for line in glove_file:
	records = line.split()
	word = records[0]
	vector_dimensions = asarray(records[1:], dtype='float32')
	embeddings_dictionary[word] = vector_dimensions
glove_file.close()

max_len_pp = 50
max_len_ui = 50
max_len_cg = 50
max_len_des = 50
dim = 256

x_pp_tr,x_pp_val,x_ui_tr,x_ui_val,x_cg_tr,x_cg_val,y_tr,y_val=train_test_split(data['pp'],data['ui'],data['cg'],data['des'],test_size=0.1,random_state=0,shuffle=True)
tokenizer = Tokenizer()
tokenizer.fit_on_texts(list(x_pp_tr) + list(x_pp_val) + list(x_ui_tr) + list(x_ui_val) + list(x_cg_tr) + list(x_cg_val) + list(y_tr) + list(y_val))


x_pp_tr = tokenizer.texts_to_sequences(x_pp_tr)
x_ui_tr = tokenizer.texts_to_sequences(x_ui_tr) 
x_cg_tr = tokenizer.texts_to_sequences(x_cg_tr) 
x_pp_val = tokenizer.texts_to_sequences(x_pp_val)
x_ui_val = tokenizer.texts_to_sequences(x_ui_val)
x_cg_val = tokenizer.texts_to_sequences(x_cg_val)

x_pp_tr = pad_sequences(x_pp_tr,  maxlen = max_len_pp, padding='post')
x_ui_tr = pad_sequences(x_ui_tr,  maxlen = max_len_ui, padding='post')
x_cg_tr = pad_sequences(x_cg_tr,  maxlen = max_len_cg, padding='post')
x_pp_val = pad_sequences(x_pp_val, maxlen = max_len_pp, padding='post')
x_ui_val = pad_sequences(x_ui_val, maxlen = max_len_ui, padding='post')
x_cg_val = pad_sequences(x_cg_val, maxlen = max_len_cg, padding='post')

x_voc_size = len(tokenizer.word_index) +1
print(x_voc_size)

# y_tokenizer = Tokenizer()
# tokenizer.fit_on_texts(list(y_tr))

#convert summary sequences into integer sequences
y_tr = tokenizer.texts_to_sequences(y_tr) 
y_val = tokenizer.texts_to_sequences(y_val) 

#padding zero upto maximum length
y_tr =  pad_sequences(y_tr, maxlen = max_len_des, padding='post')
y_val = pad_sequences(y_val, maxlen = max_len_des, padding='post')

y_voc_size = len(tokenizer.word_index) +1
print(y_voc_size)

embedding_matrix = zeros((x_voc_size, 100))
for word, index in tokenizer.word_index.items():
	embedding_vector = embeddings_dictionary.get(word)
	if embedding_vector is not None:
		embedding_matrix[index] = embedding_vector

encoder_pp_inputs = Input(shape=(max_len_pp,), dtype=K.floatx())
encoder_ui_inputs = Input(shape=(max_len_ui,), dtype=K.floatx()) 
encoder_cg_inputs = Input(shape=(max_len_cg,), dtype=K.floatx()) 
encoder_pp_emb = Embedding(x_voc_size, 100, weights = [embedding_matrix])(encoder_pp_inputs)
encoder_ui_emb = Embedding(x_voc_size, 100, weights = [embedding_matrix])(encoder_ui_inputs)
encoder_cg_emb = Embedding(x_voc_size, 100, weights = [embedding_matrix])(encoder_cg_inputs)
# encoder_pp_in, _, _, _, _ = Bidirectional(LSTM(dim, return_sequences = True, return_state = True))(encoder_pp_emb)
# encoder_ui_in = Bidirectional(LSTM(dim, return_sequences = True, return_state = True))(encoder_ui_emb)
# encoder_cg_in = Bidirectional(LSTM(dim, return_sequences = True, return_state = True))(encoder_cg_emb)
encoder_pp_in, _, _, _, _ = Bidirectional(LSTM(dim, return_sequences = True, return_state = True))(encoder_pp_emb)
encoder_ui_in, _, _, _, _ = Bidirectional(LSTM(dim, return_sequences = True, return_state = True))(encoder_ui_emb)
encoder_cg_in, _, _, _, _ = Bidirectional(LSTM(dim, return_sequences = True, return_state = True))(encoder_cg_emb)

encoder_ui_in, encoder_cg_in = CoAttentionPara(dim_k = 100, name="feature")([encoder_ui_in, encoder_cg_in])
encoder_in = Concatenate()([encoder_pp_in, encoder_ui_in, encoder_cg_in])

encoder_lstm1 = Bidirectional(LSTM(dim,return_sequences=True,return_state=True, dropout = 0.2, recurrent_dropout = 0.2, kernel_regularizer = tf.keras.regularizers.l2(l = 0.0001)))
encoder_outputs, forward_h1, forward_c1, backward_h1, backward_c1 = encoder_lstm1(encoder_in)
state_h = Concatenate()([forward_h1, backward_h1])
state_c = Concatenate()([forward_c1, backward_c1])

# Set up the decoder. 
decoder_inputs = Input(shape=(None,), dtype=K.floatx()) 
dec_emb_layer = Embedding(y_voc_size, 100)
dec_emb = dec_emb_layer(decoder_inputs) 

#LSTM using encoder_states as initial state
decoder_lstm = LSTM(dim * 2, return_sequences=True, return_state = True)
decoder_outputs, decoder_fwd_state, decoder_back_state = decoder_lstm(dec_emb, initial_state = [state_h, state_c]) 

#Attention Layer
attn_layer = AttentionLayer(name='attention_layer') 
attn_out, attn_states = attn_layer([encoder_outputs, decoder_outputs])

# Concat attention output and decoder LSTM output 
decoder_concat_input = Concatenate(axis=-1, name='concat_layer')([decoder_outputs, attn_out])

#Dense layer
decoder_dense = TimeDistributed(Dense(y_voc_size, activation='softmax', kernel_regularizer = tf.keras.regularizers.l2(l = 0.001))) 
decoder_outputs = decoder_dense(decoder_concat_input) 

# Define the model
model = Model([encoder_pp_inputs, encoder_ui_inputs, encoder_cg_inputs, decoder_inputs], decoder_outputs)
model.summary()

model.compile(optimizer='rmsprop', loss='sparse_categorical_crossentropy')
output_model_file = './model2/checkpoint-{epoch:02d}e-val_loss_{val_loss:.2f}.hdf5'
checkpoint = ModelCheckpoint(output_model_file, monitor='val_loss', verbose=1, save_best_only=True)
# es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)
history = model.fit([x_pp_tr, x_ui_tr, x_cg_tr, y_tr[:,:-1]], y_tr.reshape(y_tr.shape[0],y_tr.shape[1], 1)[:,1:], epochs = 50, callbacks = [checkpoint], batch_size = 64, validation_data = ([x_pp_val, x_ui_val, x_cg_val, y_val[:,:-1]],y_val.reshape(y_val.shape[0],y_val.shape[1], 1)[:,1:]))

reverse_target_word_index = tokenizer.index_word 
reverse_source_word_index = tokenizer.index_word 
target_word_index = tokenizer.word_index

encoder_model = Model(inputs=[encoder_pp_inputs, encoder_ui_inputs, encoder_cg_inputs],outputs=[encoder_outputs, state_h, state_c])

# decoder inference
# Below tensors will hold the states of the previous time step
decoder_state_input_h = Input(shape=(dim * 2,))
decoder_state_input_c = Input(shape=(dim * 2,))
decoder_hidden_state_input = Input(shape=(None, dim * 2))

# Get the embeddings of the decoder sequence
dec_emb2= dec_emb_layer(decoder_inputs)

# To predict the next word in the sequence, set the initial states to the states from the previous time step
decoder_outputs2, state_h2, state_c2 = decoder_lstm(dec_emb2, initial_state=[decoder_state_input_h, decoder_state_input_c])

#attention inference
attn_out_inf, attn_states_inf = attn_layer([decoder_hidden_state_input, decoder_outputs2])
decoder_inf_concat = Concatenate(axis=-1, name='concat')([decoder_outputs2, attn_out_inf])

# A dense softmax layer to generate prob dist. over the target vocabulary
decoder_outputs2 = decoder_dense(decoder_inf_concat)

# Final decoder model
decoder_model = Model(
[decoder_inputs] + [decoder_hidden_state_input,decoder_state_input_h, decoder_state_input_c],
[decoder_outputs2] + [state_h2, state_c2])

def decode_sequence(pp,ui,cg):
	# Encode the input as state vectors.
	e_out, e_h, e_c = encoder_model.predict([pp,ui,cg])

	# Generate empty target sequence of length 1.
	target_seq = np.zeros((1,1))

	# Chose the 'start' word as the first word of the target sequence
	target_seq[0, 0] = target_word_index['start']

	stop_condition = False
	decoded_sentence = ''
	while not stop_condition:
		output_tokens, h, c = decoder_model.predict([target_seq] + [e_out, e_h, e_c])

		# Sample a token
		sampled_token_index = np.argmax(output_tokens[0, -1, :])
		sampled_token = reverse_target_word_index[sampled_token_index]

		if(sampled_token!='end'):
			decoded_sentence += ' '+sampled_token

		# Exit condition: either hit max length or find stop word.
		if (sampled_token == 'end' or len(decoded_sentence.split()) >= (max_len_des-1)):
			stop_condition = True

		# Update the target sequence (of length 1).
		target_seq = np.zeros((1,1))
		target_seq[0, 0] = sampled_token_index

		# Update internal states
		e_h, e_c = h, c

	return decoded_sentence

def seq2summary(input_seq):
	newString=''
	for i in input_seq:
		if((i!=0 and i!=target_word_index['start']) and i!=target_word_index['end']):
			newString=newString+reverse_target_word_index[i]+' '
	return newString

def seq2text(input_seq):
	newString=''
	for i in input_seq:
		if(i!=0):
			newString=newString+reverse_source_word_index[i]+' '
	return newString


for i in range(len(x_pp_val)):
	print("Review:",seq2text(x_pp_val[i]))
	print("Reference Sentence:",seq2summary(y_val[i]))
	print("Synthesized Description:",decode_sequence(x_pp_val[i].reshape(1,max_len_pp), x_ui_val[i].reshape(1,max_len_ui), x_cg_val[i].reshape(1,max_len_cg)))
	print('\n')
