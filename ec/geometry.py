import sys
from typing import Mapping, Tuple
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

def process_ec(volume: VolumeParams) -> VolumeParams:
    name = volume.name

    def _parse_name(pat: str) -> dict:
        return parse(name, pat)

    # EC Mother Volume    
    if name.startswith("ec_s"):
        parsed_data = _parse_name(r"ec_s(?P<sector>\d)$")
        volume.material = "G4_AIR"
        volume.color = "ff1111"
        volume.visible = 0
        volume.description = f"Forward Calorimeter - Sector {parsed_data['sector']}"
    
    # lids
    # first stainless cover - Last-a-Foam layer - second stainless steel cover
    if name.startswith("eclid"):
        parsed_data = _parse_name(r"eclid(?P<layer>\d)_s(?P<sector>\d)$")
        layer_parsed = int(parsed_data['layer'])
        if layer_parsed == 2:
            volume.material = "LastaFoam"
            volume.color = "EED18C"
            volume.description = f"LastaFoam"
        else:
            volume.material = "G4_STAINLESS-STEEL"
            volume.color = "FCFFF0"
            volume.description = f"Stainless Steel Skin {layer_parsed}"
        volume.style = 1

    # lead layers
    if name.startswith("lead"):
        parsed_data = _parse_name(r"lead_(?P<layer>\d{1,2})_s(?P<sector>\d)_view_(?P<view>\d)_stack_(?P<stack>\d)$")
        layer_parsed = parsed_data['layer']
        volume.material = "G4_Pb"
        volume.color = "7CFC00"
        volume.style = 1
        volume.description = f"Forward Calorimeter lead layer {layer_parsed}"

    # Scintillator layers
    color_map_layers = {
        "U": "ff6633",
        "V": "33ffcc",
        "W": "33ffcc",
    }
    if name.find("scintillator") != -1:
        parsed_data = _parse_name(r"(?P<type>[UVW])-scintillator_(?P<layer>\d{1,2})_s(?P<sector>\d)_view_(?P<view>\d)_stack_(?P<stack>\d)$")
        volume.material = "G4_AIR"
        volume.color = color_map_layers[parsed_data['type']]
        volume.description = f"Forward Calorimeter scintillator layer ${parsed_data['layer']}"
    
    # UVW Layer Strips
    # Notice:
	# $layer is the scintillator layer, goes from 1 to 39

	# hipo:
	# layer=1-3 (PCAL) 4-9 (ECAL)
	# hipoADC.setByte("layer", counter, (byte) (view+stack*3));
	# view: u,v,w = 1,2,3
	# stack: Inner / Outer = 1,2

    color_map_strips: Mapping[str, Tuple(str, int)]= {
        "U": ("ff6633", 1),
        "V": ("6600ff", 2),
        "W": ("6600ff", 3),
    }
    if name.find("strip") != -1:
        parsed_data = _parse_name(r"(?P<type>[UVW])_strip_(?P<layer>\d{1,2})_(?P<strip>\d{1,2})_s(?P<sector>\d)_stack_(?P<stack>\d)$")
        volume.material = "scintillator"
        color, view = color_map_strips[parsed_data['type']]
        volume.color = color
        volume.style = 1
        volume.digitization = "ecal"
        volume.description = f"Forward Calorimeter scintillator layer {parsed_data['layer']} strip {parsed_data['strip']} view {view}"
        hipo_layer = view + int(parsed_data['stack']) * 3
        volume.identifier = f"sector: {parsed_data['sector']}, layer: {hipo_layer}, strip: {parsed_data['strip']}"
    return volume

def apply_configuration(input_file_name: str, configuration: GConfiguration):
    volumes = read_file(input_file_name)

    for volume in volumes:
        volume = process_ec(volume)
        gvolume = volume.build_gvolume()
        gvolume.publish(configuration)