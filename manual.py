s = open("in.txt", encoding="utf-8").read()

s = s.replace(" —", "~---")
s = s.replace(" ---", "~---")
s = s.replace("—", "---")
s = s.replace("``", "<<")
s = s.replace("''", ">>")


s = s.replace("тестовым случаем", "набором входных данных")
s = s.replace("тестовом случае", "наборе входных данных")
s = s.replace("тестового случая", "набора входных данных")
s = s.replace("тестовых случаях", "наборах входных данных")
s = s.replace("тестовым случаям", "наборам входных данных")
s = s.replace("тестовый случай", "набор входных данных")
s = s.replace("тестовые случаи", "наборы входных данных")

s = s.replace("тестам", "наборам входных данных")
s = s.replace("тесте", "наборе входных данных")
s = s.replace("тесту", "набору входных данных")
s = s.replace("тестов", "наборов входных данных")
s = s.replace("теста", "набора входных данных")
s = s.replace("тест", "набор входных данных")
s = s.replace("не превышает $", "не превосходит $")

s = s.replace("положительных целых", "целых положительных")
s = s.replace("неотрицательных целых", "целых неотрицательных")
s = s.replace("неотрицательное целое", "целое неотрицательное")

s = s.replace("https://en.wikipedia.org/wiki/Bitwise_operation#AND", "https://ru.wikipedia.org/wiki/Битовая_операция#Побитовое_И")
s = s.replace("https://en.wikipedia.org/wiki/Bitwise_operation#OR", "https://ru.wikipedia.org/wiki/Битовая_операция#Побитовое_ИЛИ")
s = s.replace("https://en.wikipedia.org/wiki/Bitwise_operation#XOR", "https://ru.wikipedia.org/wiki/Битовая_операция#Побитовое_исключающее_ИЛИ")

open("in.txt", "w", encoding="utf-8").write(s)
