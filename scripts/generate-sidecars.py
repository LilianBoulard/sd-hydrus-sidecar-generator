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


def parse_tags(parameters: str):
    parameters = f"Prompt: {parameters}"  # Prefix
    parameters = parameters.replace("\n", ", ")
    raw_parts = parameters.split(", ")
    parts: list[list[str]] = []
    for part in raw_parts:
        if not part:
            continue
        if part[0] in ascii_uppercase and ": " in part:
            sub_parts = part.split(": ")
            parts.append(sub_parts)
        else:
            parts[-1].append(part)
    return {
        part[0]: ", ".join(part[1:])
        for part in parts
    }


def to_hydrus(parameters: dict[str, str]) -> list[str]:
    """
    Converts parsed parameters to hydrus tags.
    """
    ignored = {"Size", "Version"}
    hydrus_tags = ["creator:Stable Diffusion"]
    for key, value in parameters.items():
        if key in ignored:
            continue
        if key == "Prompt":
            # We add the prompt parameters to the tags themselves
            hydrus_tags.extend(value.split(", "))
        tag = f"sd:{key}:{value}"
        hydrus_tags.append(tag)
    return hydrus_tags



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
        images_directory = Path(p.outpath_samples)
        for file in images_directory.iterdir():
            sidecar_file = images_directory / f"{file.name}.txt"
            geninfo, _ = images.read_info_from_image(Image.open(file))
            tags = to_hydrus(parse_tags(geninfo))
            sidecar_file.write_text("\n".join(tags))
            sidecars_count += 1
        raise Finished(f"Done constructing {sidecars_count} sidecars")
