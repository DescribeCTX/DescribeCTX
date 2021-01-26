import tensorflow as tf
import os
from tensorflow.python.keras.layers import Layer, InputSpec
from tensorflow.python.keras import backend as K


class AttentionLayer(Layer):
    """
    This class implements Bahdanau attention (https://arxiv.org/pdf/1409.0473.pdf).
    There are three sets of weights introduced W_a, U_a, and V_a
     """

    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        assert isinstance(input_shape, list)
        # Create a trainable weight variable for this layer.

        self.W_a = self.add_weight(name='W_a',
                                   shape=tf.TensorShape((input_shape[0][2], input_shape[0][2])),
                                   initializer='glorot_uniform',
                                   trainable=True)
        self.U_a = self.add_weight(name='U_a',
                                   shape=tf.TensorShape((input_shape[1][2], input_shape[0][2])),
                                   initializer='glorot_uniform',
                                   trainable=True)
        self.V_a = self.add_weight(name='V_a',
                                   shape=tf.TensorShape((input_shape[0][2], 1)),
                                   initializer='glorot_uniform',
                                   trainable=True)

        super(AttentionLayer, self).build(input_shape)  # Be sure to call this at the end

    def call(self, inputs, verbose=False):
        """
        inputs: [encoder_output_sequence, decoder_output_sequence]
        """
        assert type(inputs) == list
        encoder_out_seq, decoder_out_seq = inputs
        if verbose:
            print('encoder_out_seq>', encoder_out_seq.shape)
            print('decoder_out_seq>', decoder_out_seq.shape)

        def energy_step(inputs, states):
            """ Step function for computing energy for a single decoder state
            inputs: (batchsize * 1 * de_in_dim)
            states: (batchsize * 1 * de_latent_dim)
            """

            assert_msg = "States must be an iterable. Got {} of type {}".format(states, type(states))
            assert isinstance(states, list) or isinstance(states, tuple), assert_msg

            """ Some parameters required for shaping tensors"""
            en_seq_len, en_hidden = encoder_out_seq.shape[1], encoder_out_seq.shape[2]
            de_hidden = inputs.shape[-1]

            """ Computing S.Wa where S=[s0, s1, ..., si]"""
            # <= batch size * en_seq_len * latent_dim
            W_a_dot_s = K.dot(encoder_out_seq, self.W_a)

            """ Computing hj.Ua """
            U_a_dot_h = K.expand_dims(K.dot(inputs, self.U_a), 1)  # <= batch_size, 1, latent_dim
            if verbose:
                print('Ua.h>', U_a_dot_h.shape)

            """ tanh(S.Wa + hj.Ua) """
            # <= batch_size*en_seq_len, latent_dim
            Ws_plus_Uh = K.tanh(W_a_dot_s + U_a_dot_h)
            if verbose:
                print('Ws+Uh>', Ws_plus_Uh.shape)

            """ softmax(va.tanh(S.Wa + hj.Ua)) """
            # <= batch_size, en_seq_len
            e_i = K.squeeze(K.dot(Ws_plus_Uh, self.V_a), axis=-1)
            # <= batch_size, en_seq_len
            e_i = K.softmax(e_i)

            if verbose:
                print('ei>', e_i.shape)

            return e_i, [e_i]

        def context_step(inputs, states):
            """ Step function for computing ci using ei """

            assert_msg = "States must be an iterable. Got {} of type {}".format(states, type(states))
            assert isinstance(states, list) or isinstance(states, tuple), assert_msg

            # <= batch_size, hidden_size
            c_i = K.sum(encoder_out_seq * K.expand_dims(inputs, -1), axis=1)
            if verbose:
                print('ci>', c_i.shape)
            return c_i, [c_i]

        fake_state_c = K.sum(encoder_out_seq, axis=1)
        fake_state_e = K.sum(encoder_out_seq, axis=2)  # <= (batch_size, enc_seq_len, latent_dim

        """ Computing energy outputs """
        # e_outputs => (batch_size, de_seq_len, en_seq_len)
        last_out, e_outputs, _ = K.rnn(
            energy_step, decoder_out_seq, [fake_state_e],
        )

        """ Computing context vectors """
        last_out, c_outputs, _ = K.rnn(
            context_step, e_outputs, [fake_state_c],
        )

        return c_outputs, e_outputs

    def compute_output_shape(self, input_shape):
        """ Outputs produced by the layer """
        return [
            tf.TensorShape((input_shape[1][0], input_shape[1][1], input_shape[1][2])),
            tf.TensorShape((input_shape[1][0], input_shape[1][1], input_shape[0][1]))
        ]

class CoAttentionPara(Layer):
    """
    self-defined parallel co-attention layer.
    inputs: [tFeature, iFeature]
    outputs: [coFeature]
    dimension:
    input dimensions: [(batch_size, seq_length, embedding_size), (batch_size, num_img_region, 2*hidden_size)]
        considering subsequent operation, better to set embedding_size == 2*hidden_size
    output dimensions:[(batch_size, 2*hidden_size)]
    """
    def __init__(self, dim_k, **kwargs):
        super(CoAttentionPara, self).__init__(**kwargs)
        self.dim_k = dim_k  # internal tensor dimension
        self.supports_masking = True

    def build(self, input_shape):
        if not isinstance(input_shape, list):
            raise ValueError('A Co-Attention_para layer should be called '
                             'on a list of inputs.')
        if len(input_shape) != 2:
            raise ValueError('A Co-Attention_para layer should be called on a list of 2 inputs.'
                             'Got '+str(len(input_shape))+'inputs.')
        self.embedding_size = input_shape[0][-1]
        self.num_region = input_shape[1][1]
        self.seq_len = input_shape[0][1]
        """
        naming variables following the VQA paper
        """
        self.Wb = self.add_weight(name="Wb",
                                  initializer="random_normal",
                                  # initializer="ones",
                                  shape=(self.embedding_size, self.embedding_size),
                                  trainable=True)
        self.Wq = self.add_weight(name="Wq",
                                  initializer="random_normal",
                                  # initializer="ones",
                                  shape=(self.embedding_size, self.dim_k),
                                  trainable=True)
        self.Wv = self.add_weight(name="Wv",
                                  initializer="random_normal",
                                  # initializer="ones",
                                  shape=(self.embedding_size, self.dim_k),
                                  trainable=True)
        self.Whv = self.add_weight(name="Whv",
                                   initializer="random_normal",
                                   # initializer="ones",
                                   shape=(self.dim_k, 1),
                                   trainable=True)
        self.bhv = self.add_weight(name="bhv",
                                   shape=(1,),
                                   initializer="zeros",
                                   trainable=True)
        self.Whq = self.add_weight(name="Whq",
                                   initializer="random_normal",
                                   # initializer="ones",
                                   shape=(self.dim_k, 1),
                                   trainable=True)
        self.bhq = self.add_weight(name="bhq",
                                   shape=(1,),
                                   initializer="zeros",
                                   trainable=True)

        super(CoAttentionPara, self).build(input_shape)  # Be sure to call this somewhere!

    def call(self, inputs, mask=None):
        # t_mask = mask[0]
        tFeature = inputs[0]
        iFeature = inputs[1]
        # affinity matrix C
        affi_mat = K.dot(tFeature, self.Wb)
        affi_mat = K.batch_dot(affi_mat, K.permute_dimensions(iFeature, (0, 2, 1)))  # (batch_size, seq_len, num_region)
        # Hq, Hv, av, aq
        # image
        tmp_Hv = K.dot(tFeature, self.Wq)
        Hv = K.dot(iFeature, self.Wv) + K.batch_dot(K.permute_dimensions(affi_mat, (0, 2, 1)), tmp_Hv)
        Hv = K.tanh(Hv)
        # image attention
        av = K.squeeze(K.dot(Hv, self.Whv) + K.expand_dims(self.bhv, 0), axis=-1)
        av = K.softmax(av)

        # text
        tmp_Hq = K.dot(iFeature, self.Wv)
        Hq = K.dot(tFeature, self.Wq) + K.batch_dot(affi_mat, tmp_Hq)
        Hq = K.tanh(Hq)
        # masked text attention
        aq = K.squeeze(K.dot(Hq, self.Whq) + K.expand_dims(self.bhq, 0), axis=-1)
        # m = K.cast(t_mask, dtype="float32")
        # m = m - 1
        # m = m * REMOVE_FACTOR
        # aq = aq + m
        aq = K.softmax(aq)

        av = K.permute_dimensions(K.repeat(av, self.embedding_size), (0, 2, 1))
        aq = K.permute_dimensions(K.repeat(aq, self.embedding_size), (0, 2, 1))

        tfeature = aq * tFeature
        ifeature = av * iFeature

        return tfeature, ifeature

    def get_config(self):
        config = {'dim_k': self.dim_k}
        base_config = super(CoAttentionPara, self).get_config()

        return dict((k, v) for cfg in (config, base_config) for k, v in cfg.items())

    def compute_mask(self, inputs, mask=None):
        return None

    def compute_output_shape(self, input_shape):
        output_shape = (input_shape[0][0], input_shape[0][-1])
        return output_shape