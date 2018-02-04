# Introduction

This project is a spinoff of the [rock-paper-scissors LSTM project](https://github.com/dennylslee/rock-paper-scissors-LSTM).  The last stage of the LSTM design is typically a softmax function.  The softmax function is a form of categorical normalization of the probability of each move (i.e. rock, paper or scissor). The highest probability move is the one LSTM is predicting what the opponent will put out.  The term "winning move" below is used loosely to reflects the LSTM correctly predicting the opponent's move (i.e. it does not necessarily mean literally the move LSTM puts out since as long as it predicts correctly, the move it puts out will beat the opponent).

The main objective of this project is to visualize those probabilities values (floating point value between 0 and 1) as a way to understand how the LSTM "think". 

In the RPS game, the softmax outputs are used to reduce to perform a prediction of the next move by selecting the highest probability value (most likely move prediction).  This is done using the argmax method.  However, to better visualize the probabilistic view of the LSTM outputs, all the predicted move's value are plotted:  both temporally and also spatially against one another. 

The secondary objective of this project is to learn the package bokeh.  The reference to bokeh and some of its gallary is [here](https://bokeh.pydata.org/en/latest/).  For some impression of bokeh, please see section below.

The main program for this project is in here:
rps-predict-bokeh.py

For reference to softmax, see [wiki](https://en.wikipedia.org/wiki/Softmax_function) and a quick tutorial at [pyimagesearch](https://www.pyimagesearch.com/2016/09/12/softmax-classifiers-explained/)

## Raw data selection

The raw time series is first read in from the csv files which were produced by the rock-paper-scissors LSTM project. 

For now, the selection is manual (should consider to switching to select widget with bokeh; but it has poor interaction with generic variables in the python code space).

```python

# read in the raw input
with open("testPredictResult_PRNG.csv", 'r', newline='\n') as g:
#with open("testPredictResult_RandRepeat.csv", 'r', newline='\n') as g:
#with open("testPredictResult_LFSR.csv", 'r', newline='\n') as g:
#with open("testPredictResult_RANDU.csv", 'r', newline='\n') as g:
	file = csv.reader(g, delimiter=',')
	rawlist = []
	for row in file:
		rawlist.append([float(i) for i in row])

```

## UI dashboard 

The dashboard consists of two main sections. The first sections are the rps probability plotted in time domain.  The second time series is simply the raw time series with a simple moving average (SMA) in which the window size can be interactively selected using the slider.

![image stack layer](https://github.com/dennylslee/rps-softmax-lstm-visualization-bokeh/blob/master/prob-time-series.png).


The 2nd section are pairwise comparison between each move (i.e. rock-paper, paper-scissors, rock-scissors).  There are 3 types of information shown this section of the dashboard:

1) the histogram representing the distribution of the probability values are plotted (both pairwise and 3-ways comparison are shown).

![image stack layer](https://github.com/dennylslee/rps-softmax-lstm-visualization-bokeh/blob/master/3ways-histogram.png). 

2) the winning margin plots show three 3-ways comparison plots - one for each winning move. This shows the differences between what the LSTM thinks would win (i.e. its highest probability selection) with respect to the next two moves' averages.  This "margin" reflects a form of confidence for that predicted move. 
3) the last set of plots are pairwise comparisons. In particular, the "identity line" (y = x) is the line which separate which move has the higher probability value.  The centroid calculation, which is a simple average of the winning cluster, represents the average of how strong the LSTM thinks that move is with respect to the other move in the pair. Futhermore, an eculidean distance is calculated to the identity line.  The further that distance, the more confident effectively the LSTM is predicting that move.  Since bokeh does not do 3D plot at the time of writing, these comparisons are done on a pair-wise basis.

![image stack layer](). 

## Impression with Bokeh

Bokeh is a handy package for generating web UI directly from a python coding environment.  By using bokeh, you don't have to deal with html, css, or javascipt; though the options to do lower level controls remain.  Bokeh also provides interactive actions from the browser and the plot objects.  It comes with a rich set of widget objects to select from. 

Some of the key shortcomings (albeit not all showstopper issues):
1) does not do 3D plot ... matplotlib or plotly are alternatives
2) bokeh interaction are limited to web objects (model objects mostly); it cannot easily control with variables in the python space. This is due to the fact that bokeh effectively produced JSON documents which are then used by the backend to convert into necessary html and java/js. The two worlds are in fact "separated" behind the scene.  However, for plot level interactive control, bokeh remains nonetheless a good tool. 
3) though there are many possible interactions that could be triggered through the callback functions; many 

There are three ways these plot level interactions can be implemented:
- JS call back: the widget can callback function that are implemented in javascript.  It is reasonably handy for those skilled in js.
- Python-based call back: this leverages PyScript within the flexx package.  This effectively transpile python into js but it does not support the full range of python synthax. 
- Server-based call back: one of the unique aspect of bokehs is that it operates a servr.  This server could be a locally launched server or bokeh's provided server on the public internet.  The server interacts with the browser to handle the necessary changes caused by the widgets' action. 

# Future Work

The raw data series is manual right now. I should change it to see if I can leverage the select widget from bokeh.  

There is some "rumor" that bokeh might extend its capability in the future to allow a namespace like design such that variables can be altered from callback directly from web interaction.  Watch out for this improvement and should try it out when it becomes available.