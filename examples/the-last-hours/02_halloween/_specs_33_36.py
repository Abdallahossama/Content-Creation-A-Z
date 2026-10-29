"""one-off: insert the beat specs for Shorts 33-36 into specs.py"""
import re, sys
p = "specs.py"; s = open(p, encoding="utf-8").read()
views = '''V_FL, V_SCOT, V_PNW, V_TENA, V_KY = (-79.6, 26.8, 7.5), (-6.0, 57.9, 9.0), (-122.4, 46.5, 3.6), (-122.75, 45.75, 1.2), (-85.7, 37.8, 9.0)
FTL, HC, P2, P3 = (-80.15, 26.07), (-79.1, 26.0), (-77.86, 26.0), (-78.19, 27.18)
PDX, SEA, TENA = (-122.60, 45.59), (-122.31, 47.45), (-122.75, 45.72)
'''
if "V_FL" not in s:
    s = s.replace('EPI, VAN = (101.894, 60.886), (102.28, 60.34)\n', 'EPI, VAN = (101.894, 60.886), (102.28, 60.34)\n' + views)
new = open("_specs_33_36.txt", encoding="utf-8").read()
s, n = re.subn(r' "33": dict\(folder="33_flight_19", slug="flight19", beats=\[\]\),\n.*?"36": dict\(folder="36_kentucky_meat_shower", slug="meatshower", beats=\[\]\),\n',
               lambda m: new, s, flags=re.S)
print("replaced", n)
s = s.replace('fix={"should": "Shud.", "should.": "Shud.", "tamam": "Tamám", "Tamam": "Tamám"},',
              'fix={"should": "Shud.", "should.": "Shud.", "tamam": "Tamám", "Tamam": "Tamám"}, fix2={("has", "ended"): "is"},')
s = s.replace('fix={"20-20": "2020"},', 'fix={"20-20": "2020", "million.": "million"},')
open(p, "w", encoding="utf-8").write(s)
sys.path.insert(0, "."); import specs; print({k: len(v["beats"]) for k, v in specs.S.items()})
