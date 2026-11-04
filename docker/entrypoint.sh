#!/bin/sh
set -eu
if [ "${EULA:-FALSE}" != "TRUE" ]; then
  echo 'Setze EULA=TRUE nur nach Zustimmung zu https://www.minecraft.net/eula.' >&2
  exit 1
fi
mkdir -p /data/worlds
for config in allowlist.json permissions.json; do
  if [ ! -f "/data/$config" ]; then cp "/server/$config" "/data/$config"; fi
  rm -f "/server/$config"
  ln -s "/data/$config" "/server/$config"
done
if [ ! -f /data/server.properties ]; then
  cp /server/server.properties /data/server.properties
  sed -i 's/^level-name=.*/level-name=PrototypeTest/; s/^online-mode=.*/online-mode=true/; s/^allow-list=.*/allow-list=true/; s/^allow-cheats=.*/allow-cheats=true/; s/^content-log-console-output-enabled=.*/content-log-console-output-enabled=true/; s/^content-log-file-enabled=.*/content-log-file-enabled=true/' /data/server.properties
fi
rm -f /server/server.properties
ln -s /data/server.properties /server/server.properties
rm -rf /server/worlds
ln -s /data/worlds /server/worlds
if [ ! -d /data/worlds/PrototypeTest ]; then
  mkdir -p /data/worlds/PrototypeTest
  printf '%s\n' '[{"pack_id":"45411e2e-ecf2-4a3c-a00f-a20d4a27dbe2","version":[0,1,0]}]' > /data/worlds/PrototypeTest/world_behavior_packs.json
fi
exec /server/bedrock_server
