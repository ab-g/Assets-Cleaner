import glob
import json
import os
import re
import sys

g_key_to_dir = {
    'scenes': 'scenes',
    'scripts': 'scripts',
    'cameras': 'cameras',
    'meshes': 'meshes',
    'skinControllers': 'skin-controllers',
    'materials': 'materials',
    'textures2d': 'textures/2D',
    'texturesCube': 'textures/cube',
    'images': 'images',
    'lights': 'lights',
    'animations': 'animations',
    'audioSources': 'audio-sources',
    'soundSamples': 'sounds',
    'rigidBodies': 'rigid-bodies',
    'colliders': 'colliders',
    'characters': 'characters',
    'stateMachines': 'state-machines',
}

g_dir_to_key = {
    'scenes': 'scenes',
    'scripts': 'scripts',
    'cameras': 'cameras',
    'meshes': 'meshes',
    'skin-controllers': 'skinControllers',
    'materials': 'materials',
    'textures/2D': 'textures2d',
    'textures/cube': 'texturesCube',
    'images': 'images',
    'lights': 'lights',
    'animations': 'animations',
    'audio-sources': 'audioSources',
    'sounds': 'soundSamples',
    'rigid-bodies': 'rigidBodies',
    'colliders': 'colliders',
    'characters': 'characters',
    'state-machines': 'stateMachines',
}


def make_assets_ids_dict():
    assets_ids = {
        'scenes': set(),
        'scripts': set(),
        'cameras': set(),
        'meshes': set(),
        'skinControllers': set(),
        'materials': set(),
        'textures2d': set(),
        'texturesCube': set(),
        'images': set(),
        'lights': set(),
        'animations': set(),
        'audioSources': set(),
        'soundSamples': set(),
        'rigidBodies': set(),
        'colliders': set(),
        'characters': set(),
        'stateMachines': set()
    }
    return assets_ids


def get_resource_pack_data(game_project_dir_path):
    resource_pack_file_path = os.path.join(game_project_dir_path, 'resource-pack.json')
    with open(resource_pack_file_path, 'r') as resource_pack_file:
        resource_pack_data = json.load(resource_pack_file)
    return resource_pack_data


def get_first_scene_id(resource_pack_data):
    return resource_pack_data['scenes']['map'][0]['value']['id']['uuid']


def get_scene_data(game_project_dir_path, scene_id):
    scene_file_path = os.path.join(game_project_dir_path, 'scenes/{0}.json'.format(scene_id))
    with open(scene_file_path, 'r') as scene_file:
        scene_data = json.load(scene_file)
    return scene_data


def get_default_character_data(game_project_dir_path, character_id=None):
    if character_id is None:
        resource_pack_data = get_resource_pack_data(game_project_dir_path)
        character_id = resource_pack_data['defaultCharacterId']['uuid']
    character_file_path = os.path.join(game_project_dir_path, 'characters/{0}.json'.format(character_id))
    with open(character_file_path, 'r') as character_file:
        character_data = json.load(character_file)
    return character_data


def get_file_path(path_to_asset):
    with open(path_to_asset, 'r') as asset_file:
        asset_data = json.load(asset_file)
    return asset_data['filePath']


def extract_used_textures_ids(game_project_dir_path, materials_ids):
    used_textures_ids_2d = []
    used_textures_ids_cube = []
    for material_id in materials_ids:
        material_file_path = os.path.join(game_project_dir_path, 'materials/{0}.json'.format(material_id))
        with open(material_file_path, 'r') as material_file:
            material_data = json.load(material_file)
            textures_keys_2d = ['diffuseMap', 'normalMap', 'specularMap', 'emissiveMap', 'heightMap', 'alphaMap', 'occlusionMap', 'roughnessMap', 'metalnessMap']
            for texture_key in textures_keys_2d:
                texture_id = material_data[texture_key]['uuid']
                if texture_id.startswith('00000000-0000-0000-0000-0000000000'):  # ??
                    continue
                used_textures_ids_2d.append(texture_id)
            textures_keys_cube = ['envMap', 'irrEnvMap']
            for texture_key in textures_keys_cube:
                texture_id = material_data[texture_key]['uuid']
                if texture_id.startswith('00000000-0000-0000-0000-0000000000'):  # ??
                    continue
                used_textures_ids_cube.append(texture_id)
    return used_textures_ids_2d, used_textures_ids_cube


def extract_used_images_ids_from_textures_2d(game_project_dir_path, textures_ids):
    used_images_ids = []
    for texture_id in textures_ids:
        texture_file_path = os.path.join(game_project_dir_path, 'textures/2D/{0}.json'.format(texture_id))
        with open(texture_file_path, 'r') as texture_file:
            texture_data = json.load(texture_file)
            image_id = texture_data['image']['id']['uuid']
            used_images_ids.append(image_id)
    return used_images_ids


def extract_used_images_ids_from_textures_cube(game_project_dir_path, textures_ids):
    used_images_ids = []
    for texture_id in textures_ids:
        texture_file_path = os.path.join(game_project_dir_path, 'textures/cube/{0}.json'.format(texture_id))
        with open(texture_file_path, 'r') as texture_file:
            texture_data = json.load(texture_file)
            top_image_id = texture_data['topImage']['id']['uuid']
            used_images_ids.append(top_image_id)
            bottom_image_id = texture_data['bottomImage']['id']['uuid']
            used_images_ids.append(bottom_image_id)
            left_image_id = texture_data['leftImage']['id']['uuid']
            used_images_ids.append(left_image_id)
            right_image_id = texture_data['rightImage']['id']['uuid']
            used_images_ids.append(right_image_id)
            front_image_id = texture_data['frontImage']['id']['uuid']
            used_images_ids.append(front_image_id)
            back_image_id = texture_data['backImage']['id']['uuid']
            used_images_ids.append(back_image_id)
    return used_images_ids


def extract_used_animations_ids(game_project_dir_path, timelines_ids):
    used_animations_ids = []
    for timeline_id in timelines_ids:
        timeline_file_path = os.path.join(game_project_dir_path, 'scripts/{0}.json'.format(timeline_id))
        with open(timeline_file_path, 'r') as timeline_file:
            timeline_data = json.load(timeline_file)
            scripts = timeline_data['scripts']['list']
            for script in scripts:
                used_animations_ids.append(script['animation']['uuid'])
    return used_animations_ids


def extract_used_sounds_ids(game_project_dir_path, animations_ids):
    used_sound_ids = []
    for animation_id in animations_ids:
        animation_file_path = os.path.join(game_project_dir_path, 'animations/{0}.json'.format(animation_id))
        with open(animation_file_path, 'r') as animation_file:
            animation_data = json.load(animation_file)
            if 'tracks' in animation_data:
                tracks = animation_data['tracks']
                for track in tracks:
                    if 'clips' in track:
                        clips = track['clips']
                        for clip in clips:
                            behavior = clip['behavior']
                            if "SoundSampleBehavior" == behavior['@class']:
                                sound_id = behavior['soundSampleId']['uuid']
                                used_sound_ids.append(sound_id)
    return used_sound_ids


def extract_assets_ids_from_nodes(game_project_dir_path, nodes):
    assets_ids = make_assets_ids_dict()

    for node in nodes:
        obj = node['object3D']
        object_id = obj['id']['uuid']
        object_name = obj['name']

        if 'audio' in obj:
            audioSourceId = obj['audio']['audioSourceId']['uuid']
            assets_ids['audioSources'].add(audioSourceId)

        if 'camera' in obj:
            cameraId = obj['camera']['cameraId']['uuid']
            assets_ids['cameras'].add(cameraId)

        if 'colliders' in obj:
            for collider_component in obj['colliders']:
                colliderId = collider_component['colliderId']['uuid']
                assets_ids['colliders'].add(colliderId)

        if 'geometry' in obj:
            geometry_component = obj['geometry']
            meshId = geometry_component['meshId']['uuid']
            assets_ids['meshes'].add(meshId)
            if 'skinControllerId' in geometry_component:
                skinControllerId = geometry_component['skinControllerId']['uuid']
                assets_ids['skinControllers'].add(skinControllerId)

        if 'light' in obj:
            lightId = obj['light']['lightId']['uuid']
            assets_ids['lights'].add(lightId)

        if 'material' in obj:
            material_id = obj['material']['materialId']['uuid']
            assets_ids['materials'].add(material_id)
            used_textures_ids_2d, used_textures_ids_cube = extract_used_textures_ids(game_project_dir_path, [material_id])
            for texture_id in used_textures_ids_2d:
                assets_ids['textures2d'].add(texture_id)
            for texture_id in used_textures_ids_cube:
                assets_ids['texturesCube'].add(texture_id)
            images_ids_from_textures_2d = extract_used_images_ids_from_textures_2d(game_project_dir_path, used_textures_ids_2d)
            for image_id in images_ids_from_textures_2d:
                assets_ids['images'].add(image_id)
            images_ids_from_textures_cube = extract_used_images_ids_from_textures_cube(game_project_dir_path, used_textures_ids_cube)
            for image_id in images_ids_from_textures_cube:
                assets_ids['images'].add(image_id)

        if 'rigidBody' in obj:
            rigidBodyId = obj['rigidBody']['rigidBodyId']['uuid']
            assets_ids['rigidBodies'].add(rigidBodyId)

        if 'timeline' in obj:
            timelineId = obj['timeline']['timelineId']['uuid']
            assets_ids['scripts'].add(timelineId)
            animations_ids = extract_used_animations_ids(game_project_dir_path, [timelineId])
            for animation_id in animations_ids:
                assets_ids['animations'].add(animation_id)
            sounds_ids = extract_used_sounds_ids(game_project_dir_path, animations_ids)
            for sound_id in sounds_ids:
                assets_ids['soundSamples'].add(sound_id)

        if 'spawner' in obj:
            characterScriptId = obj['spawner']['characterScriptId']['uuid']
            assets_ids['scripts'].add(characterScriptId)

        if 'stateMachine' in obj:
            stateMachineId = obj['stateMachine']['stateMachineId']['uuid']
            assets_ids['stateMachines'].add(stateMachineId)

        if 'transform' in obj:
            pass

    return assets_ids


def extract_assets_ids_from_scene(game_project_dir_path, scene_id=None):
    resource_pack_data = get_resource_pack_data(game_project_dir_path)
    if scene_id is None:
        scene_id = get_first_scene_id(resource_pack_data)
    scene_data = get_scene_data(game_project_dir_path, scene_id)
    assets_ids = extract_assets_ids_from_nodes(game_project_dir_path, scene_data['nodes'])

    for script in scene_data['scriptSystem']['scripts']:
        script_id = script['id']['uuid']
        assets_ids['scripts'].add(script_id)

    return assets_ids


def extract_assets_ids(game_project_dir_path):
    assets_ids = make_assets_ids_dict()

    resource_pack_data = get_resource_pack_data(game_project_dir_path)

    character_id = resource_pack_data['defaultCharacterId']['uuid']
    assets_ids['characters'].add(character_id)

    default_state_machine_id = resource_pack_data['defaultStateMachineId']['uuid']
    assets_ids['stateMachines'].add(default_state_machine_id)

    scene_id = get_first_scene_id(resource_pack_data)
    assets_ids['scenes'].add(scene_id)
    assets_ids_from_scene = extract_assets_ids_from_scene(game_project_dir_path, scene_id)
    for k, v in assets_ids_from_scene.items():
        assets_ids[k] = assets_ids[k].union(v)

    default_character_data = get_default_character_data(game_project_dir_path)
    assets_ids_from_character = extract_assets_ids_from_nodes(game_project_dir_path, default_character_data['body'])
    for k, v in assets_ids_from_character.items():
        assets_ids[k] = assets_ids[k].union(v)

    return assets_ids


def clean_via_resource_pack(game_project_dir_path, used_assets_ids):
    resource_pack_file_path = os.path.join(game_project_dir_path, 'resource-pack.json')
    with open(resource_pack_file_path, 'r') as resource_pack_file:
        resource_pack_data = json.load(resource_pack_file)
        for k, v in used_assets_ids.items():
            if 'scripts' == k:
                continue
            kv = resource_pack_data[k]['map']
            for i in range(len(kv) - 1, -1, -1):
                asset_id = kv[i]['key']['uuid']
                if asset_id not in v:
                    asset_file_path = os.path.join(game_project_dir_path, '{0}/{1}.json'.format(g_key_to_dir[k], asset_id))
                    bin_file_path = None
                    if 'meshes' == k:
                        bin_file_path = os.path.join(game_project_dir_path, '{0}/{1}.bin'.format(g_key_to_dir[k], asset_id))
                    elif 'images' == k or 'soundSamples' == k:
                        file_path = get_file_path(asset_file_path)
                        bin_file_path = os.path.join(game_project_dir_path, '{0}/{1}'.format(g_key_to_dir[k], file_path))
                    print(asset_file_path)
                    os.remove(asset_file_path)
                    if bin_file_path is not None:
                        print(bin_file_path)
                        os.remove(bin_file_path)
                    del kv[i]
    with open(resource_pack_file_path, 'w') as resource_pack_file:
        json.dump(resource_pack_data, resource_pack_file, indent=4, sort_keys=False)


def extract_attachments(game_project_dir_path):
    attachments = make_assets_ids_dict()
    for dir in ['images', 'sounds']:
        asset_dir = os.path.join(game_project_dir_path, '{0}/{1}'.format(game_project_dir_path, dir))
        for full_file_path in glob.iglob(f'{asset_dir}/*.*'):
            file_name_with_ext = os.path.basename(full_file_path)
            file_name, file_extension = os.path.splitext(file_name_with_ext)
            if '.json' == file_extension:
                attachments[g_dir_to_key[dir]].add(get_file_path(full_file_path))
    return attachments


def find_unused_files(game_project_dir_path, used_assets_ids):
    attachments = extract_attachments(game_project_dir_path)

    for dir in g_dir_to_key:
        key = g_dir_to_key[dir]
        asset_dir = os.path.join(game_project_dir_path, '{0}/{1}'.format(game_project_dir_path, dir))
        for full_file_path in glob.iglob(f'{asset_dir}/*.*'):
            file_name_with_ext = os.path.basename(full_file_path)
            file_name, file_extension = os.path.splitext(file_name_with_ext)
            if '.json' == file_extension or '.bin' == file_extension:
                if re.match(r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}", file_name):
                    if file_name not in used_assets_ids[key]:
                        print(file_name)
            else:
                if file_name_with_ext not in attachments[key]:
                    print(file_name_with_ext)


def main(game_project_dir_path):
    used_assets_ids = None
    used_assets_ids = extract_assets_ids(game_project_dir_path)
    clean_via_resource_pack(game_project_dir_path, used_assets_ids)
    find_unused_files(game_project_dir_path, used_assets_ids)


if __name__ == '__main__':
    main(sys.argv[1])
