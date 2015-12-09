from search_tools import find_col_idx
from inexactfloat import InexactFloat

def find_trace(data, new_data, ncols, nrows, length, width):
	Vbg_idx = find_col_idx(data, 'Vbg',ncols)
	conduct_idx = find_col_idx(new_data, 'S(uS) L/W='+str(length)+"/"+str(width), ncols)
	trace = ['S(uS) trace L/W='+str(length)+"/"+str(width)]
	retrace = ['S(uS) retrace L/W='+str(length)+"/"+str(width)]
	for i in range(2,nrows-1):
		if InexactFloat(data[Vbg_idx][i]) == InexactFloat(data[Vbg_idx][i-1]):
			trace_idx = i
	for j in range(1,trace_idx):
		trace.append(new_data[conduct_idx][j])
	for k in range(trace_idx,nrows):
		retrace.append(new_data[conduct_idx][k])
	return trace, retrace

def compute_conductivity(data, newsheet, ncols, nrows, length, width):
	V3idx = find_col_idx(data, 'V3', ncols)
	V2idx = find_col_idx(data, 'V2', ncols)
	DrainIidx = find_col_idx(data, 'Ids',ncols)
	conductivity = ['S(uS) L/W='+str(length)+"/"+str(width)]
	diffV = ['V3-V2']
	for i in range(1,nrows):
		diffVval = data[V3idx][i]-data[V2idx][i]
		Ids = data[DrainIidx][i]
		conduct = Ids/diffVval * length/width * 10E6
		conductivity.append(conduct)
		diffV.append(diffVval)
	return  diffV, conductivity
