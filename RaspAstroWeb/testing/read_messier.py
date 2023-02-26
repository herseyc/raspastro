# Read from file ../xephemcat/Messier.edb

messier_list = []
FILE = "../xephemcat/Messier.edb"
with open(FILE) as lines:
    for line in lines:
      if not line.strip().startswith("#"):
          messier_list.append(line)


print(messier_list)
        
