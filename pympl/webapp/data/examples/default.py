from pympl import PyMPL

print("/*")
pympl = PyMPL(locals_=locals(), globals_=globals())
pympl.parse("model.mod")
print("*/")

print(pympl.output)
