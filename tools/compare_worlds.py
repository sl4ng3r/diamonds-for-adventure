#!/usr/bin/env python3
"""Isolated, destructive-only-in-new-world vanilla/add-on ore count experiment."""
import argparse
import json
import queue
import re
import shutil
import subprocess
import threading
import tempfile
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK_ID = '45411e2e-ecf2-4a3c-a00f-a20d4a27dbe2'

def enable_research_pack(packs):
    if any(item.get('pack_id') == PACK_ID for item in packs): return packs
    return [{'pack_id':PACK_ID,'version':[0,1,0]}] + packs

def eula_accepted(path):
    if not path.is_file():
        return False
    values = [line.split('=', 1)[1].strip() for line in path.read_text().splitlines()
              if line.strip().startswith('EULA=')]
    return len(values) == 1 and values[0] == 'TRUE'

def preload_columns(start, count, direction):
    columns = list(range(start, start + count))
    return columns if direction == 'east' else list(reversed(columns))

def marker_positions(chunk_x, chunk_z, count):
    return [((chunk_x+x)*16,300,(chunk_z+z)*16) for x in range(count) for z in range(count)]

def choose_mining_probe(ores):
    return next((ore for ore in ores if ore['exposed']), ores[0] if ores else None)

def parse_filled(line):
    m = re.search(r'\b(\d+) blocks? filled\b', line)
    return int(m.group(1)) if m else None

def parse_scan(line):
    marker='CAVEDIAMONDS_SCAN '
    if marker not in line: return None
    return json.loads(line.split(marker,1)[1].strip())

def create_full_removal_variant(source, destination, ignore_exposure=False, mark_origins=False, mark_grid=False, mark_underground=False):
    # Disposable research-only copy: eliminate randomness to expose skipped ores.
    shutil.copytree(source, destination)
    for name, host in [('thin_diamond', 'minecraft:stone'), ('thin_deepslate', 'minecraft:deepslate')]:
        path = destination / 'features' / (name + '.json')
        data = json.loads(path.read_text())
        data['minecraft:single_block_feature']['places_block'] = host
        if ignore_exposure: data['minecraft:single_block_feature'].pop('may_not_attach_to', None)
        path.write_text(json.dumps(data, indent=2) + '\n')
    if mark_origins or mark_grid or mark_underground:
        def write(name, kind, body):
            path = destination / 'features' / (name + '.json')
            path.write_text(json.dumps({'format_version':'1.21.40', kind:body},indent=2)+'\n')
        write('origin_marker', 'minecraft:single_block_feature', {'description':{'identifier':'cavediamonds:origin_marker'},'places_block':'minecraft:gold_block','may_replace':['minecraft:air'],'enforce_placement_rules':False,'enforce_survivability_rules':False})
    if mark_origins:
        write('shift_marker', 'minecraft:scatter_feature', {'description':{'identifier':'cavediamonds:shift_marker'},'places_feature':'cavediamonds:origin_marker','distribution':{'iterations':1,'x':0,'y':364,'z':0}})
        write('scan_with_marker', 'minecraft:aggregate_feature', {'description':{'identifier':'cavediamonds:scan_with_marker'},'features':['cavediamonds:scan_chunk','cavediamonds:shift_marker'],'early_out':'none'})
        rule_path = destination / 'feature_rules' / 'thin_overworld.json'
        rule = json.loads(rule_path.read_text())
        rule['minecraft:feature_rules']['description']['places_feature'] = 'cavediamonds:scan_with_marker'
        rule_path.write_text(json.dumps(rule,indent=2)+'\n')
    if mark_grid or mark_underground:
        if mark_underground:
            marker_path=destination/'features/origin_marker.json'
            marker=json.loads(marker_path.read_text())
            marker['minecraft:single_block_feature']['may_replace']=['minecraft:stone','minecraft:deepslate']
            marker_path.write_text(json.dumps(marker,indent=2)+'\n')
        scan_path=destination/'features/scan_chunk.json'
        scan=json.loads(scan_path.read_text())
        scan['minecraft:scatter_feature']['places_feature']='cavediamonds:origin_marker'
        scan_path.write_text(json.dumps(scan,indent=2)+'\n')
        rule_path=destination/'feature_rules/thin_overworld.json'
        rule=json.loads(rule_path.read_text())
        rule['minecraft:feature_rules']['distribution']['y']= -64 if mark_underground else 220
        rule_path.write_text(json.dumps(rule,indent=2)+'\n')
    return destination

def create_vanilla_override_variant(source, destination):
    # Research-only: disable our rule and replace identified vanilla features.
    shutil.copytree(source, destination)
    (destination/'feature_rules/thin_overworld.json').unlink()
    for name in ('diamond_ore_feature', 'diamond_ore_large_feature', 'diamond_ore_buried_feature'):
        doc={'format_version':'1.20.30','minecraft:ore_feature':{
            'description':{'identifier':'minecraft:'+name}, 'count':1,
            'replace_rules':[{'places_block':'minecraft:stone','may_replace':['minecraft:stone']},
                             {'places_block':'minecraft:deepslate','may_replace':['minecraft:deepslate']}]}}
        (destination/'features'/(name+'.json')).write_text(json.dumps(doc,indent=2)+'\n')
    return destination

def create_cave_generation_variant(source, destination, directional=False):
    # Research-only: suppress vanilla ore and introduce ore adjacent to cave air.
    create_vanilla_override_variant(source,destination)
    neighbours=['minecraft:air','minecraft:water','minecraft:flowing_water','minecraft:lava','minecraft:flowing_lava']
    for name, host, ore in [('cave_diamond','minecraft:stone','minecraft:diamond_ore'),('cave_deepslate','minecraft:deepslate','minecraft:deepslate_diamond_ore')]:
        body={'description':{'identifier':'cavediamonds:'+name},'places_block':ore,'may_replace':[host],
              'may_attach_to':{'min_sides_must_attach':1,'all':neighbours},
              'enforce_placement_rules':False,'enforce_survivability_rules':False}
        (destination/'features'/(name+'.json')).write_text(json.dumps({'format_version':'1.21.40','minecraft:single_block_feature':body},indent=2)+'\n')
    selected=['cavediamonds:cave_diamond','cavediamonds:cave_deepslate']
    if directional:
        selected=[]
        for base in ('cave_diamond','cave_deepslate'):
            original=json.loads((destination/'features'/(base+'.json')).read_text())
            for face in ('north','south','east','west','top','bottom'):
                name=base+'_'+face
                doc=json.loads(json.dumps(original))
                obj=doc['minecraft:single_block_feature']
                obj['description']['identifier']='cavediamonds:'+name
                obj['may_attach_to']={'min_sides_must_attach':1,face:neighbours}
                (destination/'features'/(name+'.json')).write_text(json.dumps(doc,indent=2)+'\n')
                selected.append('cavediamonds:'+name)
    aggregate={'format_version':'1.21.40','minecraft:aggregate_feature':{'description':{'identifier':'cavediamonds:cave_select'},'features':selected,'early_out':'first_success'}}
    (destination/'features/cave_select.json').write_text(json.dumps(aggregate,indent=2)+'\n')
    rule={'format_version':'1.21.40','minecraft:feature_rules':{
        'description':{'identifier':'cavediamonds:cave_rule','places_feature':'cavediamonds:cave_select'},
        'conditions':{'placement_pass':'final_pass','minecraft:biome_filter':{'any_of':[{'test':'has_biome_tag','operator':'==','value':'overworld'},{'test':'has_biome_tag','operator':'==','value':'overworld_generation'}]}},
        'distribution':{'iterations':300,'x':{'distribution':'uniform','extent':[0,15]},'y':{'distribution':'uniform','extent':[-64,16]},'z':{'distribution':'uniform','extent':[0,15]}}}}
    (destination/'feature_rules/cave_rule.json').write_text(json.dumps(rule,indent=2)+'\n')
    return destination

def create_snap_cave_variant(source, destination):
    # Research-only: use natural cavity floor/ceiling instead of adjacency filters.
    create_cave_generation_variant(source,destination)
    for base in ('cave_diamond','cave_deepslate'):
        path=destination/'features'/(base+'.json')
        doc=json.loads(path.read_text())
        doc['minecraft:single_block_feature'].pop('may_attach_to',None)
        path.write_text(json.dumps(doc,indent=2)+'\n')
    for face in ('floor','ceiling'):
        body={'description':{'identifier':'cavediamonds:cave_snap_'+face},'feature_to_snap':'cavediamonds:cave_select',
              'surface':face,'search_range':12,'embed_in_surface':True,'allow_air_placement':True,
              'allow_non_air_placement':False,'allow_underwater_placement':True,
              'allowed_surface_blocks':['minecraft:stone','minecraft:deepslate']}
        (destination/'features'/('cave_snap_'+face+'.json')).write_text(json.dumps({'format_version':'1.26.50','minecraft:snap_to_surface_feature':body},indent=2)+'\n')
    selector={'format_version':'1.21.40','minecraft:aggregate_feature':{'description':{'identifier':'cavediamonds:cave_snap_select'},'features':['cavediamonds:cave_snap_floor','cavediamonds:cave_snap_ceiling'],'early_out':'first_success'}}
    (destination/'features/cave_snap_select.json').write_text(json.dumps(selector,indent=2)+'\n')
    path=destination/'feature_rules/cave_rule.json'; rule=json.loads(path.read_text())
    rule['minecraft:feature_rules']['description']['places_feature']='cavediamonds:cave_snap_select'
    rule['minecraft:feature_rules']['distribution']['iterations']=100
    path.write_text(json.dumps(rule,indent=2)+'\n')
    return destination

def create_buried_generation_variant(source, destination):
    # Research-only: disable vanilla diamonds and generate a sparse buried sample.
    create_vanilla_override_variant(source,destination)
    feature={'format_version':'1.20.30','minecraft:ore_feature':{
        'description':{'identifier':'cavediamonds:sparse_buried'},'count':4,'discard_chance_on_air_exposure':1.0,
        'replace_rules':[{'places_block':'minecraft:diamond_ore','may_replace':['minecraft:stone']},
                         {'places_block':'minecraft:deepslate_diamond_ore','may_replace':['minecraft:deepslate']}]}}
    (destination/'features/sparse_buried.json').write_text(json.dumps(feature,indent=2)+'\n')
    rule={'format_version':'1.21.40','minecraft:feature_rules':{
        'description':{'identifier':'cavediamonds:sparse_buried_rule','places_feature':'cavediamonds:sparse_buried'},
        'conditions':{'placement_pass':'underground_pass','minecraft:biome_filter':{'any_of':[{'test':'has_biome_tag','operator':'==','value':'overworld'},{'test':'has_biome_tag','operator':'==','value':'overworld_generation'}]}},
        'distribution':{'iterations':1,'x':{'distribution':'uniform','extent':[0,15]},'y':{'distribution':'uniform','extent':[-64,16]},'z':{'distribution':'uniform','extent':[0,15]}}}}
    (destination/'feature_rules/sparse_buried_rule.json').write_text(json.dumps(rule,indent=2)+'\n')
    return destination

def create_combined_generation_variant(source, destination):
    # Research-only combination of independently verified features.
    create_snap_cave_variant(source,destination)
    with tempfile.TemporaryDirectory(prefix='cavediamonds-buried-') as directory:
        buried=create_buried_generation_variant(source,Path(directory)/'pack')
        for relative in ('features/sparse_buried.json','feature_rules/sparse_buried_rule.json'):
            shutil.copy2(buried/relative,destination/relative)
    return destination

def set_cave_pass(pack, placement_pass):
    path=pack/'feature_rules/cave_rule.json'
    rule=json.loads(path.read_text())
    rule['minecraft:feature_rules']['conditions']['placement_pass']=placement_pass
    path.write_text(json.dumps(rule,indent=2)+'\n')

def set_snap_selection(pack, selection):
    rule_path=pack/'feature_rules/cave_rule.json'
    rule=json.loads(rule_path.read_text())
    if selection in ('floor','ceiling'):
        rule['minecraft:feature_rules']['description']['places_feature']='cavediamonds:cave_snap_'+selection
        rule_path.write_text(json.dumps(rule,indent=2)+'\n')
    elif selection == 'both':
        path=pack/'features/cave_snap_select.json'
        doc=json.loads(path.read_text())
        doc['minecraft:aggregate_feature']['early_out']='none'
        path.write_text(json.dumps(doc,indent=2)+'\n')
    else:
        raise ValueError('invalid snap selection')

def set_cave_fixed_grid(pack):
    path=pack/'feature_rules/cave_rule.json'
    rule=json.loads(path.read_text())
    rule['minecraft:feature_rules']['distribution']={
        'iterations':176, 'coordinate_eval_order':'xzy',
        'x':{'distribution':'fixed_grid','extent':[0,15],'step_size':4},
        'y':{'distribution':'fixed_grid','extent':[-64,16],'step_size':8},
        'z':{'distribution':'fixed_grid','extent':[0,15],'step_size':4}}
    path.write_text(json.dumps(rule,indent=2)+'\n')

def count_tunnel_finds(ores, width, y, origin_x=0, origin_z=0):
    # A two-block-high, x-directed tunnel; excludes boundary corridors so side
    # faces lie inside the measured area. Does not model digging into veins.
    found = {z: 0 for z in range(origin_z+1, origin_z+width-1)}
    for ore in ores:
        x, oy, oz = ore['x'], ore['y'], ore['z']
        if not origin_x <= x < origin_x+width: continue
        if oy in (y, y+1):
            candidates = (oz-1, oz, oz+1)
        elif oy in (y-1, y+2):
            candidates = (oz,)
        else:
            continue
        for z in candidates:
            if z in found: found[z] += 1
    return found

def compare_scans(baseline, treated):
    def positions(scan):
        result = {}
        for ore in scan['ores']:
            position = (ore['x'], ore['y'], ore['z'])
            if position in result: raise ValueError('duplicate ore position')
            result[position] = ore
        return result
    before = positions(baseline)
    after = positions(treated)
    exposed = {p for p, o in before.items() if o['exposed']}
    buried = set(before) - exposed
    remaining = set(after)
    return {
        'baseline_total':len(before), 'treated_total':len(after),
        'baseline_exposed':len(exposed), 'exposed_preserved':len(exposed & remaining),
        'baseline_buried':len(buried), 'buried_removed':len(buried - remaining),
        'new_coordinates':len(remaining - set(before)),
    }

def compare_restart(before, after):
    def positions(scan):
        result = {}
        for ore in scan['ores']:
            position = (ore['x'], ore['y'], ore['z'])
            if position in result: raise ValueError('duplicate ore position')
            result[position] = (ore['type'], ore['exposed'])
        return result
    first, second = positions(before), positions(after)
    return {'removed':len(first.keys()-second.keys()), 'added':len(second.keys()-first.keys()),
            'changed':sum(first[p] != second[p] for p in first.keys() & second.keys())}

def update_properties(text, values):
    for key, value in values.items():
        line = f'{key}={value}'
        text, count = re.subn(rf'(?m)^{re.escape(key)}=.*$', lambda _: line, text)
        if not count:
            text += '\n' + line + '\n'
    return text

def run(seed, addon, chunks, diagnose=False, reapply=False, pack_path=None, mark_grid=False, mark_underground=False, probe_cave=False, cave_directional=False, chunk_x=0, chunk_z=0, restart_world=None, air_probe=False, preload_direction=None, watch_block=None, settle_seconds=15, locate_biome=None, surface_probe=False, stability_delay=0, mark_saved_chunks=False, mine_one=False, fingerprint=False, ore_trace=False, height_probe=False, probe_snap=False):
    name = f'cavediamonds-research-{uuid.uuid4().hex[:10]}'
    data = ROOT / 'data' / 'research' / name if restart_world is None else Path(restart_world).resolve()
    world = data / 'worlds' / 'PrototypeTest'
    if restart_world is None:
        world.mkdir(parents=True, exist_ok=False)
        config = update_properties((ROOT / 'data/server.properties').read_text(), {
            'level-seed': str(seed), 'level-name':'PrototypeTest', 'online-mode':'true',
            'allow-list':'true', 'allow-cheats':'true', 'view-distance':'10', 'tick-distance':'4',
            'content-log-console-output-enabled':'true', 'content-log-file-enabled':'true',
        })
        (data / 'server.properties').write_text(config)
        packs = ([{'pack_id':PACK_ID,'version':[0,1,0]}] if addon else [])
        if diagnose: packs.append({'pack_id':'404597db-6431-4765-8966-b69ee41c377c','version':[0,1,0]})
        (world / 'world_behavior_packs.json').write_text(json.dumps(packs))
    elif data.parent != (ROOT/'data/research').resolve() or not (data/'ore_scan.json').is_file() or not world.is_dir():
        raise ValueError('restart only permitted for an existing diagnostic research world')
    cmd = ['docker','run','--rm','-i','--name',name,'--platform','linux/amd64','-e','EULA=TRUE','-v',f'{data}:/data']
    if addon:
        cmd += ['-v',f'{pack_path or ROOT / "prototype/behavior_pack"}:/server/behavior_packs/cavediamonds:ro']
    if diagnose: cmd += ['-v',f'{ROOT / "diagnostics/behavior_pack"}:/server/behavior_packs/cavediamonds_diagnostic:ro']
    cmd += ['minceaftplugin-bedrock-test']
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    lines = queue.Queue()
    captured = []
    def reader():
        for line in proc.stdout:
            captured.append(line)
            lines.put(line)
    threading.Thread(target=reader, daemon=True).start()
    def waitfor(predicate, timeout):
        deadline = time.monotonic()+timeout
        while time.monotonic() < deadline:
            try: line=lines.get(timeout=min(1,max(0.01,deadline-time.monotonic())))
            except queue.Empty:
                if proc.poll() is not None: raise RuntimeError('Server terminated')
                continue
            if predicate(line): return line
        raise TimeoutError('No expected server response')
    def send(command):
        proc.stdin.write(command+'\n'); proc.stdin.flush()
    try:
        waitfor(lambda s:'Server started.' in s,180)
        if addon and not any(PACK_ID in x and 'Pack Stack' in x for x in captured):
            raise RuntimeError('Behavior pack missing from pack stack')
        if not addon and any(PACK_ID in x and 'Pack Stack' in x for x in captured):
            raise RuntimeError('Unexpected addon in baseline')
        if locate_biome:
            send(f'scriptevent cavediamondstest:locate {locate_biome}')
            found=waitfor(lambda s:'CAVEDIAMONDS_LOCATE ' in s or 'CAVEDIAMONDS_LOCATE_ERROR ' in s,90)
            print(found.strip(),flush=True)
        if restart_world is None:
            if preload_direction:
                for index, column in enumerate(preload_columns(chunk_x, chunks, preload_direction)):
                    send(f'tickingarea add {column*16} -64 {chunk_z*16} {column*16+15} 16 {(chunk_z+chunks)*16-1} route{index} true')
                    waitfor(lambda s:'Added ticking area' in s,30)
                    time.sleep(8)
            send(f'tickingarea add {chunk_x*16-16} -64 {chunk_z*16-16} {(chunk_x+chunks)*16+15} 16 {(chunk_z+chunks)*16+15} sample true')
            waitfor(lambda s:'Added ticking area' in s,30)
        # Allow the preloading area to generate; fill commands additionally reject unloaded locations.
        time.sleep(settle_seconds)
        if addon and probe_snap:
            # A hollow box in the disposable world. Examine only the selected face,
            # not a nearby ore created by the optional neighboring-block feature.
            probes=[]
            faces={'floor':['2 -23 2 6 -23 6'], 'ceiling':['2 -17 2 6 -17 6'],
                   'wall':['1 -22 2 1 -18 6','7 -22 2 7 -18 6','2 -22 1 6 -18 1','2 -22 7 6 -18 7']}
            for surface in ('floor','ceiling','wall'):
                for trial in range(3):
                    for command in ('fill 1 -23 1 7 -17 7 stone','fill 2 -22 2 6 -18 6 air'):
                        send(command)
                        waitfor(lambda line:parse_filled(line) is not None,30)
                    send(f'place feature cavediamonds:cave_snap_{surface} 4 -20 4')
                    placement=waitfor(lambda line:'Place command succeeded.' in line or 'Feature could not be placed at this location.' in line,30)
                    found=0
                    for box in faces[surface]:
                        send(f'fill {box} gold_block replace diamond_ore')
                        found+=parse_filled(waitfor(lambda line:parse_filled(line) is not None,30))
                    probes.append({'surface':surface,'trial':trial,'placed':'Place command succeeded.' in placement,'ore_on_face':found})
            (data/'snap_probes.json').write_text(json.dumps(probes,indent=2)+'\n')
            print('SNAP_PROBES '+json.dumps(probes),flush=True)
        if addon and probe_cave:
            results=[]
            directions=[(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]
            for host,feature in [('stone','cave_diamond'),('deepslate','cave_deepslate')]:
                for dx,dy,dz in directions:
                    send(f'fill 0 120 0 4 124 4 {host}')
                    send(f'setblock {2+dx} {122+dy} {2+dz} air')
                    face={(-1,0,0):'west',(1,0,0):'east',(0,-1,0):'bottom',(0,1,0):'top',(0,0,-1):'north',(0,0,1):'south'}[(dx,dy,dz)]
                    chosen=feature+'_'+face if cave_directional else feature
                    send(f'place feature cavediamonds:{chosen} 2 122 2')
                    response=waitfor(lambda line:'Place command succeeded.' in line or 'Feature could not be placed at this location.' in line,30)
                    results.append({'host':host,'direction':[dx,dy,dz],'placed':'Place command succeeded.' in response})
            if cave_directional:
                for host,feature in [('stone','cave_diamond_north'),('deepslate','cave_deepslate_north')]:
                    send(f'fill 0 120 0 4 124 4 {host}')
                    send(f'place feature cavediamonds:{feature} 2 122 2')
                    response=waitfor(lambda line:'Place command succeeded.' in line or 'Feature could not be placed at this location.' in line,30)
                    results.append({'host':host,'direction':'no_exposure','placed':'Place command succeeded.' in response})
            print('CAVE_PROBES '+json.dumps(results),flush=True)
            (data/'cave_probes.json').write_text(json.dumps(results,indent=2)+'\n')
        if diagnose:
            send(f'scriptevent cavediamondstest:scan {chunks}:' + ('GRID' if mark_grid else 'GROUND' if mark_underground else 'AIR' if air_probe else 'SURFACE' if surface_probe else 'FINGERPRINT' if fingerprint else 'TRACE' if ore_trace else 'HEIGHT' if height_probe else 'NORMAL') + f':{chunk_x*16}:{chunk_z*16}')
            line=waitfor(lambda s: 'CAVEDIAMONDS_SCAN ' in s or 'CAVEDIAMONDS_SCAN_ERROR ' in s,240)
            if 'CAVEDIAMONDS_SCAN_ERROR ' in line: raise RuntimeError(line.strip())
            result=parse_scan(line)
            (data/('ore_scan_after_restart.json' if restart_world is not None else 'ore_scan.json')).write_text(json.dumps(result,indent=2)+'\n')
            if watch_block:
                send('scriptevent cavediamondstest:block '+watch_block.replace(',',':'))
                block_line=waitfor(lambda s:'CAVEDIAMONDS_BLOCK ' in s or 'CAVEDIAMONDS_BLOCK_ERROR ' in s,30)
                if 'CAVEDIAMONDS_BLOCK_ERROR ' in block_line: raise RuntimeError(block_line.strip())
                print(('RESTART_BLOCK ' if restart_world else 'WATCH_BLOCK ')+block_line.split('CAVEDIAMONDS_BLOCK ',1)[1].strip(),flush=True)
            if addon and stability_delay and restart_world is None:
                time.sleep(stability_delay)
                send(f'scriptevent cavediamondstest:scan {chunks}:NORMAL:{chunk_x*16}:{chunk_z*16}')
                later_line=waitfor(lambda s: 'CAVEDIAMONDS_SCAN ' in s or 'CAVEDIAMONDS_SCAN_ERROR ' in s,240)
                if 'CAVEDIAMONDS_SCAN_ERROR ' in later_line: raise RuntimeError(later_line.strip())
                later=parse_scan(later_line)
                (data/'ore_scan_later.json').write_text(json.dumps(later,indent=2)+'\n')
                print('BEFORE_RESTART_STABILITY '+json.dumps(compare_restart(result,later)),flush=True)
            if mark_saved_chunks and restart_world is None:
                for x,y,z in marker_positions(chunk_x,chunk_z,chunks):
                    send(f'setblock {x} {y} {z} gold_block')
                    marker_line=waitfor(lambda s:'Block placed' in s or 'Could not set the block' in s,30)
                    if 'Block placed' not in marker_line: raise RuntimeError('chunk marker failed: '+marker_line.strip())
            if addon and mine_one and restart_world is None:
                selected=choose_mining_probe(result['ores'])
                if selected is None: raise RuntimeError('no ore for mining probe')
                send(f"setblock {selected['x']} {selected['y']} {selected['z']} air")
                answer=waitfor(lambda s:'Block placed' in s or 'Could not set the block' in s,30)
                if 'Block placed' not in answer: raise RuntimeError('mining probe failed: '+answer.strip())
                (data/'simulated_mine.json').write_text(json.dumps(selected,indent=2)+'\n')
                print('SIMULATED_MINE '+json.dumps(selected),flush=True)
            ores=result['ores']
            if mark_grid or mark_underground: print('GRID '+json.dumps({'addon':addon,'grid':result.get('grid')}),flush=True)
            summary={'seed':seed,'addon':addon,'chunks':chunks*chunks,'total':len(ores),'exposed':sum(o['exposed'] for o in ores),'buried':sum(not o['exposed'] for o in ores),'world':str(data)}
            if addon and reapply:
                for x in range(chunks):
                    for z in range(chunks):
                        send(f'place feature cavediamonds:scan_chunk {(chunk_x+x)*16} -64 {(chunk_z+z)*16}')
                        waitfor(lambda s:'Place command succeeded.' in s or 'Feature could not be placed at this location.' in s,40)
                send(f'scriptevent cavediamondstest:scan {chunks}:' + ('GRID' if mark_grid else 'GROUND' if mark_underground else 'NORMAL') + f':{chunk_x*16}:{chunk_z*16}')
                line=waitfor(lambda s: 'CAVEDIAMONDS_SCAN ' in s or 'CAVEDIAMONDS_SCAN_ERROR ' in s,240)
                if 'CAVEDIAMONDS_SCAN_ERROR ' in line: raise RuntimeError(line.strip())
                after=parse_scan(line)
                (data/'ore_scan_after_reapply.json').write_text(json.dumps(after,indent=2)+'\n')
                summary['reapply']=compare_scans(result,after)
            return summary
        counts={}
        for ore in ('diamond_ore','deepslate_diamond_ore'):
            total=0
            for x in range(chunks):
                for z in range(chunks):
                    send(f'fill {(chunk_x+x)*16} -64 {(chunk_z+z)*16} {(chunk_x+x)*16+15} 16 {(chunk_z+z)*16+15} gold_block replace {ore}')
                    line=waitfor(lambda s: parse_filled(s) is not None or any(t in s.lower() for t in ('cannot place blocks outside','outside of the world','not loaded')),40)
                    value=parse_filled(line)
                    if value is None: raise RuntimeError('fill error: '+line.strip())
                    total+=value
            counts[ore]=total
        return {'seed':seed,'addon':addon,'chunks':chunks*chunks,'counts':counts,'world':str(data)}
    finally:
        try:
            send('stop')
            proc.wait(timeout=40)
        except Exception:
            subprocess.run(['docker','stop','-t','5',name], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, timeout=15)
        (data / ('server_after_restart.log' if restart_world is not None else 'server.log')).write_text(''.join(captured))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--diagnose', action='store_true')
    parser.add_argument('--restart-check', action='store_true', help='test-only: restart the new add-on world and compare ore snapshots')
    parser.add_argument('--restart-control', action='store_true', help='test-only: additionally restart the vanilla comparison world')
    parser.add_argument('--activation-check', action='store_true', help='test-only: activate add-on on the previously generated vanilla research world')
    parser.add_argument('--mark-baseline-chunks', action='store_true', help='test-only: modify each baseline chunk before activation')
    parser.add_argument('--mark-saved-chunks', action='store_true', help='test-only: place a gold block above every test chunk before restart')
    parser.add_argument('--mine-one', action='store_true', help='test-only: replace one ore with air before restart (not a real mining event)')
    parser.add_argument('--air-probe', action='store_true', help='test-only: bounded air connectivity around ores')
    parser.add_argument('--fingerprint', action='store_true', help='test-only: fingerprint normalized block types per chunk')
    parser.add_argument('--preload-direction', choices=('east','west'), help='test-only: generate chunk columns in different orders')
    parser.add_argument('--watch-block', help='test-only: log a specific block as x,y,z')
    parser.add_argument('--settle-seconds', type=int, default=15, help='test-only: wait before scanning; not proof that generation is complete')
    parser.add_argument('--stability-delay', type=int, default=0, help='test-only: rescan add-on world after N seconds without restart')
    parser.add_argument('--locate-biome', help='test-only: find an approximate biome coordinate from the seed')
    parser.add_argument('--cave-pass', choices=('underground_pass','after_underground_pass','after_surface_pass','final_pass'), help='test-only: change cave generation pass in disposable copy')
    parser.add_argument('--snap-selection', choices=('floor','ceiling','both'), help='test-only: isolate cave floor and ceiling generation')
    parser.add_argument('--cave-fixed-grid', action='store_true', help='test-only: deterministic test positions for cave generation')
    parser.add_argument('--reapply', action='store_true')
    parser.add_argument('--remove-all', action='store_true', help='test-only: replace all eligible ores, without changing prototype')
    parser.add_argument('--override-vanilla', action='store_true', help='test-only: attempt to replace vanilla ore generation')
    parser.add_argument('--cave-test', action='store_true', help='test-only: suppress vanilla ore and test cave-exposed placement')
    parser.add_argument('--probe-cave', action='store_true', help='test-only: directly check cave placement on six sides')
    parser.add_argument('--cave-directional', action='store_true', help='test-only: use one feature per face')
    parser.add_argument('--buried-test', action='store_true', help='test-only: suppress vanilla ore and test sparse buried placement')
    parser.add_argument('--snap-cave', action='store_true', help='test-only: snap diamond ore to cave floors and ceilings')
    parser.add_argument('--combined-test', action='store_true', help='test-only: cave and buried generation together')
    parser.add_argument('--ignore-exposure', action='store_true', help='test-only: remove exposure filter; requires --remove-all')
    parser.add_argument('--mark-origins', action='store_true', help='test-only: put marker above each invocation')
    parser.add_argument('--mark-grid', action='store_true', help='test-only: mark scanned grid in the sky')
    parser.add_argument('--mark-underground', action='store_true', help='test-only: mark host rock')
    parser.add_argument('--chunk-x',type=int,default=0)
    parser.add_argument('--chunk-z',type=int,default=0)
    parser.add_argument('--seed',type=int,default=12345)
    parser.add_argument('--chunks',type=int,default=2,choices=range(1,5))
    args=parser.parse_args()
    if not eula_accepted(ROOT/'.env'):
        parser.error('EULA-Zustimmung fehlt: .env nach Zustimmung zu https://www.minecraft.net/eula auf EULA=TRUE setzen')
    if args.cave_directional and not args.cave_test: parser.error('--cave-directional requires --cave-test')
    if args.probe_cave and (args.chunk_x or args.chunk_z): parser.error('--probe-cave requires zero origin')
    if args.probe_cave and not args.cave_test: parser.error('--probe-cave requires --cave-test')
    if args.reapply and not args.diagnose: parser.error('--reapply requires --diagnose')
    if args.restart_check and (not args.diagnose or args.reapply or args.probe_cave): parser.error('--restart-check requires --diagnose and cannot use --reapply or --probe-cave')
    if args.restart_control and not args.restart_check: parser.error('--restart-control requires --restart-check')
    if args.activation_check and (not args.diagnose or args.restart_check or not args.combined_test): parser.error('--activation-check requires --diagnose --combined-test and no --restart-check')
    if args.mark_baseline_chunks and not args.activation_check: parser.error('--mark-baseline-chunks requires --activation-check')
    if args.mark_saved_chunks and not args.restart_check: parser.error('--mark-saved-chunks requires --restart-check')
    if args.mine_one and (not args.restart_check or args.mark_saved_chunks or args.stability_delay): parser.error('--mine-one requires --restart-check and no marker or stability-delay')
    if args.air_probe and (not args.diagnose or args.mark_grid or args.mark_underground or args.reapply): parser.error('--air-probe requires --diagnose and a normal scan')
    if args.fingerprint and (not args.diagnose or args.air_probe or args.mark_grid or args.mark_underground or args.reapply): parser.error('--fingerprint requires --diagnose and a normal scan')
    if not 0 <= args.settle_seconds <= 600: parser.error('--settle-seconds must be between 0 and 600')
    if not 0 <= args.stability_delay <= 600 or (args.stability_delay and (not args.diagnose or args.reapply)): parser.error('--stability-delay requires --diagnose, no --reapply, and a value from 0 to 600')
    if args.locate_biome and not args.diagnose: parser.error('--locate-biome requires --diagnose')
    if args.cave_pass and not (args.combined_test or args.snap_cave): parser.error('--cave-pass requires --combined-test or --snap-cave')
    if args.snap_selection and not (args.combined_test or args.snap_cave): parser.error('--snap-selection requires --combined-test or --snap-cave')
    if args.cave_fixed_grid and not (args.combined_test or args.snap_cave): parser.error('--cave-fixed-grid requires --combined-test or --snap-cave')
    if args.locate_biome and not re.fullmatch(r'[a-z0-9_:]+', args.locate_biome): parser.error('--locate-biome must be a biome identifier')
    if args.watch_block:
        try:
            if len(args.watch_block.split(',')) != 3: raise ValueError()
            [int(v) for v in args.watch_block.split(',')]
        except ValueError: parser.error('--watch-block requires x,y,z integer coordinates')
        if not args.diagnose: parser.error('--watch-block requires --diagnose')
    if (args.ignore_exposure or args.mark_origins or args.mark_grid or args.mark_underground) and not args.remove_all: parser.error('diagnostic options require --remove-all')
    if args.combined_test and (args.snap_cave or args.buried_test or args.cave_test or args.remove_all or args.override_vanilla or not args.diagnose): parser.error('--combined-test requires --diagnose and cannot be combined with other variants')
    if args.snap_cave and (args.buried_test or args.cave_test or args.remove_all or args.override_vanilla or not args.diagnose): parser.error('--snap-cave requires --diagnose and cannot be combined with other variants')
    if args.buried_test and (args.cave_test or args.remove_all or args.override_vanilla or not args.diagnose): parser.error('--buried-test requires --diagnose and cannot be combined with other variants')
    if args.cave_test and (args.remove_all or args.override_vanilla or not args.diagnose): parser.error('--cave-test requires --diagnose and cannot be combined with other variants')
    if args.override_vanilla and (args.remove_all or not args.diagnose): parser.error('--override-vanilla requires --diagnose and cannot be combined with --remove-all')
    pack_path = None
    if args.combined_test:
        pack_path = create_combined_generation_variant(ROOT/'prototype/behavior_pack', ROOT/'data/research'/('combined-'+uuid.uuid4().hex[:10]))
        print(f'Test-only combined variant: {pack_path}',flush=True)
    if args.snap_cave:
        pack_path = create_snap_cave_variant(ROOT/'prototype/behavior_pack', ROOT/'data/research'/('snap-'+uuid.uuid4().hex[:10]))
        print(f'Test-only snap variant: {pack_path}',flush=True)
    if args.buried_test:
        pack_path = create_buried_generation_variant(ROOT/'prototype/behavior_pack', ROOT/'data/research'/('buried-'+uuid.uuid4().hex[:10]))
        print(f'Test-only buried variant: {pack_path}',flush=True)
    if args.cave_test:
        pack_path = create_cave_generation_variant(ROOT/'prototype/behavior_pack', ROOT/'data/research'/('cave-'+uuid.uuid4().hex[:10]), directional=args.cave_directional)
        print(f'Test-only cave variant: {pack_path}',flush=True)
    if args.override_vanilla:
        pack_path = create_vanilla_override_variant(ROOT/'prototype/behavior_pack', ROOT/'data/research'/('override-'+uuid.uuid4().hex[:10]))
        print(f'Test-only vanilla override: {pack_path}',flush=True)
    if args.remove_all:
        if not args.diagnose: parser.error('--remove-all requires --diagnose')
        pack_path = create_full_removal_variant(ROOT/'prototype/behavior_pack', ROOT/'data/research'/('variant-'+uuid.uuid4().hex[:10]), ignore_exposure=args.ignore_exposure, mark_origins=args.mark_origins, mark_grid=args.mark_grid, mark_underground=args.mark_underground)
        print(f'Test-only variant: {pack_path}',flush=True)
    if args.cave_pass:
        set_cave_pass(pack_path,args.cave_pass)
    if args.snap_selection:
        set_snap_selection(pack_path,args.snap_selection)
    if args.cave_fixed_grid:
        set_cave_fixed_grid(pack_path)
    result=[]
    for addon in (False,True):
        print(f'Seed {args.seed}: {"Add-on" if addon else "Vanilla"} startet',flush=True)
        item=run(args.seed,addon,args.chunks,args.diagnose,args.reapply,pack_path,args.mark_grid,args.mark_underground,args.probe_cave,args.cave_directional,args.chunk_x,args.chunk_z,air_probe=args.air_probe,preload_direction=args.preload_direction,watch_block=args.watch_block,settle_seconds=args.settle_seconds,locate_biome=args.locate_biome,stability_delay=args.stability_delay,mark_saved_chunks=(args.mark_saved_chunks and addon) or (args.mark_baseline_chunks and not addon),mine_one=args.mine_one,fingerprint=args.fingerprint)
        result.append(item)
        print(json.dumps(item),flush=True)
    if args.diagnose:
        before=json.loads((Path(result[0]['world'])/'ore_scan.json').read_text())
        after=json.loads((Path(result[1]['world'])/'ore_scan.json').read_text())
        print('COMPARISON '+json.dumps(compare_scans(before,after)),flush=True)
        vanilla_tunnels = count_tunnel_finds(before['ores'], args.chunks * 16, -57, args.chunk_x*16, args.chunk_z*16)
        addon_tunnels = count_tunnel_finds(after['ores'], args.chunks * 16, -57, args.chunk_x*16, args.chunk_z*16)
        print('TUNNEL_MODEL '+json.dumps({'y':-57,'length':args.chunks*16,'corridors':len(vanilla_tunnels),'vanilla_contacts':sum(vanilla_tunnels.values()),'addon_contacts':sum(addon_tunnels.values()),'note':'overlapping hypothetical corridors; counts are contacts, not unique ores or per-hour yield'}),flush=True)
        if args.activation_check:
            baseline_path=Path(result[0]['world'])
            pack_file=baseline_path/'worlds/PrototypeTest/world_behavior_packs.json'
            previous=pack_file.read_text()
            (baseline_path/'world_behavior_packs.before_activation.json').write_text(previous)
            pack_file.write_text(json.dumps(enable_research_pack(json.loads(previous))))
            print('Activating test pack in the existing disposable baseline world',flush=True)
            run(args.seed,True,args.chunks,True,False,pack_path,chunk_x=args.chunk_x,chunk_z=args.chunk_z,restart_world=baseline_path,settle_seconds=args.settle_seconds)
            activated=json.loads((baseline_path/'ore_scan_after_restart.json').read_text())
            print('ACTIVATION '+json.dumps(compare_restart(before,activated)),flush=True)
        if args.restart_check:
            if args.restart_control:
                print('Restarting the same disposable vanilla world', flush=True)
                run(args.seed,False,args.chunks,True,False,None,False,False,False,False,args.chunk_x,args.chunk_z,restart_world=result[0]['world'],settle_seconds=args.settle_seconds,fingerprint=args.fingerprint)
                vanilla_restarted=json.loads((Path(result[0]['world'])/'ore_scan_after_restart.json').read_text())
                print('VANILLA_RESTART '+json.dumps(compare_restart(before,vanilla_restarted)),flush=True)
                if args.fingerprint:
                    print('VANILLA_FINGERPRINT_CHANGED_CHUNKS '+json.dumps([k for k in before['fingerprints'] if before['fingerprints'][k] != vanilla_restarted['fingerprints'].get(k)]),flush=True)
            print('Restarting the same disposable add-on world', flush=True)
            run(args.seed,True,args.chunks,True,False,pack_path,args.mark_grid,args.mark_underground,False,False,args.chunk_x,args.chunk_z,restart_world=result[1]['world'],watch_block=args.watch_block,settle_seconds=args.settle_seconds,fingerprint=args.fingerprint)
            restarted=json.loads((Path(result[1]['world'])/'ore_scan_after_restart.json').read_text())
            if args.fingerprint:
                print('FINGERPRINT_CHANGED_CHUNKS '+json.dumps([k for k in after['fingerprints'] if after['fingerprints'][k] != restarted['fingerprints'].get(k)]),flush=True)
            if args.mine_one:
                mined=json.loads((Path(result[1]['world'])/'simulated_mine.json').read_text())
                position=(mined['x'],mined['y'],mined['z'])
                print('SIMULATED_MINE_REAPPEARED '+json.dumps(any((o['x'],o['y'],o['z'])==position for o in restarted['ores'])),flush=True)
            restart_baseline=json.loads((Path(result[1]['world'])/'ore_scan_later.json').read_text()) if args.stability_delay else after
            print('RESTART '+json.dumps(compare_restart(restart_baseline,restarted)),flush=True)
    print('RESULT '+json.dumps(result),flush=True)
if __name__=='__main__': main()
