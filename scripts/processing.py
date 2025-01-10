import re
import html

translate_inside_commands = ["textbf", "bf", "textit", "it", "footnote"]

s = ""
ans = ""
text_ind = 0


def add_symbols(add):
    global text_ind, ans
    ans += s[text_ind:text_ind + add]
    text_ind += add
    assert text_ind <= len(s)


def add_before(la, add_after=0):  # adds symbols while lambda is false and then add_after more
    global text_ind, ans

    while not la(s[text_ind:]):
        add_symbols(1)
        if text_ind == len(s):
            return False
    ans += s[text_ind:text_ind + add_after]
    text_ind += add_after
    return True


def add_until_correct_brackets(add_after=0):
    global text_ind, ans
    balance = 0
    while text_ind < len(s):
        if s[text_ind] in ["[", "{"]:
            balance += 1
        elif s[text_ind] in ["]", "}"]:
            balance -= 1

        if balance < 0:
            break
        add_symbols(1)
    ans += s[text_ind:text_ind + add_after]
    text_ind += add_after


def preprocess(text):
    global s, text_ind, ans

    text = text.replace("``", "<<").replace("''", ">>")
    s = text
    ans = ""
    text_ind = 0
    replaces = []  # string, space before start, space after end

    while text_ind < len(text):
        if text[text_ind:].startswith("$$"):
            ind_start = text_ind
            ans += '<span>'
            text_ind += 2
            assert add_before(lambda x: x.startwith("$$"))
            text_ind += 2
            ans += "</span>"
            replaces.append([text[ind_start:text_ind]])

        elif text[text_ind:].startswith("$"):
            ind_start = text_ind
            ans += '<span>'
            text_ind += 1
            assert add_before(lambda x: x.startswith("$"))
            text_ind += 1
            ans += "</span>"
            replaces.append([text[ind_start:text_ind]])

        elif text[text_ind] == '\\':
            ind_start = text_ind
            ans += '<span>'
            assert add_before(lambda x: x[0] in [' ', '\n', '$', '{', '['])

            if text[ind_start + 1:text_ind] in translate_inside_commands:  # not translating only the command
                assert add_before(lambda x: x[0] in ['{', '['], add_after=1)
                ans += "</span>"
                replaces.append([text[ind_start:text_ind]])
                add_until_correct_brackets(add_after=1)
            elif text[text_ind] in ['{', '[']:
                assert add_before(lambda x: x[0] in ['{', '['], add_after=1)
                add_until_correct_brackets(add_after=1)
                ans += "</span>"
                replaces.append([text[ind_start:text_ind]])
            else:
                ans += "</span>"
                replaces.append([text[ind_start:text_ind]])

        else:
            add_symbols(1)

    # saving info about spaces
    starts = [m.start() for m in re.finditer('<span>', ans)]
    ends = [m.end() for m in re.finditer("</span>", ans)]
    assert len(starts) == len(ends) == len(replaces)
    for i in range(len(replaces)):
        replaces[i].append(ans[starts[i] - 1:].startswith(' '))
        replaces[i].append(ans[ends[i]:].startswith(' '))
    return ans, replaces


def postprocess(text, replaces):
    text = html.unescape(text)

    starts = [m.start() for m in re.finditer('<span>', text)]
    ends = [m.end() for m in re.finditer("</span>", text)]
    assert len(starts) == len(ends) == len(replaces)

    ans = ""
    cur = 0
    for i in range(len(replaces)):
        ans += text[cur:starts[i]]
        if replaces[i][1] and ans[-1:] != ' ':
            ans += ' '
        elif not replaces[i][1] and ans[-1:] == ' ':
            ans = ans[:-1]
        ans += replaces[i][0]
        if replaces[i][2] and text[ends[i]:ends[i] + 1] != ' ':
            ans += ' '
        elif not replaces[i][2] and text[ends[i]:ends[i] + 1] == ' ':
            ends[i] += 1
        cur = ends[i]
    ans += text[cur:]
    return ans
