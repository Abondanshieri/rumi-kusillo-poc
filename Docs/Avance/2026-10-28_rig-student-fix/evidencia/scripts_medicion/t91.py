from exp import *
ALLR={}
for tag,al,pole in (("rigOFF",0.0,"location"),("rigON_dir",1.0,"direction"),("rigON_loc",1.0,"location")):
    ALLR[tag]=run_cfg(tag,al,pole)
    json.dump(ALLR,open("meas_cfg.json","w"))
print("FIN",flush=True)
