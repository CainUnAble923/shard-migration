from render import *
from PIL import Image
import json
c=json.load(open('cands_strict.json'))
labels=['A','A2','E1','C','E2','E3','E4','D','E5','E6']
boxes=[(a,b,cc,d,(0,255,0),labels[i]) for i,(a,b,cc,d) in enumerate(c)]
boxes.append((6144,3072,7167,3583,(255,0,255),'114vs117 changed'))
render(5120,0,7168,4096,'overview_candidates_full.png',scale=1,boxes=boxes,grid=256)
im=Image.open('overview_candidates_full.png'); im.resize((1024,2048),Image.BOX).save('overview_candidates.png')
render(5090,1000,5420,1300,'cand_A_strict.png',scale=3,boxes=boxes,grid=25)
render(6100,1500,6900,2400,'cand_C_D_strict.png',scale=1,boxes=boxes,grid=100)
