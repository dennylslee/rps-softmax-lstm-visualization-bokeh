# Introduction

This project is a spinoff of the [rock-paper-scissors LSTM project](https://github.com/dennylslee/rock-paper-scissors-LSTM).  The last stage of the LSTM design is typically a softmax function. In the context of this project, the softmax function is a form of categorical normalization of the probability of each move (i.e. rock, paper or scissor). The move with the highest probability is the one the LSTM is predicting what the opponent will put out.  The term "winning move" below is used loosely to reflect the LSTM correctly predicting the opponent's move (i.e. it does not necessarily mean literally the move LSTM puts out;  since as long as it predicts correctly, the move it puts out will beat the opponent).

The main objective of this project is to visualize those probability values (floating point value between 0 and 1) as a way to understand how the LSTM "thinks". 

In the RPS game, the softmax outputs are used to generate a prediction of the next move by selecting the highest probability value (i.e. the most likely move prediction).  This is done using the argmax method.  However, to better visualize the probabilistic view of the LSTM outputs, all the moves's probability values are plotted:  both temporally and also spatially against one another. 

The secondary objective of this project is to learn the general ability of the visualization package bokeh.  The reference to bokeh and some of its gallary is [here](https://bokeh.pydata.org/en/latest/).  For my impression of using bokeh on this simple project, please see later section below.

The main program for this project is in here: [rps-predict-bokeh.py](https://github.com/dennylslee/rps-softmax-lstm-visualization-bokeh/blob/master/rps-predict-bokeh.py)

After bokeh is installed on the local host, the program can be run by executing the following command in the terminal:

```
bokeh serve --show rps-predict-bokeh.py
```


For reference to softmax, see [wiki](https://en.wikipedia.org/wiki/Softmax_function) and a quick tutorial at [pyimagesearch](https://www.pyimagesearch.com/2016/09/12/softmax-classifiers-explained/)

## Raw data selection

The raw time series is first read in from the csv files which were produced by the rock-paper-scissors LSTM project. 

For now, this selection is manual (I should consider switching to the select widget provided by bokeh; but its poor interaction with generic variables in the python code space prevents me from pursuing further at this point).

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

The dashboard consists of two main sections. The first section consists of two rps probability values plots in time domain.  The second time series is simply the raw time series with a simple moving average (SMA) in which the window size can be interactively selected using the slider. SMA tends to reveal the "support" level as oppose to exponential moving average (EMA).  A simple comparison can be found [here](https://www.investopedia.com/ask/answers/05/smavsema.asp)

![image stack layer](https://github.com/dennylslee/rps-softmax-lstm-visualization-bokeh/blob/master/prob-time-series.png).


The 2nd section consists of charts the captures pairwise comparison between move types (i.e. rock-paper, paper-scissors, rock-scissors).  There are 3 types of information shown this section of the dashboard:

1) the histogram representing the distribution of the probability values are plotted (both pairwise and 3-ways comparison are shown).

![image stack layer](https://github.com/dennylslee/rps-softmax-lstm-visualization-bokeh/blob/master/3ways-histogram.png). 

2) the winning margin plots show three 3-ways comparison plots - one for each winning move. These chart shows the differences between what the LSTM thinks would win (i.e. the highest probability selection) with respect to the next two moves' averages.  This "margin" reflects a form of confidence for that predicted winning move. One could say the higher the margin, the more certain the LSTM is about that predicted move.

![image stack layer](https://github.com/dennylslee/rps-softmax-lstm-visualization-bokeh/blob/master/pairwise-win-margin.png). 

3) the last set of plots are pairwise comparisons of probability values. In particular, the "identity line" (y = x) is the line which separate the region of the winning move. The region below the identity line is the winning move region for the x-axis move types.  The centroid calculation, which is a simple average of the winning cluster, represents the average of how strong the LSTM thinks that move is with respect to the other move in the pairwise comparison. Futhermore, an eculidean distance is calculated to the identity line.  The further that distance, the more confident (effectively) the LSTM is predicting that move. That is, it has better winning margin than the comparing move.  Since bokeh does not support 3D plot at this time, these comparisons are done on a pair-wise basis.

![image stack layer](https://github.com/dennylslee/rps-softmax-lstm-visualization-bokeh/blob/master/pairwise-comparison.png). 

## Impression with Bokeh

Bokeh is a handy package for generating web UI directly from a python coding environment.  By using bokeh, you don't have to deal with html, css, or javascipt; though the options to do lower level controls remain for the developers.  Bokeh also provides support for interactive actions between the browser and the plot objects.  Bokeh comes with a rich set of widget objects for interaction purposes. 

Some of the key shortcomings (albeit not all showstopper issues):
1) bokeh does not support 3D plot ... for that, matplotlib or plotly are better alternatives.
2) bokeh interactions are limited to its web objects (model objects mostly). It cannot easily interacts with all variables in the python code space. This is due to the fact that bokeh's architecture effectively produced JSON documents which are then used by its backend to convert into the necessary html and java/js code. The two worlds (input in python and output in web) are in fact "separated" behind the scene.  However, for plot level interactive control, bokeh remains nonetheless a good tool. 
3) though there are many possible interaction methods that could be triggered through the callback functions; there are also some limitation I experienced during the process.  See summary below. 

### Bokeh callback options

There are three ways the plot level interactions can be implemented:
- JS callback: the widget can callback function that are implemented in javascript.  It is reasonably handy for those skilled in js.
- Python-based callback: this leverages the library PyScript from the flexx package.  PyScript effectively transpiles python into js but it does not support the full range of python synthax. 
- Server-based callback: one of the unique aspect of bokeh is that it operates a servr.  This server could be a locally launched server or bokeh-provided server on the public internet.  The server interacts with the browser to handle the necessary changes caused by the widgets' action. 

# Future Work

The raw data series is manually selected right now. It would be much cleaner to leverage the select widget from bokeh.  

There is some "rumor" that bokeh might extend its capability in the future to allow a namespace-like design approach such that variables can be altered from web interaction callback. Let's keep an eye out for this bokeh improvement and try it out when it becomes available.