from time import time
import six
import json
from chameleon import PageTemplate
import numpy as np
import argparse

from time_limit import set_time_limit

parser = argparse.ArgumentParser()
parser.add_argument('-num_of_rows', type=int, default=400)
parser.add_argument('-num_of_cols', type=int, default=400)
args = parser.parse_args()

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

@set_time_limit()
def lambda_handler(event, context):
    num_of_rows = event['num_of_rows']
    num_of_cols = event['num_of_cols']

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
    event = dict()
    event['num_of_rows'] = args.num_of_rows
    event['num_of_cols'] = args.num_of_cols

    # print()
    # print("#### test: chameleon ####")
    total = list()
    for i in range(1):
        total.append(lambda_handler(event=event, context=None))
    # print("mean: " + str(np.mean(total)))
    # print("std:  " + str(np.std(total)))