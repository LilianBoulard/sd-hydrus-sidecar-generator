"""
sd-sidecar-generator

Author: Lilian Boulard <https://github.com/LilianBoulard>

Licensed under the GNU Affero General Public License.
"""

import modules.scripts as scripts
from modules import images
from modules.processing import StableDiffusionProcessing
from PIL import Image
from pathlib import Path
from string import ascii_uppercase


def convert_to_hydrus_tags(parameters: str):
    parameters = f"Prompt: {parameters}"  # Prefix
    parameters = parameters.replace(r"\n", ", ")
    raw_parts = parameters.split(", ")
    parts: list[list[str]] = [[]]
    for part in raw_parts:
        if part[0] in ascii_uppercase and ": " in part:
            parts.append([part])
        else:
            parts[-1].append(part)
    return {
        part[0]: part[1:]
        for part in parts
    }



class Finished(Exception):
    pass


class Script(scripts.Script):

    def title(self) -> str:
        return "Sidecar generator"

    def show(self, is_img2img: bool) -> bool:
        return True

    def ui(self, is_img2img: bool) -> None:
        pass

    def run(self, p: StableDiffusionProcessing):
        sidecars_count = 0
        for file in Path(p.outpath_samples).iterdir():
            sidecars_count += 1
            geninfo, _ = images.read_info_from_image(Image.open(file))
            print(convert_to_hydrus_tags(geninfo))
        raise Finished(f"Done constructing {sidecars_count} sidecars")*
