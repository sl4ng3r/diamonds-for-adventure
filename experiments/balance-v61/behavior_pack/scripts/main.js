import {BlockVolume, system, world} from '@minecraft/server';
import {maxY, minY, oreTypes, planVeinRemoval} from './veins.js';

const markerType = 'minecraft:barrier';
const markerOffsets = [0, 1];
const spacing = 16;

function loadedBlock(dimension, position) {
    try {
        return dimension.getBlock(position);
    } catch (error) {
        if (error.name !== 'LocationInUnloadedChunkError') throw error;
        return undefined;
    }
}

function chunkMarkers(dimension, chunkX, chunkZ) {
    const markers = markerOffsets.map(x => loadedBlock(dimension, {
        x: chunkX * spacing + x, y: minY, z: chunkZ * spacing + 8,
    }));
    return markers.every(block => block?.typeId === markerType) ? markers : undefined;
}

function restoreBedrock(markers) {
    for (const marker of markers) marker.setType('minecraft:bedrock');
}

export function processChunk(dimension, chunkX, chunkZ) {
    const markers = chunkMarkers(dimension, chunkX, chunkZ);
    if (!markers) return undefined;
    const x = chunkX * spacing;
    const z = chunkZ * spacing;
    const endX = x + spacing - 1;
    const endZ = z + spacing - 1;
    const bounds = new BlockVolume({x, y: minY, z}, {x: endX, y: maxY, z: endZ});
    const seeds = dimension.getBlocks(bounds, {includeTypes: oreTypes}).getBlockLocationIterator();
    const read = position => {
        const block = loadedBlock(dimension, position);
        // Waterlogged surfaces count as water while fully solid blocks use their own type.
        return block?.isWaterlogged ? 'minecraft:water' : block?.typeId;
    };
    const inside = p => p.x >= x && p.x <= endX && p.z >= z && p.z <= endZ;
    const ready = new Map();
    const canRemoveAt = position => {
        if (inside(position)) return true;
        const cx = Math.floor(position.x / spacing);
        const cz = Math.floor(position.z / spacing);
        if (Math.abs(cx - chunkX) > 1 || Math.abs(cz - chunkZ) > 1) return false;
        const key = `${cx},${cz}`;
        if (!ready.has(key)) ready.set(key, Boolean(chunkMarkers(dimension, cx, cz)));
        return ready.get(key);
    };
    const removals = planVeinRemoval(seeds, read, inside, undefined, canRemoveAt);
    for (const {position, type, replacement} of removals) {
        const block = dimension.getBlock(position);
        if (block.typeId === type) block.setType(replacement);
    }
    restoreBedrock(markers);
    return removals.length;
}

const nearby = [[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]];
let nextPlayer = 0;
let nextErrorReport = 0;
function tryProcessNearby() {
    const players = world.getAllPlayers();
    for (let index = 0; index < players.length; index++) {
        const playerIndex = (nextPlayer + index) % players.length;
        const player = players[playerIndex];
        const {dimension, location} = player;
        if (dimension.id !== 'minecraft:overworld') continue;
        const chunkX = Math.floor(location.x / spacing);
        const chunkZ = Math.floor(location.z / spacing);
        for (const [dx, dz] of nearby) {
            if (processChunk(dimension, chunkX + dx, chunkZ + dz) === undefined) continue;
            nextPlayer = (playerIndex + 1) % players.length;
            return;
        }
    }
}

system.runInterval(() => {
    try {
        tryProcessNearby();
    } catch (error) {
        if (system.currentTick >= nextErrorReport) {
            console.warn(`Cave Diamonds: ${error}`);
            nextErrorReport = system.currentTick + 200;
        }
    }
}, 4);

function preserveEditedChunk({block, dimension}) {
    if (dimension.id !== 'minecraft:overworld') return;
    const {x, z} = block.location;
    const markers = chunkMarkers(dimension, Math.floor(x / spacing), Math.floor(z / spacing));
    if (markers) restoreBedrock(markers);
}

world.afterEvents.playerPlaceBlock.subscribe(preserveEditedChunk);
world.afterEvents.playerBreakBlock.subscribe(preserveEditedChunk);
