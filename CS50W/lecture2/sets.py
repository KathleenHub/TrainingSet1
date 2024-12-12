#create an empty set
s= set()

#add element to set
s.add(1)
s.add(2)
s.add(3)
s.add(4)
s.add(3) # this is not unique
print(s)

s.remove(2)
print(s)

len(s) #length

print(f"the set has {len(s)} elements")