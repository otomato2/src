# このコードはどのように利用していただいてもかまいません．
# ただし，実行したことによる損害や問題に関して当方は責任を負いかねます．
# ご理解の上ご利用ください．

import requests
import re

url = "https://docs.python.org/ja/3/library/codecs.html"

r = requests.get(url)
content = r.content

content = content.decode()

begin = '<th class="head"><p>言語</p></th>\n</tr>\n</thead>\n<tbody>\n'
end = '<p><span class="versionmodified changed">バージョン 3.4 で変更: </span>utf-16* と utf-32* のエンコーダは、サロゲートコードポイント (<code class="docutils literal notranslate"><span class="pre">U+D800</span></code>--<code class="docutils literal notranslate"><span class="pre">U+DFFF</span></code>)  がエンコードされることを許可しなくなりました。utf-32* デコーダは、サロゲートコードポイントに対応するバイト列をデコードしなくなりました。</p>\n'
idx1 = content.find(begin)
idx2 = content.find(end)
result = content[idx1+len(begin):idx2+len(end)]

result = result.replace("\n", "")

idx = 0
encode_d = {}

codec_begin = '"><td><p>'
codec_end = '</p></td>'
lang_begin = '<td><p>'
lang_end = '</p></td>'
lang_end_special = '</p><div class'

while 1:
  matchObj = re.search(rf'{codec_begin}(.*?){codec_end}', result[idx:])
  if matchObj == None:
    break
  codec_tmp = matchObj.group()[len(codec_begin):-len(codec_end)]
  # print("Codec: ", matchObj.group())
  idx += matchObj.end()
  matchObj = re.search(r'<td>(.*?)</td>', result[idx:])
  # print("alias: ", matchObj.group())
  idx += matchObj.end()
  matchObj1 = re.search(rf'{lang_begin}(.*?){lang_end}', result[idx:])
  matchObj2 = re.search(rf'{lang_begin}(.*?){lang_end_special}', result[idx:])
  if matchObj1 != None and matchObj2 != None:
    if len(matchObj1.group()) < len(matchObj2.group()):
      lang_tmp = matchObj1.group()[len(lang_begin):-len(lang_end)]
    else:
      lang_tmp = matchObj2.group()[len(lang_begin):-len(lang_end_special)]
  elif matchObj1 == None:
    lang_tmp = matchObj2.group()[len(lang_begin):-len(lang_end_special)]
  else:
    lang_tmp = matchObj1.group()[len(lang_begin):-len(lang_end)]
  idx += matchObj.end()
  encode_d[codec_tmp] = lang_tmp

fname = 'filename'

for k in encode_d:
  try:
    with open(fname, 'r', encoding=f"{k}") as f:
      f.readline()
      print("codec: ", k.rjust(14), ", lang: ", encode_d[k])
  except UnicodeDecodeError as e:
    pass