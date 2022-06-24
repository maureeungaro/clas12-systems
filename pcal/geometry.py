import sys
from gemc_api_geometry import GVolume
from gemc_api_utils import GConfiguration
from gemc_api_materials import GMaterial
sys.path.append("..")
from volume_geometry_services import (
    VolumeParams,
    parse,
    read_file,
)

__author__ = "Maria K Zurek <zurek@anl.gov>"

def process_pcal(volume: VolumeParams) -> VolumeParams:
    name = volume.name

    def _parse_name(pat: str) -> dict:
        return parse(name, pat)

    # PCAL Mother Volume    
    if name.startswith("pcal_s"):
        volume.material = "G4_AIR"
        volume.color = "ff1111"
        volume.visible = 0
        volume.description = "Preshower Calorimeter"
    # Lead Layers
    if name.startswith("PCAL_Lead_Layer"):
        parsed_data = _parse_name(r"PCAL_Lead_Layer_(?P<layer>\d{1,2})_s(?P<sector>\d)$")
        volume.material = "G4_Pb"
        volume.color = "66ff33"
        volume.visible = 1
        volume.style = 1
        volume.description = f"Preshower Calorimeter lead layer {parsed_data['layer']}"

    # U Layers
    if name.startswith("U-view-scintillator"):
        parsed_data = _parse_name(r"U-view-scintillator_(?P<layer>\d{1,2})_s(?P<sector>\d)$")
        volume.material = "G4_TITANIUM_DIOXIDE"
        volume.color = "ff6633"
        volume.visible = 1
        volume.style = 1
        volume.description = "Preshower Calorimeter"
    # U Layer Strips
    if name.startswith("U-view_single_strip"):
        parsed_data = _parse_name(r"U-view_single_strip_(?P<ulayer>\d)_(?P<strip>\d{1,2})_s(?P<sector>\d)$")
        volume.material = "scintillator"
        volume.color = "ff6633"
        volume.visible = 1
        volume.description = "Preshower Calorimeter scintillator layer 1 strip"
        strip_parsed = int(parsed_data['strip'])
        if strip_parsed == 0:
            volume.style = 1 
        else:        
            volume.digitization = "ecal"
            sector_id = parsed_data['sector']
            layer_id = 1
            strip_id = strip_parsed if strip_parsed <= 52 else 53 + (strip_parsed-53) // 2
            volume.identifier = f"sector: {sector_id}, layer: {layer_id}, strip: {strip_id}"

    # V Layers
    if name.startswith("V-view-scintillator"):
        parsed_data = _parse_name(r"V-view-scintillator_(?P<layer>\d{1,2})_s(?P<sector>\d)$")
        volume.material = "G4_TITANIUM_DIOXIDE"
        volume.color = "33ffcc"
        volume.visible = 1
        volume.style = 1
        volume.description = "Preshower Calorimeter"
    # V Layer Strips
    if name.startswith("V-view_single_strip"):
        parsed_data = _parse_name(r"V-view_single_strip_(?P<vlayer>\d)_(?P<strip>\d{1,2})_s(?P<sector>\d)$")
        volume.material = "scintillator"
        volume.color = "6600ff"
        volume.visible = 1
        volume.description = "Preshower Calorimeter scintillator layer 2 strip"
        strip_parsed = int(parsed_data['strip'])
        if strip_parsed == 0:
            volume.style = 1 
        else:        
            volume.digitization = "ecal"
            sector_id = parsed_data['sector']
            layer_id = 2
            strip_id = 1 + ((strip_parsed-1) // 2) if strip_parsed <= 30 else strip_parsed-15
            volume.identifier = f"sector: {sector_id}, layer: {layer_id}, strip: {strip_id}"

    # W Layers
    if name.startswith("W-view-scintillator"):
        parsed_data = _parse_name(r"W-view-scintillator_(?P<layer>\d{1,2})_s(?P<sector>\d)$")
        volume.material = "G4_TITANIUM_DIOXIDE"
        volume.color = "33ffcc"
        volume.visible = 1
        volume.style = 1
        volume.description = "Preshower Calorimeter"
    # W Layer Strips
    if name.startswith("W-view_single_strip"):
        parsed_data = _parse_name(r"W-view_single_strip_(?P<wlayer>\d)_(?P<strip>\d{1,2})_s(?P<sector>\d)$")
        volume.material = "scintillator"
        volume.color = "6600ff"
        volume.visible = 1
        volume.description = "Preshower Calorimeter scintillator layer 3 strip"
        strip_parsed = int(parsed_data['strip'])
        if strip_parsed == 0:
            volume.style = 1 
        else:        
            volume.digitization = "ecal"
            sector_id = parsed_data['sector']
            layer_id = 3
            strip_id = 1 + ((strip_parsed-1) // 2) if strip_parsed <= 30 else strip_parsed-15
            volume.identifier = f"sector: {sector_id}, layer: {layer_id}, strip: {strip_id}"

    # Back and Front Stanless Steel Window
    if name.startswith("Stainless_Steel"):
        parsed_data = _parse_name(r"Stainless_Steel_(?P<window>(Back|Front))_(?P<layer>\d)_s(?P<sector>\d)$")
        volume.material = 'G4_STAINLESS-STEEL'
        volume.color = "D4E3EE"
        volume.style = 1
        volume.description = f"{parsed_data['window']} Window"

    # Back and Front Last-a-Foam Window
    if name.startswith("Last-a-Foam"):
        parsed_data = _parse_name(r"Last-a-Foam_(?P<window>(Back|Front))_s(?P<sector>\d)$")
        volume.material = "LastaFoam"
        volume.color = "EED18C"
        volume.style = 1
        volume.description = f"{parsed_data['window']} Foam"
    return volume

def apply_configuration(input_file_name: str, configuration: GConfiguration):
    volumes = read_file(input_file_name)

    for volume in volumes:
        volume = process_pcal(volume)
        gvolume = volume.build_gvolume()
        gvolume.publish(configuration)