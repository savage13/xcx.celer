#!/usr/bin/env python
import math
import json

v = json.load(open("qE8XszzDOgV2ZTyLcN8m1A.1127051.json", "r"))
ents = v['entities']
items = {
    "FNSite": {},
    "Treasure": {},
    "StuffedLobster": {},
    "Loc": {},
}
for key,v in ents.items():
    data = v.get('data')
    if not data:
        continue
    if data.get('latLng') is None:
        continue
    name = data.get('name')
    name = name.replace("(Map Marker)", "").strip()
    name = name.replace(" ", "")
    name = name.replace("#", "")
    name = name.replace(",the", "The")
    name = name.replace("'", "")
    name = name.replace('"', "")
    xy = data.get('latLng')
    x = xy.get('lng') or xy.get('lon')
    x = float(x)
    y = float(xy.get('lat'))
    xy0 = f"{x:.3f}, {y:.3f}"

    y2 = math.degrees( math.log(math.tan(math.pi/4 + math.radians(y)/2)))/2
    xy = [x, y2]
    if name.startswith("Treasure"):
        name = int(name.replace("Treasure", ""))
        items['Treasure'][name] = {'coord': xy, 'icon': 'treasure', 'coordxy': xy0}
        items['Treasure'][name]['name'] = f'Treasure {name}'
    elif name.startswith("FNSite"):
        name = int(name.replace("FNSite", ""))
        items['FNSite'][name] = {'coord': xy, 'icon': 'fnsite','coordxy': xy0}
        items['FNSite'][name]['name'] = f'FNSite {name}'
    elif name.startswith("StuffedLobster"):
        name = int(name.replace("StuffedLobster", ""))
        items['StuffedLobster'][name] = {'coord': xy, 'icon': 'lobster','coordxy': xy0}
        items['StuffedLobster'][name]['name'] = f'Stuffed Lobster {name}'
    else:
        items['Loc'][name] = {'coord': xy, 'icon': 'loc','coordxy': xy0}
        items['Loc'][name]['name'] = name

names = []
print("presets:")
for key, vals in items.items():
    print(f"  _{key}:")
    
    for name, obj in dict(sorted(vals.items())).items():
        print(f'    {name}:')
        print(f'      text: {obj["name"]}')
        print(f'      icon: {obj["icon"]}')
        print(f'      coord: {obj["coord"]}')
        print(f'      notes: {obj["coordxy"]}')
        names.append(f"- _{key}::{name}")

with open("route.yaml","w") as f:
    print('''
- First Segment Name:
  - Location at (0,0):
     notes: (0, 0)
     comment: Comment stuff
     coord: [0, 0]
  - Location at (200, 80):
     notes: (200, 80)
     comment: Comments
     coord: [200, 80]
  - Location at (200, -80):
     notes: (200, -80)
     comment: Silly Comment
     coord: [200, -80]
  - Location at (-200, -80):
     notes: (-200, -80)
     comment: Sutff
     coord: [-200, -80]
  - Location at (-200, 80):
     notes: (-200, 80)
     comment: More Stuff
     coord: [-200, 80]
  - Location at (200, 80) again:
     notes: (200, 80)
     comment: Hi :D
     coord: [200, 80]
''', file=f)
    print("- Second Segment:", file=f)
    for name in names:
        print(f"  {name}", file=f)
