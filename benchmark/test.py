

test = []

a = {'views':'71,555','a':'b'}

test.append(a)
a = {'views':'6,555','a':'b'}
test.append(a)
a = {'views':'60,555','a':'b'}
test.append(a)
a = {'views':'81,555','a':'b'}
test.append(a)

test.sort(key=lambda item: item['views'], reverse=True) 

print(test[:2])