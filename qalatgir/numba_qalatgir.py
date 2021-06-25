# import inspect
# from numba import jit
#
# from . import qalatgir
#
#
# for name, obj in inspect.getmembers(qalatgir):
#     if name.startswith('_') or inspect.isclass(obj) or inspect.isbuiltin(obj):
#         continue
#     elif inspect.isfunction(obj):
#         globals()['numba_' + name] = jit(obj, nopython=True)
