import re

import translator_api


def preprocess(s):
    s = s.replace("test cases", "sets of input data").replace("test case", "set of input data").replace("``",
                                                                                                        "<<").replace(
        "''", ">>").replace("testcase", "set of input data")

    s = s.strip().split("\n")
    if r"$t$ ($1" in s[0]:
        lim = s[0].split("(")[1].split(")")[0]
        s[0] = (
            f"Each test consists of several sets of input data. The first line contains one integer $t$ ({lim})~--- "
            f"the number of input data sets. The description of the input data sets follows.")

    for i in range(len(s)):
        s[i] = re.sub(r'\\(?!textbf)(\w+)(\[[^[]+?\])*(\{[^}]+?\})?', r'<span translate=no>\g<0></span>', s[i])
        s[i] = re.sub(r'\$.+?\$', r'<span translate=no>\g<0></span>', s[i])
    return s


s = open("../in.txt", encoding="utf-8").read()
s = preprocess(s)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {open("../credentials/token.txt").read().strip()}"
}

response = translator_api.send_request(s)

f = file = open("../out.txt", "w", encoding="utf-8")
for line in response:
    x = (line.get('text', '')
         .replace('<span translate="no">$', ' $')
         .replace('<span translate="no">\\', '\\')
         .replace('</span>', ' ')
         .replace(' ,', ',')
         .replace(' .', '.')
         .replace(' :', ':')
         .replace('( $', '($')
         .replace('$ )', '$)')
         .replace('} {', '}{')
         .replace('} (', '}(')
         .replace(') {', '){')
         .replace('{ ', '{')
         .replace(' }', '}')
         .replace('&lt;', '<')
         .replace('&gt;', '>')
         )
    x = re.sub(r'([^ ]) {2,3}([^ ])', r'\g<1> \g<2>', x).rstrip()
    x = re.sub(r'(\$.+?\$) число', r'число \g<1>', x).rstrip()
    x = re.sub(r'(\$.+?\$) числа', r'числа \g<1>', x).rstrip()
    x = re.sub(r'(\$.+?\$) чисел', r'чисел \g<1>', x).rstrip()
    print(x, file=f)
