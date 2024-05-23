
class c:
    def __init__(self):
        print("caprio")
    def s(self):
        print("zuccaprio")

def ciao(ty):
    istanza = ty()
    istanza.s()

ciao(c)