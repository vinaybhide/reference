from tkinter import *
from tkinter import ttk

root = Tk()
#root.tk.call('info', 'patchlevel') 

style = ttk.Style()

tree = ttk.Treeview(root)

tree.tag_configure('alpha', background='blue')
tree.tag_configure('self', background='#DFDFDF')


tree["columns"] = ("one", "two", "three", "four", "five")

tree.column("one", width=150)
tree.column("two", width=100)
tree.column("three", width=100)
tree.column("four", width=100)
tree.column("five", width=100)
tree.heading("one", text="column A")
tree.heading("two", text="column B")
tree.heading("three", text="column C")
tree.heading("four", text="column D")
tree.heading("five", text="column E")


### insert format -> insert(parent, index, iid=None, **kw)
### reference: https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview
tree.insert("", 0, text="Line 1", values=("1A", "1b", "1c", "1d", "1e"))
tree.insert("", "end", text="sub dir 2", values=("2A", "2B", "2c", "2d", "2e"), tags=('self'))

### insert sub-item, method 1
id2 = tree.insert("", "end", "dir2", text="Dir 2")
dtemp = tree.item(id2)

#tree.insert(id2, "end", text="sub dir 2-1", values=("sub1", "sub2", "sub3"), tags=('self'))
idMarket = tree.insert(id2, "end", iid="market_cols", text='Market')
for i in range(3):
    tree.set(idMarket, i, value="sub" + str(i))

idMarket = tree.insert(id2, "end", iid="market_val", text='')
for i in range(3):
    tree.set(idMarket, i, "marketval_" + str(i))

idMarket = tree.insert(id2, "end", iid="holding_cols", text='')
for i in range(3):
    tree.set(idMarket, i, "sub" + str(i))

idMarket = tree.insert(id2, "end", iid="holding_val1", text='')
for i in range(3):
    tree.set(idMarket, i, "holdingval1_" + str(i))

idMarket = tree.insert(id2, "end", iid="holding_val2", text='')
for i in range(3):
    tree.set(idMarket, i, "holdingval2_" + str(i))


tree.insert(id2, "end", text="sub dir 2-2", values=("2A-2", "2B-2", "2C-2", "2D-2", "2E-2"))

### insert sub-item, method 2
tree.insert("", "end", "dir3", text="Dir 3")
tree.insert("dir3", "end", text=" sub dir 3", values=("3A", "3B"))
tree.pack()

tree.delete("holding_val2")

idMarket = tree.insert(id2, "end", iid="holding_val2", text='')
for i in range(3):
    tree.set(idMarket, i, "holdingval2_" + str(i))


tree.delete(*tree.get_children())

tup = tree.get_children()

print(tup)

"""alltuple=tree.get_children()
print(alltuple)
for ctr in alltuple:
    childrows = tree.get_children(ctr)
    for eachrow in childrows:
        print(eachrow)
        dictrow = tree.item(eachrow, 'values')
        print(dictrow)
"""
root.mainloop()