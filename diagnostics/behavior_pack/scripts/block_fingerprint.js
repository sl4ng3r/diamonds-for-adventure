// FNV-1a over block types; hash collisions are possible. Diamond is mapped to its host.
export function normalizeBlockType(type) {
  if (type==='minecraft:diamond_ore') return 'minecraft:stone';
  if (type==='minecraft:deepslate_diamond_ore') return 'minecraft:deepslate';
  return type;
}
export function updateFingerprint(hash, type) {
  type=normalizeBlockType(type);
  for (let i=0; i<type.length; i++) hash=Math.imul(hash ^ type.charCodeAt(i),16777619);
  return Math.imul(hash ^ 0,16777619) >>> 0;
}
