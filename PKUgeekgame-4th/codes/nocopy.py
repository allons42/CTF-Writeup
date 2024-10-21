import re

with open("不许复制 · Expert 难度.html", "r") as f:
    data = f.read()

# 获取每个data块的内容
code = re.findall('<div class="centralNoiseContent" id="centralNoiseContent1">(.*)兄弟你好香</span></div>', data)[0]
matches = re.findall(r'(data-[a-zA-Z0-9]*)=\"([IJl|1O0()i!]*)\"', code)
match_dict = {d[0]:d[1] for d in matches}

# 获取所有chunk的id和顺序
chunks = re.findall(r'(chunk-[a-zA-Z0-9]*)', code)
style = re.findall('<style>(#chunk-.*)</style></div>', data)[0]
matches = re.findall('#(chunk-[a-zA-Z0-9]*)::([a-z]*){content:(.*?)}', style)

# 获取重排序后每个chunk前后的数据
tar = {}
for ch, di, att in matches:
    atts = re.findall('attr\((data-[a-zA-Z0-9]*)\)', att)
    s = ""
    for a in atts:
        s += match_dict[a]
    tar[ch+di] = s
    
# 排序输出
final = ""
for c in chunks:
    if c + "before" in tar:
        final += tar[c + "before"]
    if c + "after" in tar:
        final += tar[c + "after"]
        
print(len(final)) 
print(final)