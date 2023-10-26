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


class Script(scripts.Script):

    def title(self) -> str:
        return "Sidecar generator"

    def show(self, is_img2img: bool) -> bool:
        return True

    def ui(self, is_img2img: bool) -> None:
        pass

    def run(self, p: StableDiffusionProcessing):
        try:
            directory = p.output_directory
            print(directory)
        except Exception:
            print(vars(p))
        return
        for file in Path(p.output_directory).iterdir():  # FIXME
            Image.open()
        geninfo, items = images.read_info_from_image()
        generation = {**{'parameters': geninfo}, **items}
        print(generation)