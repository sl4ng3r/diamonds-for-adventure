const oreHosts = new Map([
    ['minecraft:diamond_ore', 'minecraft:stone'],
    ['minecraft:deepslate_diamond_ore', 'minecraft:deepslate'],
]);
const exposedTypes = new Set([
    'minecraft:air', 'minecraft:cave_air', 'minecraft:water',
    'minecraft:flowing_water', 'minecraft:lava', 'minecraft:flowing_lava',
]);
const oreOffsets = [];
for (const x of [-1, 0, 1]) {
    for (const y of [-1, 0, 1]) {
        for (const z of [-1, 0, 1]) {
            const distance = Math.abs(x) + Math.abs(y) + Math.abs(z);
            if (distance) oreOffsets.push({x, y, z, face: distance === 1});
        }
    }
}
const positionKey = ({x, y, z}) => `${x},${y},${z}`;

export const oreTypes = [...oreHosts.keys()];
export const minY = -64;
export const maxY = 16;

export function keepBuriedVein(vein) {
    const anchor = vein.reduce((lowest, current) =>
        current.y < lowest.y ||
        (current.y === lowest.y && (current.x < lowest.x ||
            (current.x === lowest.x && current.z < lowest.z))) ? current : lowest);
    let hash = Math.imul(anchor.x, 0x8da6b343) ^
        Math.imul(anchor.y, 0xd8163841) ^ Math.imul(anchor.z, 0xcb1ab31f);
    hash = Math.imul(hash ^ (hash >>> 16), 0x45d9f3b);
    hash = Math.imul(hash ^ (hash >>> 16), 0x45d9f3b);
    const roll = ((hash ^ (hash >>> 16)) >>> 0) / 0x100000000;
    // Protected veins also contribute to the final amount of buried ore.
    if (anchor.y <= -55) return roll < 0.08;
    if (anchor.y <= -20) return roll < 0.15;
    return roll < 0.22;
}

export function planVeinRemoval(seeds, read, insideChunk, keep = keepBuriedVein, canRemoveAt = insideChunk) {
    const visited = new Set();
    const removals = [];
    for (const seed of seeds) {
        if (!insideChunk(seed) || seed.y < minY || seed.y > maxY ||
            visited.has(positionKey(seed)) || !oreHosts.has(read(seed))) continue;
        const vein = [seed];
        visited.add(positionKey(seed));
        let protectedVein = false;
        for (const point of vein) {
            for (const offset of oreOffsets) {
                const neighbor = {x: point.x + offset.x, y: point.y + offset.y, z: point.z + offset.z};
                if (neighbor.y < minY) continue;
                const block = read(neighbor);
                if (block === undefined || (offset.face && exposedTypes.has(block))) {
                    protectedVein = true;
                }
                if (!oreHosts.has(block)) continue;
                if (neighbor.y > maxY || !canRemoveAt(neighbor)) {
                    protectedVein = true;
                    continue;
                }
                const key = positionKey(neighbor);
                if (visited.has(key)) continue;
                visited.add(key);
                vein.push(neighbor);
            }
        }
        if (protectedVein || keep(vein)) continue;
        for (const position of vein) {
            const type = read(position);
            removals.push({position, type, replacement: oreHosts.get(type)});
        }
    }
    return removals;
}
