import pandas as pd
import json
def convert(x):
    ''' Convert a json string to a flat python dictionary
    which can be passed into Pandas. '''
    ob = json.loads(x)
    for k, v in ob.items():
        if isinstance(v, list):
            ob[k] = ','.join(str(v))
        elif isinstance(v, dict):
            for kk, vv in v.items():
                ob['%s_%s' % (k, kk)] = vv
            del ob[k]
    return ob
 
json_filename='user.json'
csv_filename='user.csv'
print 'Converting %s to %s' % (json_filename, csv_filename)
df = pd.DataFrame([convert(line) for line in file(json_filename)])
df.to_csv(csv_filename, encoding='utf-8', index=False)
