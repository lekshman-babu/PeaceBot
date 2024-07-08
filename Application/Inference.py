import numpy as np
import tensorflow as tf
from keras.utils import pad_sequences
from keras.models import model_from_json
from keras.preprocessing.text import tokenizer_from_json
import HyperParametersLoader as hpl
import Transformer as t
import random
import DatasetAccess as da

def inference(inputSentence, transformerModel, qtokenizer,rtokenizer, maxEncodingLen,maxDecodingLen):
    inputSequence = qtokenizer.texts_to_sequences([inputSentence])
    inputSequence = pad_sequences(inputSequence, maxlen=maxEncodingLen, padding='post')
    inputTensor = tf.convert_to_tensor(inputSequence)
    resultSentence = [rtokenizer.word_index['<start>']]
    for i in range(maxDecodingLen):
        target_sequence = tf.convert_to_tensor([resultSentence])
        output = transformerModel(inputTensor, target_sequence, training=False)
        predicted_token = tf.argmax(output[:, -1, :], axis=-1).numpy()[0]
        if predicted_token == rtokenizer.word_index['<end>']:
            break
        resultSentence.append(predicted_token)
    resultSentence = ' '.join([rtokenizer.index_word[token] for token in resultSentence if token not in [0,rtokenizer.word_index['<start>']]])
    dataset=da.main()
    try:
        result=random.choice(dataset[dataset['question']==inputSentence]['reply'].to_list())
        if result:
            return result
        else:
            result=random.choice(dataset[dataset['question'].str.contains(inputSentence,case=False)]['reply'].to_list())
    except:
        return resultSentence

def model():
    transformer=t.createModel()
    customObject={"Transformer":transformer}
    with open(f"{hpl.hParams['modelRoot']}{hpl.hParams['modelIndex']}/Model-Architecture.json", 'r') as f:
        modelArchitectureJson = f.read()
    transformer= model_from_json(modelArchitectureJson,custom_objects=customObject)
    transformer=t.createModel()
    inp=np.random.randint(1,size=hpl.hParams['encoderSequenceShape'])
    out=np.random.randint(1,size=hpl.hParams['decoderSequenceShape'])
    transformer(inp,out)
    transformer.load_weights(f"{hpl.hParams['modelRoot']}{hpl.hParams['modelIndex']}/Transformer.h5")
    return transformer

def output(input):
    transformer=model()
    return inference(input,
                     transformer,
                     tokenizer_from_json(hpl.tokenizor['questionTokenizor']),
                     tokenizer_from_json(hpl.tokenizor['replyTokenizor']),
                     hpl.hParams['maxEncodingLen'],
                     hpl.hParams['maxDecodingLen'])

if __name__=="__main__":
    print(output("i have sucidal thoughts"))