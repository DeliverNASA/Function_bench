from time import time
import six
from chameleon import PageTemplate


BIGTABLE_ZPT = """\
<table xmlns="http://www.w3.org/1999/xhtml"
xmlns:tal="http://xml.zope.org/namespaces/tal">
<tr tal:repeat="row python: options['table']">
<td tal:repeat="c python: row.values()">
<span tal:define="d python: c + 1"
tal:attributes="class python: 'column-' + %s(d)"
tal:content="python: d" />
</td>
</tr>
</table>""" % six.text_type.__name__

def handle(req):
    num_of_rows = int(req)
    num_of_cols = int(req)

    start = time()
    tmpl = PageTemplate(BIGTABLE_ZPT)

    # 创建一个row * col的矩阵
    data = {}
    for i in range(num_of_cols):
        data[str(i)] = i

    table = [data for x in range(num_of_rows)]
    options = {'table': table}

    data = tmpl.render(options=options)
    latency = time() - start
    # print(latency)

    # result = json.dumps({'latency': latency, 'data': data})
    return latency

if __name__ == "__main__":
    handle(400)
    # print("mean: " + str(np.mean(total)))
    # print("std:  " + str(np.std(total)))
