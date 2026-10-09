import json
last=None
for line in open('/root/.claude/projects/-home-user-milenkovicdarko/36dbfb1e-5ae8-5c5c-84cb-089beb7f3444.jsonl'):
    try: o=json.loads(line)
    except: continue
    m=o.get('message',{})
    if o.get('type')!='assistant': continue
    for c in m.get('content',[]) if isinstance(m.get('content'),list) else []:
        if c.get('type')=='tool_use' and 'KIT_BM_KINDS equ' in c.get('input',{}).get('command',''):
            last=c['input']['command']
cmd=last
body=cmd.split("<<'E'\n",1)[1].rsplit("\nE\n",1)[0]
body=body.replace('''rep("""        inc si
        cmp si, 3
        jb .class
        pop si
        pop ax
        ret

; LV_ASK:""","""        inc si
        cmp si, 3
        jb .class
        or cl, cl''','''rep("""        cmp si, 3
        jb .class
        pop si
        pop ax
        ret

; LV_ASK:""","""        cmp si, 3
        jb .class
        or cl, cl''')
open('bm_patch.py','w').write(body)