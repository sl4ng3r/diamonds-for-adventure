import { system, world } from '@minecraft/server';
import { probeAir } from './air_probe.js';
import { updateFingerprint, normalizeBlockType } from './block_fingerprint.js';
const protectedTypes = new Set(['minecraft:air','minecraft:water','minecraft:flowing_water','minecraft:lava','minecraft:flowing_lava']);
const directions = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]];
const tracedOres = new Set(['minecraft:iron_ore','minecraft:deepslate_redstone_ore','minecraft:deepslate_lapis_ore','minecraft:deepslate_gold_ore','minecraft:deepslate_copper_ore']);
function* scan(chunks, mode, startX, startZ) {
  try {
    const dimension = world.getDimension('overworld');
    const ores = [];
    const otherOreCounts = {};
    const oreTrace = [];
    const upperDiamondOre = [];
    const biomes = {};
    const deepDarkAirSurfaces = {};
    const fingerprints = {};
    const blockCounts = {};
    const markers = [];
    const grid = {gold:0, air:0, other:0, perChunk:{}};
    for (let x=startX; x<startX+chunks*16; x++) {
      for (let z=startZ; z<startZ+chunks*16; z++) {
        if (x % 4 === 0 && z % 4 === 0) {
          for (const y of [-57, -32, 0, 64]) {
            const id = dimension.getBiome({x,y,z}).id;
            biomes[y] ??= {};
            biomes[y][id] = (biomes[y][id] ?? 0) + 1;
          }
        }
        const marker = dimension.getBlock({x,y:300,z});
        if (!marker) throw new Error(`unloaded marker ${x},300,${z}`);
        if (marker.typeId === 'minecraft:gold_block') markers.push({x,y:300,z});
        if (mode === 'GRID') {
          const key = `${Math.floor(x/16)},${Math.floor(z/16)}`;
          grid.perChunk[key] ??= {gold:0, air:0, other:0};
          for (let y=220; y<=300; y++) {
            const b=dimension.getBlock({x,y,z});
            if (!b) throw new Error(`unloaded grid ${x},${y},${z}`);
            const k=b.typeId === 'minecraft:gold_block' ? 'gold' : b.typeId === 'minecraft:air' ? 'air' : 'other';
            grid[k]++; grid.perChunk[key][k]++;
          }
        }
        for (let y=-64; y<=16; y++) {
          const block = dimension.getBlock({x,y,z});
          if (!block) throw new Error(`unloaded position ${x},${y},${z}`);
          if (mode === 'FINGERPRINT') {
            const key=`${Math.floor(x/16)},${Math.floor(z/16)}`;
            fingerprints[key]=updateFingerprint(fingerprints[key] ?? 2166136261,block.typeId);
            const normalized=normalizeBlockType(block.typeId);
            blockCounts[key] ??= {};
            blockCounts[key][normalized]=(blockCounts[key][normalized] ?? 0)+1;
          }
          if (mode === 'SURFACE' && block.typeId === 'minecraft:air' && dimension.getBiome({x,y,z}).id === 'minecraft:deep_dark') {
            for (const [dx,dy,dz] of directions) {
              const other=dimension.getBlock({x:x+dx,y:y+dy,z:z+dz});
              if (!other) throw new Error('unloaded surface neighbour');
              if (other.typeId !== 'minecraft:air') deepDarkAirSurfaces[other.typeId]=(deepDarkAirSurfaces[other.typeId] ?? 0)+1;
            }
          }
          if (mode === 'GROUND') {
            const key = `${Math.floor(x/16)},${Math.floor(z/16)}`;
            grid.perChunk[key] ??= {gold:0, air:0, other:0};
            const k=block.typeId === 'minecraft:gold_block' ? 'gold' : (block.typeId === 'minecraft:stone' || block.typeId === 'minecraft:deepslate') ? 'air' : 'other';
            grid[k]++; grid.perChunk[key][k]++;
          }
          if (block.typeId !== 'minecraft:diamond_ore' && block.typeId !== 'minecraft:deepslate_diamond_ore') {
            if (block.typeId.endsWith('_ore')) otherOreCounts[block.typeId] = (otherOreCounts[block.typeId] ?? 0) + 1;
            if (mode === 'TRACE' && tracedOres.has(block.typeId)) oreTrace.push([x,y,z,block.typeId]);
            continue;
          }
          const neighbours = directions.map(([dx,dy,dz]) => {
            const neighbour = dimension.getBlock({x:x+dx,y:y+dy,z:z+dz});
            if (!neighbour) throw new Error(`unloaded neighbour ${x+dx},${y+dy},${z+dz}`);
            return neighbour.typeId;
          });
          ores.push({x,y,z,type:block.typeId,biome:dimension.getBiome({x,y,z}).id,exposed:neighbours.some(type=>protectedTypes.has(type)),neighbours});
        }
        if (mode === 'HEIGHT') {
          for (let y=17; y<=40; y++) {
            const b=dimension.getBlock({x,y,z});
            if (!b) throw new Error(`unloaded upper position ${x},${y},${z}`);
            if (b.typeId === 'minecraft:diamond_ore' || b.typeId === 'minecraft:deepslate_diamond_ore') upperDiamondOre.push({x,y,z,type:b.typeId});
          }
        }
        yield;
      }
    }
    if (mode === 'AIR') {
      const bounds={minX:startX,maxX:startX+chunks*16-1,minY:-64,maxY:16,minZ:startZ,maxZ:startZ+chunks*16-1};
      const getType=p => { const b=dimension.getBlock(p); if (!b) throw new Error(`unloaded air probe ${p.x},${p.y},${p.z}`); return b.typeId; };
      for (const ore of ores) {
        let result={status:'none',count:0};
        for (let i=0; i<directions.length; i++) {
          if (ore.neighbours[i] !== 'minecraft:air') continue;
          const [dx,dy,dz]=directions[i];
          const next=probeAir({x:ore.x+dx,y:ore.y+dy,z:ore.z+dz},getType,bounds);
          if (next.status==='large' || (next.status==='boundary' && result.status!=='large') || (next.status==='small' && result.status==='none')) result=next;
          if (result.status==='large') break;
        }
        ore.airProbe=result;
        yield;
      }
    }
    console.warn('CAVEDIAMONDS_SCAN '+JSON.stringify({chunks,ores,markers,grid,otherOreCounts,biomes,deepDarkAirSurfaces,fingerprints,blockCounts,oreTrace,...(mode === 'HEIGHT' ? {upperDiamondOre} : {})}));
  } catch (error) { console.warn('CAVEDIAMONDS_SCAN_ERROR '+String(error)); }
}
system.afterEvents.scriptEventReceive.subscribe(event => {
  if (event.id === 'cavediamondstest:locate') {
    try {
      const biome=event.message.trim();
      const position=world.getDimension('overworld').calculateClosestBiomeFromSeed({x:0,y:-32,z:0},biome);
      console.warn('CAVEDIAMONDS_LOCATE '+JSON.stringify({biome,position:position ?? null}));
    } catch (error) { console.warn('CAVEDIAMONDS_LOCATE_ERROR '+String(error)); }
    return;
  }
  if (event.id === 'cavediamondstest:block') {
    try {
      const [x,y,z]=event.message.split(':').map(Number);
      if (![x,y,z].every(Number.isInteger)) throw new Error('invalid coordinates');
      const block=world.getDimension('overworld').getBlock({x,y,z});
      if (!block) throw new Error('unloaded');
      console.warn('CAVEDIAMONDS_BLOCK '+JSON.stringify({x,y,z,type:block.typeId}));
    } catch (error) { console.warn('CAVEDIAMONDS_BLOCK_ERROR '+String(error)); }
    return;
  }
  if (event.id !== 'cavediamondstest:scan') return;
  const [size, mode, startXText='0', startZText='0'] = event.message.split(':');
  const startX=Number(startXText), startZ=Number(startZText);
  if (!Number.isInteger(startX) || !Number.isInteger(startZ)) { console.warn('CAVEDIAMONDS_SCAN_ERROR invalid origin'); return; }
  const chunks = Number(size);
  if (!Number.isInteger(chunks) || chunks<1 || chunks>4) { console.warn('CAVEDIAMONDS_SCAN_ERROR invalid chunks'); return; }
  system.runJob(scan(chunks, mode, startX, startZ));
});
