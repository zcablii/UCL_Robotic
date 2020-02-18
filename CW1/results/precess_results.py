reslist = [
289	,110,	110	,351,	193,	278,	264
]
min_res = min(reslist)
reslist = [item / min_res -1 for item in reslist]
print(reslist)
