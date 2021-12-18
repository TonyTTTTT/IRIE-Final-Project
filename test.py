txt = '<?xml version="1.0"?><data><abstract><sec><title>Objective:</title><p>'

# for i in range(len(txt)):
#     if txt[i] == '<':
#         while txt[i] != '>':
#             txt = txt[:i] + txt[i+1:]
#         txt = txt[:i] + txt[i + 1:]

cnt = 0
while True:
    if cnt == len(txt):
        break
    if txt[cnt] == '<':
        while txt[cnt] != '>':
            txt = txt[:cnt] + txt[cnt+1:]
        txt = txt[:cnt] + txt[cnt+1:]
    else:
        cnt += 1
