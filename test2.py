cand_name = ['xiaoming', 'xiaohua', 'xiaojuhua']
answer = 'xiaohua'
for n in cand_name:
	if answer in n:
		print('True')
		break
	else:
		print('False')