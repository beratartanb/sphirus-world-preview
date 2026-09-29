import unreal as u, builtins, gc, types
n = 0
for f in gc.get_objects():
    if isinstance(f, types.FunctionType) and f.__name__ == 'tick':
        g = f.__globals__
        if 'state' in g and 'cases' in g and isinstance(g['state'], dict) and 'phase' in g['state']:
            if g['state'].get('running'): g['state']['i'] = len(g['cases']); g['state']['phase'] = 0; n += 1
print('capture tickers flagged to finish:', n)
