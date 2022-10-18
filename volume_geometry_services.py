#!/usr/bin/env python3

__author__ = "Maria K Zurek <zurek@anl.gov>"


from dataclasses import dataclass, field, asdict
import logging

import collections
import re
from typing import List, Iterable, Dict, Tuple, Union

from gemc_api_geometry import GVolume


_logger = logging.getLogger("volume_geometry_services")


def _ensure_single_unit(units: Iterable[str]) -> str:
    if len(set(units)) == 1:
        return units[0]
    else:
        raise ValueError(f"The units are different! {units}")


def _extract_numbers_units(tokens: Iterable[str], unit_separator: str = "*") -> Tuple[List[float], List[str]]:
    numbers, units = [], []
    for tok in tokens:
        number_and_units = tok.split(unit_separator)
        if len(number_and_units) == 2:
            num, unit = number_and_units
        else:
            num, unit = tok, None
        numbers.append(float(num))
        units.append(unit)
    return numbers, units


@dataclass
class PositionParams:
    "Parses position parameters"
    original: str
    tokens: List[str] = None
    without_units: str = None
    numbers: List[float] = None
    units: List[str] = None

    def __post_init__(self):
        self.tokens = self.original.split()

        self.numbers, self.units = _extract_numbers_units(self.tokens)


@dataclass
class RotationParams:
    "Parses and orders rotation parameters"
    original: str
    tokens: List[str] = None
    order: str = None
    numbers: List[str] = None
    units: List[str] = None
    single_unit: str = None

    def __post_init__(self):
        s = self.original
        self.tokens = s.split()

        numbers_with_units = []
        if len(self.tokens) == 3:
            numbers_with_units = self.tokens
        elif len(self.tokens) == 5:
            self.order = " ".join(self.tokens[1:2])
            numbers_with_units = self.tokens[2:5]

        self.numbers, self.units = _extract_numbers_units(numbers_with_units)
        self.single_unit = _ensure_single_unit(self.units)


@dataclass
class SolidParams:
    original: str
    solid_type: str
    dimensions: List[str] = None
    numbers: List[float] = None
    units: List[str] = None

    def __post_init__(self):
        self.dimensions = self.original.split()
        self.numbers, self.units = _extract_numbers_units(self.dimensions)

    def process_volume(self, gvolume):
        map_type_to_method = {
            "Box": self.process_box,
            "Tube": self.process_tube,
            "Sphere": self.process_sphere,
            "Polycone": self.process_polycone,
            "Trd": self.process_trd,
            "G4Trap": self.process_trap,
        }
        return map_type_to_method[self.solid_type](gvolume)

    def process_box(self, gvolume):
        gvolume.make_box(
            *self.numbers,
            lunit=_ensure_single_unit(self.units),
        )

    def process_tube(self, gvolume):
        length_units = self.units[:3]
        angle_units = self.units[3:]
        
        gvolume.make_tube(
            *self.numbers,
            lunit1=_ensure_single_unit(length_units),
            lunit2=_ensure_single_unit(angle_units)
        )
    
    def process_sphere(self, gvolume):
        length_units = self.units[:2]
        angle_units = self.units[2:]
        
        gvolume.make_sphere(
            *self.numbers,
            lunit1=_ensure_single_unit(length_units),
            lunit2=_ensure_single_unit(angle_units)
        )

    def process_polycone(self, gvolume):
        def get_chunk(lst, idx, size):
            return lst[size * idx:size * (idx + 1)]
        
        def get_chunks(numbers, size):
            return {
                idx: get_chunk(numbers[3:], idx, size)
                for idx in [0, 1, 2]
            }

        n_planes = int(self.numbers[2])
        chunks = get_chunks(self.numbers, n_planes)
        args = [
            self.numbers[0],
            self.numbers[1],
            n_planes,
            *chunks[2],
            *chunks[0],
            *chunks[1]
        ]
        angle_units = self.units[:2]
        length_units = self.units[3:]
        gvolume.make_polycone(
            *args,
            lunit1=_ensure_single_unit(length_units),
            lunit2=_ensure_single_unit(angle_units)
        )

    def process_trd(self, gvolume):
        gvolume.make_trapezoid(
            *self.numbers,
            lunit=_ensure_single_unit(self.units)
        )

    def process_trap(self, gvolume):
        length_units = self.units[0:1] + self.units[3:6] + self.units[7:10]
        angle_units = self.units[1:3] + [self.units[6], self.units[10]]
        
        gvolume.make_trap(
            self.numbers,
            lunit1=_ensure_single_unit(length_units),
            lunit2=_ensure_single_unit(angle_units)
        )

@dataclass
class VolumeParams:
    "Parses and stores G4 volume parameters"
    _original: str = field(repr=False)
    _tokens: List[str] = field(default_factory=list, repr=None)
    name: str = None
    mother: str = None
    _solid: SolidParams = None
    material: str = None
    _position: PositionParams = None
    _rotation: RotationParams = None
    mfield: str = None
    visible: float = None
    style: float = None
    color: str = None
    digitization: str = None
    _identifier_volume: str = None
    _identifier_template: str = field(default="", repr=False)
    _identifier_numbers: List[str] = None
    identifier: str = None
    copyOf: str = None
    replicaOf: str = None
    solidsOpr: str = None
    mirror: str = None
    exist: str = None
    description: str = None

    def __post_init__(self):
        s = self._original
        self.tokens = [
            tok.strip()
            for tok in s.split("|")
        ]
        self.read_volume(self.tokens)
        if self._identifier_template:
            self.set_identifier(self._identifier_template)

    def read_volume(self, tokens: List[str]):
        self.name = tokens[0]
        self.mother = tokens[1]
        self._solid = SolidParams(tokens[5], tokens[4])
        self._position = PositionParams(tokens[2])
        self._rotation = RotationParams(tokens[3])
        self._identifier_volume = tokens[6]
        self._identifier_numbers = self._identifier_volume.split()

    def build_gvolume(self):
        gvolume = GVolume(self.name)
        gvolume.set_position(
            *self._position.numbers,
            lunit=_ensure_single_unit(self._position.units),
        )
        rotation_kwargs = {}
        if self._rotation.single_unit is not None:
            rotation_kwargs["lunit"] = self._rotation.single_unit
        if self._rotation.order is not None:
            rotation_kwargs["order"] = self._rotation.order
        gvolume.set_rotation(
            *self._rotation.numbers,
            **rotation_kwargs,
        )

        self._solid.process_volume(gvolume)
        self.set_attributes(gvolume)
        return gvolume

    def set_attributes(self, gvolume):

        for attr_name, attr_value in asdict(self).items():
            if attr_name.startswith("_"): continue
            if attr_value is not None:
                setattr(gvolume, attr_name, attr_value)


def read_file(
        input_file_name,
    ) -> Iterable[VolumeParams]:

    with open(input_file_name) as f:
        return [
           VolumeParams(line)
           for line in f.readlines()
        ]


def parse(text: str, pattern: Union[str, re.Pattern]) -> dict:
    pat = re.compile(pattern)
    m = re.match(pat ,text)
    return m.groupdict()


