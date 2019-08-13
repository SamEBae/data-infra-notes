import subprocess

cmd = 'ps aux | sort -nrk 3,3 | grep filebeat | head -n 1'

cpu_float_arr = []

while True:
	result_line = subprocess.check_output(cmd, shell=True)
	str_list = list(filter(None, result_line.split(' ')))
	print(str_list)
	cpu_float_arr.append(
		float(str_list[2])
	)

total = 0 
avg = 0
print(sum(cpu_float_arr), sum(cpu_float_arr)/len(cpu_float_arr))