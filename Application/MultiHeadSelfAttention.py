import tensorflow as tf
from tensorflow import keras
from keras.layers import Softmax,Layer,Dense
from keras.models import Sequential

def feedForward(EMBEDDING_DIMENSIONS,HIDDEN_DIMENSIONS,DROPOUT=0.1):
    return Sequential([
        Dense(HIDDEN_DIMENSIONS,activation='selu'),
        Dense(EMBEDDING_DIMENSIONS)
    ])

def scaledDotProdect(query,key,value,mask=None):
    keyDim=tf.cast(tf.shape(key)[-1],tf.float32)
    scores=tf.matmul(query,key,transpose_b=True)/tf.sqrt(keyDim)
    if mask is not None:
        scores += (1.0 - mask) * -1e9
    softmax=Softmax()
    weights=softmax(scores)
    return tf.matmul(weights,value)

class MultiheadSelfAttention(Layer):
    def __init__(self,EMBEDDING_DIMENSIONS,NUM_OF_HEADS):
        super (MultiheadSelfAttention,self).__init__()
        self.embeddingDimension=EMBEDDING_DIMENSIONS
        self.numOfHeads=NUM_OF_HEADS
        self.singleHeadDimensions=EMBEDDING_DIMENSIONS//NUM_OF_HEADS
        self.weightQuery=Dense(EMBEDDING_DIMENSIONS)
        self.weightKey=Dense(EMBEDDING_DIMENSIONS)
        self.weightValue=Dense(EMBEDDING_DIMENSIONS)
        self.denseLayer=Dense(EMBEDDING_DIMENSIONS)
    
    def splitHeads(self,input):
        batchSize = tf.shape(input)[0] 
        splitInputs=tf.reshape(input,(batchSize,-1,self.numOfHeads,self.singleHeadDimensions))
        return tf.transpose(splitInputs,perm=[0,2,1,3])
    
    def mergeHeads(self,input):
        batchSize = tf.shape(input)[0] 
        mergedInputs=tf.transpose(input,perm=[0,2,1,3])
        return tf.reshape(mergedInputs,(batchSize,-1,self.embeddingDimension))
    
    def call(self, q,k,v,mask=None):

        query=self.weightQuery(q)
        key=self.weightKey(k)
        value=self.weightValue(v)
        query=self.splitHeads(query)
        key=self.splitHeads(key)
        value=self.splitHeads(value)
        output=scaledDotProdect(query,key,value,mask)
        output=self.mergeHeads(output)
        return output
    
