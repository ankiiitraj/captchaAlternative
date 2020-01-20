import tensorflow as tf
import matplotlib.pyplot as plt
import librosa as lb
import numpy as np
import pylab

import wave
import numpy as np
import matplotlib.pyplot as plt

test_file = './mywav.wav'

y, sr = lb.load(test_file)
pylab.axis('off') # no axis
pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # Remove the white edge
S = lb.feature.melspectrogram(y, sr)
r = len(S)    # 3 rows in your example
c = len(S[0]) # 2 columns in your example
sm=0
for i in range(0,c):
    for j in range(0,r):
        sm=sm+S[j][i]
sm=sm/(r*c)
S=S*(100/sm)
s = np.log10(S+0.0001)+5
z=s[:,30:80]

t1 = z.reshape(128, 50, 1)

tx=[t1]

# import tflearn 
# from tflearn.layers.conv import conv_2d, max_pool_2d 
# from tflearn.layers.core import input_data, dropout, fully_connected 
# from tflearn.layers.estimator import regression 

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten
#create model
model = Sequential([
    keras.layers.Conv2D(16, 3, padding='same', activation='relu', input_shape=(128, 50, 1)),
    keras.layers.MaxPooling2D(),
    keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
    keras.layers.MaxPooling2D(),
    keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
    keras.layers.MaxPooling2D(),
    keras.layers.Flatten(),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(60, activation='relu'),
    keras.layers.Dense(2, activation='softmax')
])


model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

model.load_weights('./checkpoint_model_2/my_checkpoint')

prediction = model.predict([tx])

if(np.argmax(prediction[0])==1):
    print("Human Voice")
else:
    print("Machine Voice")