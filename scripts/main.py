import translator_api
import processing


orig = open("../in.txt", encoding="utf-8").read()
orig_escaped, replaces = processing.preprocess(orig)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {open("../credentials/token.txt").read().strip()}"
}

translated_escaped = translator_api.send_request(orig_escaped)

f = file = open("../out.txt", "w", encoding="utf-8")
translated = processing.postprocess(translated_escaped, replaces)
print(translated, end='', file=f)

print(f"Translated {len(orig)} symbols into {len(translated)} symbols")
