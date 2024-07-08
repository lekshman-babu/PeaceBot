import MultiHeadSelfAttention as m
import tensorflow as tf
from keras.layers import Layer,Dropout,LayerNormalization,Embedding

class DecoderBlock(Layer):
    def __init__(self,EMBEDDING_DIMENSIONS,NUM_OF_HEADS,HIDDEN_DIMENSIONS,DROPOUT=0.1):
        super(DecoderBlock,self).__init__()
        self.mhsa1=m.MultiheadSelfAttention(EMBEDDING_DIMENSIONS,NUM_OF_HEADS)
        self.mhsa2=m.MultiheadSelfAttention(EMBEDDING_DIMENSIONS,NUM_OF_HEADS)
        self.feedForwardLayer=m.feedForward(EMBEDDING_DIMENSIONS,HIDDEN_DIMENSIONS,DROPOUT)
        self.dropoutLayer1=Dropout(DROPOUT)
        self.dropoutLayer2=Dropout(DROPOUT)
        self.dropoutLayer3=Dropout(DROPOUT)
        self.layerNorm1=LayerNormalization()
        self.layerNorm2=LayerNormalization()
        self.layerNorm3=LayerNormalization()

    def call(self, encoderOut,target, training, decoderMask,memoryMask):
        mhsaOut1=self.mhsa1(target,target,target,decoderMask)
        mhsaOut1=self.dropoutLayer1(mhsaOut1,training=training)
        mhsaOut1=self.layerNorm1(mhsaOut1+target)

        mhsaOut2=self.mhsa2(mhsaOut1,encoderOut,encoderOut,memoryMask)
        mhsaOut2=self.dropoutLayer2(mhsaOut2,training=training)
        mhsaOut2=self.layerNorm2(mhsaOut1+mhsaOut2)

        feedOut=self.feedForwardLayer(mhsaOut2)
        feedOut=self.dropoutLayer3(feedOut,training=training)
        output=self.layerNorm3(feedOut+mhsaOut2)

        return output
    
class Decoder(Layer):
    def __init__(self,replyVocabSize,EMBEDDING_DIMENSIONS,NUM_OF_HEADS,HIDDEN_DIMENSIONS,NUM_OF_BLOCKS_DECODER,maxDecodingLen,DROPOUT=0.1):
        super(Decoder,self).__init__()
        self.maxDecodingLen=maxDecodingLen
        self.embeddingDimensions=EMBEDDING_DIMENSIONS
        self.tokenEncodingLayer=Embedding(replyVocabSize,self.embeddingDimensions)
        self.positionEncodingLayer=Embedding(self.maxDecodingLen,self.embeddingDimensions)
        self.dropout=Dropout(DROPOUT)
        self.blocks=[DecoderBlock(self.embeddingDimensions,NUM_OF_HEADS,HIDDEN_DIMENSIONS,DROPOUT) for _ in range(NUM_OF_BLOCKS_DECODER)]

    def call(self, encoderOut,target,training,decoderMask,memoryMask):
        tokenEmbeddings=self.tokenEncodingLayer(target)
        batch_size = tf.shape(target)[0]
        posIndex = tf.range(target.shape[1]) 
        posIndex = tf.broadcast_to(posIndex, [batch_size, target.shape[1]])
        posEncodings=self.positionEncodingLayer(posIndex)
        target=self.dropout(posEncodings+tokenEmbeddings,training=training)

        for block in self.blocks:
            target=block(encoderOut,target,training,decoderMask,memoryMask)
        return target
        