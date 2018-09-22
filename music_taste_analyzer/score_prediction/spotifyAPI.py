import spotipy
import numpy as np

import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F

import net


# OAuth Token
# link : https://developer.spotify.com/console/get-search-item/?q=the%20police%20every%20breath%20you%20take&type=track&market=&limit=&offset=
user_token = "BQBnbzVS30A2tgSzquLxsUWOZqXS6FYlzQmqVf6HXqwacquQ9nxu3YYTIY9YKvkf4lcXIH57PFoZcIw9mMnGvgfvJSV3mMmsOwPFHnd85_Zyk2_iL1VoSjDrylzsDUUrjWTS4B-MisEszlj8a9vhX_HqG9Vo5g97fg"

sp = spotipy.Spotify(auth=user_token)

#Track id
def audio_feat_pretty(query):
	#Track id
	results = sp.search(q=query, type='track', limit=1)
	id = results["tracks"]["items"][0]["id"]
	#print(id)

	#Audio Features
	#aud_ana = sp.audio_analysis(id)
	aud_feat = sp.audio_features(id)[0]
	aud_feat_pretty = [aud_feat["danceability"],
						aud_feat["energy"],
						aud_feat["key"],
						aud_feat["loudness"],
						aud_feat["mode"],
						aud_feat["speechiness"],
						aud_feat["acousticness"],
						aud_feat["instrumentalness"],
						aud_feat["liveness"],
						aud_feat["valence"],
						aud_feat["tempo"],
						aud_feat["time_signature"],
						]

	return np.array(aud_feat_pretty)


# Liked songs
q1 = "The+Police+Every+Breath+You+Take"
vec1 = audio_feat_pretty(q1)
q2 = "Queen+Another+one+bites+the+dust"
vec2 = audio_feat_pretty(q2)
q3 = "Bowery+Electric"
vec3 = audio_feat_pretty(q3)
q4 = "one+kiss"
vec4 = audio_feat_pretty(q4)
q5 = "get+involved"
vec5 = audio_feat_pretty(q5)
q6 = "craig+leon"
vec6 = audio_feat_pretty(q6)
q7 = "cortex"
vec7 = audio_feat_pretty(q7)
q8 = "lizzy+mercier+descloux"
vec8 = audio_feat_pretty(q8)
q9 = "lord+shorty"
vec9 = audio_feat_pretty(q9)
q10 = "francis+bebey"
vec10 = audio_feat_pretty(q10)

# Unliked songs
q11 = "tokyo+hotel"
vec11 = audio_feat_pretty(q11)
q12 = "Slipknot+Psychosocial"
vec12 = audio_feat_pretty(q12)
q13 = "Vald"
vec13 = audio_feat_pretty(q13)
q14 = "afrojack"
vec14 = audio_feat_pretty(q14)
q15 = "mgmt+kids"
vec15 = audio_feat_pretty(q15)
q16 = "alesso"
vec16 = audio_feat_pretty(q16)
q17 = "stromae+alors+on+danse"
vec17 = audio_feat_pretty(q17)
q18 = "zedd+the+middle"
vec18 = audio_feat_pretty(q18)
q19 = "kendji+girac"
vec19 = audio_feat_pretty(q19)
q20 = "the+blaze"
vec20 = audio_feat_pretty(q20)


vec = np.array([vec1,vec2,vec3,vec4,vec5,vec6,vec7,vec8,vec9,vec10,
				vec11,vec12,vec13,vec14,vec15,vec16,vec17,vec18,vec19,vec20])
x = Variable(torch.Tensor(vec), requires_grad=True)
print("Shape of input : {}".format(x.shape))

res = np.array([0.95, 0.75, 0.94, 0.98, 0.8, 0.75, 0.9, 0.73, 0.85, 0.7,
				0.1, 0.1, 0.3, 0.13, 0.35, 0.13, 0.3, 0.1, 0.05, 0.08])
y = Variable(torch.Tensor(res), requires_grad=False)
y = y.view(len(y),1)
print("Shape of output : {}".format(y.shape))


# Model
network = net.Model()

# Train
learning_rate = 0.001
optimizer = torch.optim.SGD(network.parameters(), lr=learning_rate, momentum=0.9)
criterion = nn.MSELoss()


print("T R A I N I N G")
epochs = 10001
for epoch in range(epochs):
	optimizer.zero_grad()
	net_out = network(x)
	loss = criterion(net_out, y)
	loss.backward()
	optimizer.step()
	if epoch%1000==0:
		print('Train Epoch : {} Loss:{}'.format(epoch,loss.item()))

print("Desired output : {}".format(y))
print("Real Output : {}".format(network(x)))


# Test song
qtest1 = "shofukan"
vectest1 = audio_feat_pretty(qtest1)
x_test1 = Variable(torch.Tensor(vectest1))
pred1 = network(x_test1)
print("Prediction to like the first song : {}%".format(pred1.item()*100))


qtest2 = "spike+jones"
vectest2 = audio_feat_pretty(qtest2)
x_test2 = Variable(torch.Tensor(vectest2))
pred2 = network(x_test2)
print("Prediction to like the second song : {}%".format(pred2.item()*100))



