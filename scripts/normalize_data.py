#!/usr/bin/env python3
import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'data'/'opportunities.json'
def flatten(value):
 if isinstance(value,dict): return [value]
 if isinstance(value,list):
  out=[]
  for item in value: out.extend(flatten(item))
  return out
 return []
records=flatten(json.loads(p.read_text()))
p.write_text(json.dumps(records,indent=2)+'\n')
print(f'Normalized {len(records)} tracker records')
