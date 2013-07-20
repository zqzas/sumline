from bottle import route, run, request, template

@route('/')
def hello():
    index = open('index.html', 'r').read()
    return index

@route('/search/<key>')
def search(key):
    if key == None or key == '':
        return hello()

    results = open('results.html', 'r').read()
    return template(results, key=key)


run(host='localhost', port=8080, debug=True)
