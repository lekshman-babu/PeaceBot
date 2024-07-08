import Encoder as e
import Decoder as d
import tensorflow as tf
from keras import Model
from keras.layers import Dense
import HyperParametersLoader as hp

class Transformer(Model):
    def __init__(self, questionVocabSize,replyVocabSize,EMBEDDING_DIMENSIONS,maxEncodingLen,maxDecodingLen,NUM_OF_HEADS,HIDDEN_DIMENSIONS,NUM_OF_BLOCKS_ENCODER,NUM_OF_BLOCKS_DECODER,dropout=0.1):
        super(Transformer,self).__init__()
        self.encoder=e.Encoder(questionVocabSize,EMBEDDING_DIMENSIONS,maxEncodingLen,NUM_OF_HEADS,HIDDEN_DIMENSIONS,NUM_OF_BLOCKS_ENCODER,dropout)
        self.decoder=d.Decoder(replyVocabSize,EMBEDDING_DIMENSIONS,NUM_OF_HEADS,HIDDEN_DIMENSIONS,NUM_OF_BLOCKS_DECODER,maxDecodingLen,dropout)

        self.finalLayer=Dense(replyVocabSize)
    
    def call(self,input,target,training=False):
        encoderMask=tf.cast(tf.math.not_equal(input,0),tf.float32)
        encoderMask=encoderMask[:,tf.newaxis,tf.newaxis,:]
        
        decoderMask=tf.cast(tf.math.not_equal(target,0),tf.float32)
        decoderMask=decoderMask[:,tf.newaxis,tf.newaxis,:]
        lookAheadMask=tf.linalg.band_part(tf.ones((target.shape[1],target.shape[1])),-1,0)
        decoderMask=tf.minimum(decoderMask,lookAheadMask)

        encoderOut=self.encoder(input,mask=encoderMask,training=training)
        decoderOut=self.decoder(encoderOut,target,training=training,decoderMask=decoderMask,memoryMask=encoderMask)

        output=self.finalLayer(decoderOut)
        return output

def createModel():
    return Transformer(
            hp.hParams['questionVocabSize'],
            hp.hParams['replyVocabSize'],
            hp.hParams['EMBEDDING_DIMENSIONS'],
            hp.hParams['maxEncodingLen'],
            hp.hParams['maxDecodingLen'],
            hp.hParams['NUM_OF_HEADS'],
            hp.hParams['HIDDEN_DIMENSIONS'],
            hp.hParams['NUM_OF_BLOCKS_ENCODER'],
            hp.hParams['NUM_OF_BLOCKS_DECODER'],
            hp.hParams['DROPOUT']
            )