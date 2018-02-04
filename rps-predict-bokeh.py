
# --------------------------------------------------------------------------------------------
# use the bokeh local server for interaction
# on terminal run> bokeh serve --show rps-predict-bokeh.py
# --------------------------------------------------------------------------------------------

import csv
from bokeh.plotting import figure, output_file, show, ColumnDataSource, curdoc
from bokeh.layouts import gridplot, widgetbox, column
from bokeh.layouts import row as rowlayout
from bokeh.models import CustomJS, RangeSlider, RadioButtonGroup, Select, Slider
from bokeh.models import Range1d, Label, Jitter, HoverTool
import numpy as np
import math

# output to static HTML file
#output_file("lines.html")

# read in the raw input
with open("testPredictResult_PRNG.csv", 'r', newline='\n') as g:
#with open("testPredictResult_RandRepeat.csv", 'r', newline='\n') as g:
#with open("testPredictResult_LFSR.csv", 'r', newline='\n') as g:
#with open("testPredictResult_RANDU.csv", 'r', newline='\n') as g:
	file = csv.reader(g, delimiter=',')
	rawlist = []
	for row in file:
		rawlist.append([float(i) for i in row])

# function for histogram
nbins = 20
def histogram(list, nbins):
	x = np.array(list)
	n, bins = np.histogram(x, nbins, density=1)
	pdfx = np.zeros(n.size)
	pdfy = np.zeros(n.size)
	for k in range(n.size):
		pdfx[k] = 0.5*(bins[k]+bins[k+1])
		pdfy[k] = n[k]
	return pdfx, pdfy

# process the data
rawlist0 = [row[0] for row in rawlist] # the R row
rawlist1 = [row[1] for row in rawlist] # the P row
rawlist2 = [row[2] for row in rawlist] # the S row

# prepare data for the histogram plot
r_histx, r_histy = histogram(rawlist0, nbins)
p_histx, p_histy = histogram(rawlist1, nbins)
s_histx, s_histy = histogram(rawlist2, nbins)

# prepare the initial moving avg plot
cumsum0 = [sum(rawlist0[:index]) for index, i in enumerate(rawlist0,1)]
cumsum1 = [sum(rawlist1[:index]) for index, i in enumerate(rawlist1,1)]
cumsum2 = [sum(rawlist2[:index]) for index, i in enumerate(rawlist2,1)]
# create moving window average; account for padding at initial few index using the max and min flooring
movavg_window = 40
movavg0 = [(cs-cumsum0[max(index-movavg_window,0)])/(min(movavg_window,index)) for index, cs in enumerate(cumsum0,1)]
movavg1 = [(cs-cumsum1[max(index-movavg_window,0)])/(min(movavg_window,index)) for index, cs in enumerate(cumsum1,1)]
movavg2 = [(cs-cumsum2[max(index-movavg_window,0)])/(min(movavg_window,index)) for index, cs in enumerate(cumsum2,1)]

# prepare some data for the timestep (x) dimension
x = list(range(1, len(rawlist0)+1))

rp_r = [[row[0],row[1]] for row in rawlist if row[0]>row[1]] 		# built a list between R and P in which R is larger
rp_p = [[row[0],row[1]] for row in rawlist if row[0]<=row[1]]		# built a list between R and P in which P is larger
ps_p = [[row[1],row[2]] for row in rawlist if row[1]>row[2]]		# built a list between P and S in which P is larger
ps_s = [[row[1],row[2]] for row in rawlist if row[1]<=row[2]]		# built a list between P and S in which S is larger
rs_r = [[row[0],row[2]] for row in rawlist if row[0]>row[2]]		# built a list between R and S in which R is larger
rs_s = [[row[0],row[2]] for row in rawlist if row[0]<=row[2]]		# built a list between R and S in which S is larger

# gets all combination of the winning counts
rp_r_len = len(rp_r)
rp_p_len = len(rp_p)
ps_p_len = len(ps_p)
ps_s_len = len(ps_s)
rs_r_len = len(rs_r)
rs_s_len = len(rs_s)

# cal all the averages 
# account for the x and y axis orientation on the chart
rp_r_avg = [sum([row[1] for row in rp_r])/rp_r_len, sum([row[0] for row in rp_r])/rp_r_len]
rp_p_avg = [sum([row[1] for row in rp_p])/rp_p_len, sum([row[0] for row in rp_p])/rp_p_len]
ps_p_avg = [sum([row[1] for row in ps_p])/ps_p_len, sum([row[0] for row in ps_p])/ps_p_len]
ps_s_avg = [sum([row[1] for row in ps_s])/ps_s_len, sum([row[0] for row in ps_s])/ps_s_len]
rs_r_avg = [sum([row[1] for row in rs_r])/rs_r_len, sum([row[0] for row in rs_r])/rs_r_len]
rs_s_avg = [sum([row[1] for row in rs_s])/rs_s_len, sum([row[0] for row in rs_s])/rs_s_len]

# cal all the intersect on identity line
rp_r_intersec=[(rp_r_avg[0]+rp_r_avg[1])/2]*2 # repeat two times since the coordinate is on identity line
rp_p_intersec=[(rp_p_avg[0]+rp_p_avg[1])/2]*2
ps_p_intersec=[(ps_p_avg[0]+ps_p_avg[1])/2]*2 # repeat two times since the coordinate is on identity line
ps_s_intersec=[(ps_s_avg[0]+ps_s_avg[1])/2]*2
rs_r_intersec=[(rs_r_avg[0]+rs_r_avg[1])/2]*2 # repeat two times since the coordinate is on identity line
rs_s_intersec=[(rs_s_avg[0]+rs_s_avg[1])/2]*2

# cal the euclidean distance from centroid
rp_r_D = math.sqrt(abs(rp_r_intersec[1]-rp_r_avg[1])**2+abs(rp_r_intersec[0]-rp_r_avg[0])**2)
rp_p_D = math.sqrt(abs(rp_p_intersec[1]-rp_p_avg[1])**2+abs(rp_p_intersec[0]-rp_p_avg[0])**2)
ps_p_D = math.sqrt(abs(ps_p_intersec[1]-ps_p_avg[1])**2+abs(ps_p_intersec[0]-ps_p_avg[0])**2)
ps_s_D = math.sqrt(abs(ps_s_intersec[1]-ps_s_avg[1])**2+abs(ps_s_intersec[0]-ps_s_avg[0])**2)
rs_r_D = math.sqrt(abs(rs_r_intersec[1]-rs_r_avg[1])**2+abs(rs_r_intersec[0]-rs_r_avg[0])**2)
rs_s_D = math.sqrt(abs(rs_s_intersec[1]-rs_s_avg[1])**2+abs(rs_s_intersec[0]-rs_s_avg[0])**2)

# prepare data for range selection
startrange = 100
endrange = 1000
rawlist0_short_len = sum(rawlist0[startrange:endrange])/float(len(rawlist0[startrange:endrange]))
rawlist1_short_len = sum(rawlist1[startrange:endrange])/float(len(rawlist1[startrange:endrange]))
rawlist2_short_len = sum(rawlist2[startrange:endrange])/float(len(rawlist2[startrange:endrange]))
rps_avg=[rawlist0_short_len, rawlist1_short_len, rawlist2_short_len]

# prepare the win comparison data set
rwin_r, rwin_p, rwin_s = [], [], []
pwin_r, pwin_p, pwin_s = [], [], []
swin_r, swin_p, swin_s = [], [], []
rawlist_array = np.array(rawlist)
for index, k in enumerate(rawlist_array.argmax(axis=1)):
	if k == 0:
		rwin_r.append(rawlist[index][0])
		rwin_p.append(rawlist[index][1])
		rwin_s.append(rawlist[index][2])
	elif k ==1:
		pwin_r.append(rawlist[index][0])
		pwin_p.append(rawlist[index][1])
		pwin_s.append(rawlist[index][2]) 
	else:
		swin_r.append(rawlist[index][0])
		swin_p.append(rawlist[index][1])
		swin_s.append(rawlist[index][2])
rwin_r_avg, rwin_p_avg, rwin_s_avg = sum(rwin_r[:])/float(len(rwin_r)), sum(rwin_p[:])/float(len(rwin_p)), sum(rwin_s[:])/float(len(rwin_s))
pwin_r_avg, pwin_p_avg, pwin_s_avg = sum(pwin_r[:])/float(len(pwin_r)), sum(pwin_p[:])/float(len(pwin_p)), sum(pwin_s[:])/float(len(pwin_s))
swin_r_avg, swin_p_avg, swin_s_avg = sum(swin_r[:])/float(len(swin_r)), sum(swin_p[:])/float(len(swin_p)), sum(swin_s[:])/float(len(swin_s))



#-------------------------------------------------------------------------------------------------------------------------
# Prepare all the CDS 
movavg_src = ColumnDataSource(data=dict(x=x, y0=cumsum0, y1=cumsum1, y2=cumsum2, y3=movavg0 , y4=movavg1, y5=movavg2))
rawlist_src = ColumnDataSource(data=dict(x=x, rawlist0=rawlist0, rawlist1=rawlist1, rawlist2=rawlist2))
rps_avg_src = ColumnDataSource(data=dict(rps_average=rps_avg))
rp_src_r = ColumnDataSource(data=dict(r=[i[0] for i in rp_r], p=[i[1] for i in rp_r])) # built a list between R and P in which R is larger
rp_src_p = ColumnDataSource(data=dict(r=[i[0] for i in rp_p], p=[i[1] for i in rp_p])) # built a list between R and P in which P is larger
ps_src_p = ColumnDataSource(data=dict(p=[i[0] for i in ps_p], s=[i[1] for i in ps_p])) # built a list between P and S in which P is larger
ps_src_s = ColumnDataSource(data=dict(p=[i[0] for i in ps_s], s=[i[1] for i in ps_s])) # built a list between P and S in which S is larger
rs_src_r = ColumnDataSource(data=dict(r=[i[0] for i in rs_r], s=[i[1] for i in rs_r])) # built a list between R and S in which R is larger
rs_src_s = ColumnDataSource(data=dict(r=[i[0] for i in rs_s], s=[i[1] for i in rs_s])) # built a list between R and S in which S is larger

print ('Data Prep Done!')
size = 4
TOOLS="pan,wheel_zoom,box_zoom,undo,reset"

#-------------------------------------------------------------------------------------------------------------------------
# create a time series plot with RPS raw probabiities
p1 = figure(title="RPS Raw Probability Plot (from Softmax output)", x_axis_label='timestep', 
			y_axis_label='Instantaneous Prob Value', plot_width=900, plot_height=300,
			toolbar_location="above", tools=TOOLS,
			sizing_mode="scale_width")

# add 3 set of data points
p1c = p1.circle('x', 'rawlist0', legend="Rock", source=rawlist_src, size=size, color='blue', muted_alpha = 0.1)
p1d = p1.diamond('x', 'rawlist1', legend="Paper", source=rawlist_src, size=size, color='green', muted_alpha = 0.1)
p1t = p1.triangle('x', 'rawlist2', legend="Scissors", source=rawlist_src, size=size, color='red' , muted_alpha = 0.1)
p1.legend.location = "top_left"
p1.legend.click_policy="mute"

#-------------------------------------------------------------------------------------------------------------------------
# text book to print out the average of the probabilities
# the range slide seems to only trigger render on title change but not on annotation
textbox0 = figure(title="Average R probability: %.4f" % rawlist0_short_len, plot_width=300, plot_height=40, toolbar_location=None)
textbox1 = figure(title="Average P probability: %.4f" % rawlist1_short_len, plot_width=300, plot_height=40, toolbar_location=None)
textbox2 = figure(title="Average S probability: %.4f" % rawlist2_short_len, plot_width=300, plot_height=40, toolbar_location=None)

#--------------------------------------------------------------------------------------------
# create a time series with moving average of the probabilities values ; also use widget to control moving avg window size
p2 = figure(title="RPS Probability Moving Avg Plot", x_axis_label='timestep', 
			y_axis_label='Moving Avg of Prob Value', plot_width=900, plot_height=300, 
			x_range = p1.x_range,
			toolbar_location="above", tools=TOOLS,) 			# link the range to p1

# put all moving average and cumsum data into source via ColumnDataSource method.  Bokeh cannot hanlde mix mode
# add a line renderer with legend and line thickness
p2.line('x', 'y3', legend="Rock", source=movavg_src, line_width=2, color='blue',muted_alpha = 0.2)
p2.line('x', 'y4', legend="Paper", source=movavg_src, line_width=1, color='green', muted_alpha = 0.2)
p2.line('x', 'y5', legend="Scissors", source=movavg_src, line_width=1, color='red', muted_alpha = 0.2)
p2.legend.location = "top_left"
p2.legend.click_policy="mute"
# force a display offset at initialization
p2.y_range = Range1d(0.25, 0.4)

#-------------------------------------

# define a slider to control moving avg window size
# callback done in Python. IMPORTANT: need installation of flexx packaga w PyScript
# Pyscript does not support enumerate starting offset
def callback_win(source=movavg_src):
    data = source.data
    f = cb_obj.value
    x, y0, y1, y2 = data['x'], data['y0'], data['y1'], data['y2']
    data['y3'] = [(cs-y0[max(index+1-f,0)])/(min(f,index+1)) for index, cs in enumerate(y0)]
    data['y4'] = [(cs-y1[max(index+1-f,0)])/(min(f,index+1)) for index, cs in enumerate(y1)]
    data['y5'] = [(cs-y2[max(index+1-f,0)])/(min(f,index+1)) for index, cs in enumerate(y2)]
    source.change.emit()  # update 0.12.6 ... used for registering change to CDS

slider = Slider(start=0, end=200, value=10, step=1, title="SMA (Simple Moving Avg) Window Size",
				callback=CustomJS.from_py_func(callback_win))

#-----------------------------------------

# assume using bokeh server for handling change
def update_size(attrname, old, new):
	f = radio_group.active
	if f==0:
		#p1.x_axis_label = "Large button"
		p1c.glyph.size = 6
		p1d.glyph.size = 6
		p1t.glyph.size = 6
	elif f==1:
		p1c.glyph.size = 4
		p1d.glyph.size = 4
		p1t.glyph.size = 4
	else:		
		p1c.glyph.size = 2
		p1d.glyph.size = 2
		p1t.glyph.size = 2

radio_group = RadioButtonGroup(labels=["Large", "Medium", "Small"], active=1)
radio_group.on_change('active', update_size)

# assume using bokeh server for handling change
def do_rangeslider(attrname, old, new):
	f = range_slider.value
	f0, f1 = math.ceil(f[0]), math.ceil(f[1])
	data = rawlist_src.data
	data['x'] = x[f0:f1]
	data['rawlist0'] = rawlist0[f0:f1]
	data['rawlist1'] = rawlist1[f0:f1]
	data['rawlist2'] = rawlist2[f0:f1]
	d2 = rps_avg_src.data
	d2['rps_average'][0] = sum(rawlist0[f0:f1])/float(len(rawlist0[f0:f1]))
	d2['rps_average'][1] = sum(rawlist1[f0:f1])/float(len(rawlist1[f0:f1]))
	d2['rps_average'][2] = sum(rawlist2[f0:f1])/float(len(rawlist2[f0:f1]))
	textbox0.title.text = "Average R probability: %.4F" % d2['rps_average'][0]
	textbox1.title.text = "Average P probability: %.4F" % d2['rps_average'][1]
	textbox2.title.text = "Average S probability: %.4F" % d2['rps_average'][2]
	#p1.x_range=Range1d(f0, f1)  # frame the plot around the chosen range

# add a range slider for calculating a probability average 
range_slider = RangeSlider(start=0, end=len(rawlist0), value=(100, 1000), step=250, title="Range for averaging")
range_slider.on_change('value', do_rangeslider)

#--------------------------------------------------------------------------------------------
size_scatter = 2 

# create the scatter plot
p4 = figure(tools=TOOLS, plot_width=400, plot_height=400, min_border=10, min_border_left=50,
           toolbar_location="right",
           title="R-vs-P probability",
           x_axis_label='P move prob', y_axis_label='R move prob')
p4.background_fill_color = "#fafafa"
p4.scatter('p','r', source=rp_src_r, size=size_scatter, color="blue", alpha=0.1)
p4.scatter('p','r', source=rp_src_p, size=size_scatter, color="green", alpha=0.1)
p4.line(np.arange(0,0.8,0.1), np.arange(0,0.8,0.1), line_width=1, color='black')
# add annotation - must have units and Label is a class and cannot be called inside add_layout
a = Label(x=150, y=270, text="R wins:%d" % rp_r_len, text_color='blue', x_units='screen', y_units='screen')
b = Label(x=150, y=25, text="P wins:%d" % rp_p_len, text_color='green', x_units='screen', y_units='screen')
p4.add_layout(a)
p4.add_layout(b)
p4.y_range = Range1d(0.15, 0.55) # zoom in at initialization, delta should be consistent w plot height
p4.x_range = Range1d(0.15, 0.55) # zoom in at initialization, delta should be consistent w plot width
p4.circle(rp_p_avg[0], rp_p_avg[1], size=12, color='black')  # plot the centroid
p4.circle(rp_r_avg[0], rp_r_avg[1], size=12, color='black')  # plot the centroid
# plot euclidean distance line
p4.line([rp_r_avg[0], rp_r_intersec[0]], [rp_r_avg[1], rp_r_intersec[1]], line_width=1, color='black')
p4.line([rp_p_avg[0], rp_p_intersec[0]], [rp_p_avg[1], rp_p_intersec[1]], line_width=1, color='black')

p4_1 = figure(plot_width=400, plot_height=300, min_border=10, min_border_left=50,
           toolbar_location=None,
           title="R-vs-P histogram",
           x_axis_label='Probability', y_axis_label='Count')
p4_1.background_fill_color = "#fafafa"
p4_1.line(r_histx, r_histy, legend="Rock", line_width=1, color='blue', muted_alpha=0.2)
p4_1.line(p_histx, p_histy, legend="Paper", line_width=1, color='green', muted_alpha=0.2)
p4_1.legend.click_policy="mute"

#--------------------------------------------------------------------------------------------

# create the scatter plot
p5 = figure(tools=TOOLS, plot_width=400, plot_height=400, min_border=10, min_border_left=50,
           toolbar_location="right",
           title="P-vs-S probability",
           x_range=p4.x_range, y_range=p4.y_range,
           x_axis_label='S move prob', y_axis_label='P move prob')
p5.background_fill_color = "#fafafa"
p5.scatter('s','p', source=ps_src_p, size=size_scatter, color="green", alpha=0.1)
p5.scatter('s','p', source=ps_src_s, size=size_scatter, color="red", alpha=0.1)
p5.line(np.arange(0,0.8,0.1), np.arange(0,0.8,0.1), line_width=1, color='black')
# add annotation - must have units and Label is a class and cannot be called inside add_layout
a = Label(x=150, y=270, text="P wins:%d" % ps_p_len, text_color='green', x_units='screen', y_units='screen')
b = Label(x=150, y=25, text="S wins:%d" % ps_s_len, text_color='red', x_units='screen', y_units='screen')
p5.add_layout(a)
p5.add_layout(b)
p5.circle(ps_p_avg[0], ps_p_avg[1], size=12, color='black')
p5.circle(ps_s_avg[0], ps_s_avg[1], size=12, color='black')
# plot euclidean distance line
p5.line([ps_p_avg[0], ps_p_intersec[0]], [ps_p_avg[1], ps_p_intersec[1]], line_width=1, color='black')
p5.line([ps_s_avg[0], ps_s_intersec[0]], [ps_s_avg[1], ps_s_intersec[1]], line_width=1, color='black')


p5_1 = figure(plot_width=400, plot_height=300, min_border=10, min_border_left=50,
           toolbar_location=None,
           title="P-vs-S histogram",
           x_axis_label='Probability', y_axis_label='Count')
p5_1.background_fill_color = "#fafafa"
p5_1.line(p_histx, p_histy, legend="Paper", line_width=1, color='green', muted_alpha=0.2)
p5_1.line(s_histx, s_histy, legend="Scissors", line_width=1, color='red', muted_alpha=0.2)
p5_1.legend.click_policy="mute"

#--------------------------------------------------------------------------------------------

# create the scatter plot
p6 = figure(tools=TOOLS, plot_width=400, plot_height=400, min_border=10, min_border_left=50,
           toolbar_location="right",
           title="R-vs-S probability",
           x_range = p4.x_range, y_range=p4.y_range,
           x_axis_label='S move prob', y_axis_label='R move prob')
p6.background_fill_color = "#fafafa"
p6.scatter('s','r', source=rs_src_r, size=size_scatter, color="blue", alpha=0.1)
p6.scatter('s','r', source=rs_src_s, size=size_scatter, color="red", alpha=0.1)
p6.line(np.arange(0,0.8,0.1), np.arange(0,0.8,0.1), line_width=1, color='black')
# add annotation - must have units and Label is a class and cannot be called inside add_layout
a = Label(x=150, y=270, text="R wins:%d" % rs_r_len, text_color='blue', x_units='screen', y_units='screen')
b = Label(x=150, y=25, text="S wins:%d" % rs_s_len, text_color='red', x_units='screen', y_units='screen')
p6.add_layout(a)
p6.add_layout(b)
p6.circle(rs_r_avg[0], rs_r_avg[1], size=12, color='black')
p6.circle(rs_s_avg[0], rs_s_avg[1], size=12, color='black')
# plot euclidean distance line
p6.line([rs_r_avg[0], rs_r_intersec[0]], [rs_r_avg[1], rs_r_intersec[1]], line_width=1, color='black')
p6.line([rs_s_avg[0], rs_s_intersec[0]], [rs_s_avg[1], rs_s_intersec[1]], line_width=1, color='black')


p6_1 = figure(plot_width=400, plot_height=300, min_border=10, min_border_left=50,
           toolbar_location=None,
           title="R-vs-S histogram",
           x_axis_label='Probability', y_axis_label='Count')
p6_1.background_fill_color = "#fafafa"
p6_1.line(r_histx, r_histy, legend="Paper", line_width=1, color='blue', muted_alpha=0.2)
p6_1.line(s_histx, s_histy, legend="Scissors", line_width=1, color='red', muted_alpha=0.2)
p6_1.legend.click_policy="mute"

#--------------------------------------------------------------------------------------------
# Eulidean distance between the centriod and the identity line
# identity line represents where the probability is a tied (i.e. the LSTM is not too sure which one will win)

p7_textbox = figure(title=None, plot_width=400, plot_height=100, toolbar_location=None, background_fill_color='#2F2F2F')
rp_titletxt = Label(x=50, y=60, text="Eulidean Distance from Centriod to Identity Line", text_font_size='10pt', text_color='white', x_units='screen', y_units='screen')
a = Label(x=50, y=40, text="R: %.3f" % rp_r_D, text_font_size='10pt', text_color='white', x_units='screen', y_units='screen')
b = Label(x=50, y=20, text="P: %.3f" % rp_p_D, text_font_size='10pt',text_color='white', x_units='screen', y_units='screen')
p7_textbox.add_layout(rp_titletxt)
p7_textbox.add_layout(a)
p7_textbox.add_layout(b)

p8_textbox = figure(title=None, plot_width=400, plot_height=100, toolbar_location=None, background_fill_color='#2F2F2F')
ps_titletxt = Label(x=50, y=60, text="Eulidean Distance from Centriod to Identity Line", text_font_size='10pt', text_color='white', x_units='screen', y_units='screen')
a = Label(x=50, y=40, text="R: %.3f" % ps_p_D, text_font_size='10pt', text_color='white', x_units='screen', y_units='screen')
b = Label(x=50, y=20, text="P: %.3f" % ps_s_D, text_font_size='10pt',text_color='white', x_units='screen', y_units='screen')
p8_textbox.add_layout(ps_titletxt)
p8_textbox.add_layout(a)
p8_textbox.add_layout(b)

p9_textbox = figure(title=None, plot_width=400, plot_height=100, toolbar_location=None, background_fill_color='#2F2F2F')
rs_titletxt = Label(x=50, y=60, text="Eulidean Distance from Centriod to Identity Line", text_font_size='10pt', text_color='white', x_units='screen', y_units='screen')
a = Label(x=50, y=40, text="R: %.3f" % rs_r_D, text_font_size='10pt', text_color='white', x_units='screen', y_units='screen')
b = Label(x=50, y=20, text="P: %.3f" % rs_s_D, text_font_size='10pt',text_color='white', x_units='screen', y_units='screen')
p9_textbox.add_layout(rs_titletxt)
p9_textbox.add_layout(a)
p9_textbox.add_layout(b)

#--------------------------------------------------------------------------------------------

# use the trip names to identify which plot has the hover effect
# for some reasons,  the custom hover cannot be referenced along other tool bar items
hover = HoverTool(tooltips=[("(y)","($y)")], names=["hoverOn"])

p10 = figure(plot_width=400, plot_height=400, title="R win margin", y_axis_label='Prob', x_range=(0,4), tools=[hover])
p10.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
p10.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
p10.circle(x={'value':1.0,'transform': Jitter(width=0.4)}, y=rwin_r, color="blue", legend ="R", alpha=0.3)
p10.circle(x={'value':2.0,'transform': Jitter(width=0.4)}, y=rwin_p, color="green", legend="P", alpha=0.3)
p10.circle(x={'value':3.0,'transform': Jitter(width=0.4)}, y=rwin_s, color="red", legend="S",alpha=0.3)
p10.circle(x=[1, 2, 3], y=[rwin_r_avg, rwin_p_avg, rwin_s_avg], name="hoverOn", color='black', size=14)

p11 = figure(plot_width=400, plot_height=400, title="P win margin", y_axis_label='Prob', x_range=(0,4), tools=[hover], y_range=p10.y_range)
p11.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
p11.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
p11.circle(x={'value':2.0,'transform': Jitter(width=0.4)}, y=pwin_r, color="blue", legend ="R", alpha=0.3)
p11.circle(x={'value':1.0,'transform': Jitter(width=0.4)}, y=pwin_p, color="green", legend="P", alpha=0.3)
p11.circle(x={'value':3.0,'transform': Jitter(width=0.4)}, y=pwin_s, color="red", legend="S",alpha=0.3)
p11.circle(x=[1, 2, 3], y=[pwin_p_avg, pwin_r_avg, pwin_s_avg], name="hoverOn",color='black', size=14)

p12 = figure(plot_width=400, plot_height=400, title="S win margin", y_axis_label='Prob', x_range=(0,4), tools=[hover], y_range=p10.y_range)
p12.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
p12.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
p12.circle(x={'value':2.0,'transform': Jitter(width=0.4)}, y=swin_r, color="blue", legend ="R", alpha=0.3)
p12.circle(x={'value':3.0,'transform': Jitter(width=0.4)}, y=swin_p, color="green", legend="P", alpha=0.3)
p12.circle(x={'value':1.0,'transform': Jitter(width=0.4)}, y=swin_s, color="red", legend="S",alpha=0.3)
p12.circle(x=[1, 2, 3], y=[swin_s_avg, swin_r_avg, swin_p_avg], name="hoverOn", color='black', size=14)

#--------------------------------------------------------------------------------------------
# define overall layout
p3a = widgetbox(range_slider, radio_group, width=300, height=100)
p3b = widgetbox(slider, width=300)

#--------------------------------------------------------------------------------------------
# define a figure with all 3 historgram
p13 = figure(plot_width=1200, plot_height=300, min_border=10, min_border_left=50,
           toolbar_location=None,
           title="R-P-S probabiities histogram",
           x_axis_label='Probability', y_axis_label='Count')
p13.background_fill_color = "#fafafa"
p13.line(r_histx, r_histy, legend="Rock", line_width=1, color='blue', muted_alpha=0.2)
p13.line(p_histx, p_histy, legend="Paper", line_width=1, color='green', muted_alpha=0.2)
p13.line(s_histx, s_histy, legend="Scissors", line_width=1, color='red', muted_alpha=0.2)
p13.legend.click_policy="mute"

#--------------------------------------------------------------------------------------------
# layout and build the document for the bokeh server

p = rowlayout(p1, column(textbox0, textbox1, textbox2, p3a)) 	# raw prob time serioes
k = rowlayout(p2, p3b) 											# raw prob time series w SMA
j = rowlayout(p4_1, p5_1, p6_1)						# pairwise histogram
i = rowlayout(p7_textbox, p8_textbox, p9_textbox)	# textbox on distance from identity line
h = rowlayout(p4, p5, p6)							# pairwise probability scatter plot
m = rowlayout(p10, p11, p12)						# winning margin plot with jitter effect
n = rowlayout(p13)									# overall histogram pdf

# use the bokeh server
curdoc().add_root(p)
curdoc().add_root(k)
curdoc().add_root(n)
curdoc().add_root(m)
curdoc().add_root(i)
curdoc().add_root(h)
curdoc().add_root(j)
curdoc().title = "RPS dashboard"

# show the results (for manual built to output file without bokeh server)
#show(p)
