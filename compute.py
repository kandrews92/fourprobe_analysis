from search import get_idx

def get_4probe_conduct(data, len4, wid4, str4):
	v3idx = get_idx(data, 'V3', 1)
	v2idx = get_idx(data, 'V2', 1)
	Ids_idx = get_idx(data, 'Ids', 1)
	conduct4probe = [str4]
	abs_conduct4probe = ["abs "+str4]
	diffV = ['V3-V2']
	nrows = len(data[0][:])
	ncols = len(data)
	for i in range(1, nrows):
		v3_v2 = data[v3idx][i] - data[v2idx][i]
		Ids = data[Ids_idx][i]
		conduct4 = Ids/v3_v2 * len4/wid4 * 1e6
		conduct4probe.append(conduct4)
		abs_conduct4probe.append(abs(conduct4))
		diffV.append(v3_v2)
	return conduct4probe, abs_conduct4probe, diffV

def get_2probe_conduct(data, len2, wid2, str2):
	Ids_idx = get_idx(data, 'Ids', 1)
	Vds_idx = get_idx(data, 'Vds', 1)
	conduct2probe = [str2]
	abs_conduct2probe = ["abs "+str2]
	abs_Ids = ['abs Ids']
	nrows = len(data[0][:])
	ncols = len(data)
	for i in range(1, nrows):
		Ids = data[Ids_idx][i]
		Vds = data[Vds_idx][i]
		conduct2 = Ids/Vds * len2/wid2 * 1e6
		conduct2probe.append(conduct2)
		abs_conduct2probe.append(abs(conduct2))
		abs_Ids.append(abs(Ids))
	return conduct2probe, abs_conduct2probe, abs_Ids


def get_trace_retrace(data, conduct4probe, conduct2probe, str4, str2):
	from inexactfloat import InexactFloat
	ncols = len(data)
	nrows = len(data[0][:])
	Vbg_idx = get_idx(data, 'Vbg', 1)
	trace_4probe = [str4+" trace"]
	trace_2probe = [str2+" trace"]
	retrace_4probe = [str4+" retrace"]
	retrace_2probe = [str2+" retrace"]
	for i in range(2, nrows-1):
		if InexactFloat(data[Vbg_idx][i]) == InexactFloat(data[Vbg_idx][i-1]):
			trace_idx = i 
	for j in range(1, trace_idx):
		trace_4probe.append(conduct4probe[j])
		trace_2probe.append(conduct2probe[j])
	for k in range(trace_idx, nrows):
		retrace_4probe.append(conduct4probe[k])
		retrace_2probe.append(conduct2probe[k])
	return trace_4probe, retrace_4probe, trace_2probe, retrace_2probe, trace_idx

