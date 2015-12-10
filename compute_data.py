from search_tools import find_col_idx
from inexactfloat import InexactFloat

def find_trace(data, new_data, ncols, nrows, length, width, f_probe_str):
	Vbg_idx = find_col_idx(data, 'Vbg',ncols)
	conduct_idx = find_col_idx(new_data, f_probe_str, ncols)
	trace = [f_probe_str+" trace"]
	retrace = [f_probe_str+" retrace"]
	for i in range(2,nrows-1):
		if InexactFloat(data[Vbg_idx][i]) == InexactFloat(data[Vbg_idx][i-1]):
			trace_idx = i
	for j in range(1,trace_idx):
		trace.append(new_data[conduct_idx][j])
	for k in range(trace_idx,nrows):
		retrace.append(new_data[conduct_idx][k])
	return trace, retrace

def compute_conductivity(data,newsheet,ncols,nrows, length, width, f_probe_str, t_probe_str):
	V3idx = find_col_idx(data, 'V3', ncols)
	V2idx = find_col_idx(data, 'V2', ncols)
	DrainIidx = find_col_idx(data, 'Ids',ncols)
	conductivity = [f_probe_str]
	abs_conductivity = ["abs "+f_probe_str]
	diffV = ['V3-V2']
	for i in range(1,nrows):
		diffVval = data[V3idx][i]-data[V2idx][i]
		Ids = data[DrainIidx][i]
		conduct = Ids/diffVval * length/width * 1E6
		conductivity.append(conduct)
		abs_conductivity.append(abs(conduct))
		diffV.append(diffVval)
	return  diffV, conductivity, abs_conductivity

def compute_fe_mobility(data, new_data, ncols, nrows, capacitence, length, width, f_probe_str):
	import numpy as np
	Vbgidx = find_col_idx(data, 'Vbg', ncols)
	conduct_idx = find_col_idx(new_data, f_probe_str, ncols)
	print conduct_idx
	Vbg = np.zeros(nrows)
	S = np.zeros(nrows)
	for i in range(1,nrows):
		Vbg[i] = data[Vbgidx][i]
	for i in range(1,nrows):
		S[i] = data[conduct_idx][i]
	dVbg = np.diff(Vbg)
	#for i in range(1,nrows):
	# mu = dS/dVbg  * 1/C 
	mobility = np.diff(S)/dVbg * 1/capacitence
	return mobility