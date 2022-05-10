from gemc_api_geometry import GVolume
from gemc_api_utils import GConfiguration
from gemc_api_materials import GMaterial
from volume_geometry_services import (
    VolumeParams,
    parse,
    read_file,
)

__author__ = "Maria K Zurek <zurek@anl.gov>"


def process_ftof(volume: VolumeParams) -> VolumeParams:
    name = volume.name

    def _parse_name(pat: str) -> dict:
        return parse(name, pat)

    # FTOF Sectors    
    if name.startswith("ftof_p"):
        parsed_data = _parse_name(r"^ftof_p(?P<panel>(1a|1b|2))_s(?P<sector>\d)$")
        volume.material = "G4_AIR"
        volume.color = "000000"
        volume.visible = 0
        volume.style = 0
        volume.description = f"Forward TOF - Panel {parsed_data['panel']} - Sector {parsed_data['sector']}"
    # FTOF Paddles
    if name.startswith("panel"):
        parsed_data = _parse_name(r"panel(?P<panel>(1a|1b|2))_sector(?P<sector>\d)_paddle_(?P<paddle>\d{1,2})$")
        volume.material = "scintillator"
        volume.color = "11ffaa" if parsed_data['panel'] == "1b" else "ff11aa"
        volume.visible = 1
        volume.style = 1
        volume.digitization = "ftof"
        volume.description = f"paddle {parsed_data['paddle']} - Panel {parsed_data['panel']} - Sector {parsed_data['sector']}"
        run_id, sector_id, panel_id, paddle_id = volume._identifier_numbers
        volume.identifier = f"sector: {sector_id}, panel: {panel_id}, paddle: {paddle_id}, side: 0"
    # FTOF Shield
    if name.startswith("ftof_shield"):
        parsed_data = _parse_name(r"^ftof_shield_p(?P<layer>(1a|1b|2))_sector(?P<sector>\d)$")
        volume.material = "G4_Pb"
        volume.color = "dc143c"
        volume.visible = 1
        volume.style = 1
        volume.description = f"Layer of lead - layer {parsed_data['layer']} -  Sector {parsed_data['sector']}"
    return volume


def apply_configuration(input_file_name: str, configuration: GConfiguration):
    volumes = read_file(input_file_name)

    for volume in volumes:
        volume = process_ftof(volume)
        gvolume = volume.build_gvolume()
        gvolume.publish(configuration)
