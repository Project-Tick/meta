import concurrent.futures
import json
import os
from datetime import datetime

from meta.common import (
    upstream_path,
    ensure_upstream_dir,
    transform_maven_key,
    default_session,
)
from meta.common.fabric import DATETIME_FORMAT_HTTP
from meta.common.mojang import VERSIONS_DIR as MOJANG_VERSIONS_DIR
from meta.common.ornithe import (
    JARS_DIR,
    LIBRARIES_DIR,
    META_DIR,
    META_URL,
    MAVEN_URL,
    INTERMEDIARY_GENERATION,
    LOADERS,
)
from meta.model.fabric import FabricJarInfo

UPSTREAM_DIR = upstream_path()
GEN = f"gen{INTERMEDIARY_GENERATION}"

ensure_upstream_dir(JARS_DIR)
ensure_upstream_dir(LIBRARIES_DIR)
ensure_upstream_dir(META_DIR)

sess = default_session()


def get_json_file(path, url):
    r = sess.get(url)
    r.raise_for_status()
    version_json = r.json()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(version_json, f, sort_keys=True, indent=4)
    return version_json


def get_maven_jar_url(maven_key):
    group, artifact, version = maven_key.split(":", 3)
    return (
        f"{MAVEN_URL}/{group.replace('.', '/')}/{artifact}/{version}/"
        f"{artifact}-{version}.jar"
    )


def has_minecraft_version(version):
    return os.path.isfile(
        os.path.join(UPSTREAM_DIR, MOJANG_VERSIONS_DIR, f"{version}.json")
    )


def update_intermediary_version(entry):
    version = entry["version"]
    print(f"Processing intermediary {version}")

    r = sess.head(get_maven_jar_url(entry["maven"]))
    r.raise_for_status()
    tstamp = datetime.strptime(r.headers["Last-Modified"], DATETIME_FORMAT_HTTP)

    data = FabricJarInfo(release_time=tstamp)
    data.write(
        os.path.join(
            UPSTREAM_DIR, JARS_DIR, f"{transform_maven_key(entry['maven'])}.json"
        )
    )

    get_json_file(
        os.path.join(UPSTREAM_DIR, LIBRARIES_DIR, f"{version}.json"),
        f"{META_URL}/{GEN}/libraries/{version}",
    )

    print(f"Processing intermediary {version} Done")


def main():
    for loader in LOADERS:
        get_json_file(
            os.path.join(UPSTREAM_DIR, META_DIR, f"{loader}-loader.json"),
            f"{META_URL}/{GEN}/{loader}-loader",
        )

    index = get_json_file(
        os.path.join(UPSTREAM_DIR, META_DIR, "intermediary.json"),
        f"{META_URL}/{GEN}/intermediary",
    )

    wanted = [entry for entry in index if has_minecraft_version(entry["version"])]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(update_intermediary_version, entry) for entry in wanted
        ]
        for f in futures:
            f.result()


if __name__ == "__main__":
    main()
