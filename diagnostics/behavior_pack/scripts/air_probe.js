// Bounded connectivity test; it does not claim a player can reach the surface.
export function probeAir(start, getType, bounds, limit=64) {
  const inside = p => p.x>=bounds.minX && p.x<=bounds.maxX && p.y>=bounds.minY && p.y<=bounds.maxY && p.z>=bounds.minZ && p.z<=bounds.maxZ;
  if (!inside(start)) return {status:'boundary',count:0};
  if (getType(start)!=='minecraft:air') return {status:'none',count:0};
  const key = p => `${p.x},${p.y},${p.z}`;
  const seen = new Set([key(start)]), queue=[start];
  let boundary = false;
  for (let i=0; i<queue.length; i++) {
    if (queue.length>=limit) return {status:'large',count:queue.length};
    const p=queue[i];
    for (const [dx,dy,dz] of [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]]) {
      const next={x:p.x+dx,y:p.y+dy,z:p.z+dz};
      if (!inside(next)) { boundary=true; continue; }
      const k=key(next);
      if (!seen.has(k)) {
        seen.add(k);
        if (getType(next)==='minecraft:air') queue.push(next);
      }
    }
  }
  return {status:boundary?'boundary':'small',count:queue.length};
}
