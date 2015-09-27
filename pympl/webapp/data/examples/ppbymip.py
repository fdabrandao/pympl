from pympl import PyMPL

def read_table(fname, index1, index2, transpose=False):
    """Reads a table from a file."""
    if transpose:
        index1, index2 = index2, index1
    with open(fname) as f:
        text = f.read().replace(",", "")
        lst = list(map(float, text.split()))
        demand = {}
        for i1 in index1:
            for i2 in index2:
                if transpose:
                    demand[i2, i1] = lst.pop(0)
                else:
                    demand[i1, i2] = lst.pop(0)
        assert lst == []
        return demand

print("/*")
pympl = PyMPL(locals_=locals(), globals_=globals())
pympl.parse("model.mod")
print("*/")

print(pympl.output)
