import MultiHeadSelfAttention as m
import tensorflow as tf
from keras.layers import Layer,Dropout,LayerNormalization,Embedding

class EncoderBlock(Layer):
    def __init__(self,EMBEDDING_DIMENSIONS,NUM_OF_HEADS,HIDDEN_DIMENSIONS,DROPOUT=0.1):
        super(EncoderBlock,self).__init__()

        self.mhsa=m.MultiheadSelfAttention(EMBEDDING_DIMENSIONS,NUM_OF_HEADS)
        self.feedForwardLayer=m.feedForward(EMBEDDING_DIMENSIONS,HIDDEN_DIMENSIONS,DROPOUT)
        self.dropoutLayer1=Dropout(DROPOUT)
        self.dropoutLayer2=Dropout(DROPOUT)
        self.layerNorm1=LayerNormalization()
        self.layerNorm2=LayerNormalization()
    
    def call(self,input,training,mask=None):
        
        mhsaOut=self.mhsa(input,input,input,mask)
        mhsaOut=self.dropoutLayer1(mhsaOut,training=training)
        mhsaOut=self.layerNorm1(input+mhsaOut)

        feedOut=self.feedForwardLayer(mhsaOut)
        feedOut=self.dropoutLayer2(feedOut, training=training)
        feedOut=self.layerNorm2(input+feedOut)

        return feedOut
    
class Encoder(Layer):
    def __init__(self,questionVocabSize,EMBEDDING_DIMENSIONS,maxEncodingLen,NUM_OF_HEADS,HIDDEN_DIMENSIONS,NUM_OF_BLOCKS_ENCODER,DROPOUT=0.1):
        super(Encoder,self).__init__()
        self.maxEncodingLen=maxEncodingLen
        self.embeddingDimensions=EMBEDDING_DIMENSIONS
        self.tokenEncodingLayer=Embedding(questionVocabSize,self.embeddingDimensions)
        self.positionEncodingLayer=Embedding(self.maxEncodingLen,self.embeddingDimensions)
        
        self.dropoutLayer=Dropout(DROPOUT)
        self.blocks=[EncoderBlock(self.embeddingDimensions,NUM_OF_HEADS,HIDDEN_DIMENSIONS) for _ in range(NUM_OF_BLOCKS_ENCODER)]

    def call(self, input, training, mask=None):
        tokenEncodings=self.tokenEncodingLayer(input)
        batch_size = tf.shape(input)[0] 
        # numPos=batch_size*self.maxEncodingLen
        posIndex = tf.range(self.maxEncodingLen)  # Use TensorFlow's range function
        posIndex = tf.broadcast_to(posIndex, [batch_size, self.maxEncodingLen])
        posEncodings=self.positionEncodingLayer(posIndex)
        input=self.dropoutLayer(posEncodings+tokenEncodings)
        for block in self.blocks:
            input=block(input,training,mask)
        return input