"""The main interface for the project. 

Run `python main.py -h` for usage. 

@author: <rbm@cmu.edu>
@date: 05/07/21
"""

import argparse
import Parameters
import sys
from BackgroundEffect import BackgroundEffect
from ApplyEffect import ApplyEffect
def get_parser(): 
  """A simple CLI interface to run the program. 

  For usage, compile with the -h flag, i.e., python main.py -h

  Returns: 
    (ArgumentParser) a parser object.
  """
  prog_descr = " ".join(
                ["This script adds a virtual background to images of people.",
                "This is known as image matting.\n",
                "The program takes the following arguments."]
               )

  parser = argparse.ArgumentParser(description=prog_descr)

  parser.add_argument("-v", "--virtual", metavar="V", 
                      type=str, nargs="?", required=False,
                      help=" ".join(
                        ["Path to a virtual background image",
                         "or a directory of background images that will",
                         "be rotated through. NOT IMPLEMENTED, CONCEPTUAL."]
                        )
                      )
  parser.add_argument("-c", "--color", metavar="C",
                      type=str, nargs="?", required=False,
                      help=" ".join(
                        ["Color to use as a virtual background image",
                         "Must be one of {white, blue, yellow, random}",
                         "NOT IMPLEMENTED, CONCEPTUAL."]
                        )
                      )

  parser.add_argument("-b", "--blur", metavar="B",
                      type=int, nargs="?", required=False,
                      help=" ".join(
                        ["Int specifying the size of the gaussian kernel",
                         "to blur with. Must be a positive odd value.",
                         "By default, if no background effect is specified,",
                         "the program will default to a blur with kernel",
                         "of size 5."]
                        )
                      )

  parser.add_argument("-t", "--time", 
                      action="store_true", required=False,
                      help=" ".join(
                        ["Debug flag. Will print out time required to process",
                         "each image to stdout. NOT IMPLEMENTED, CONCEPTUAL."]
                        )
                      )

  parser.add_argument("-d", "--debug", 
                      action="store_true", required=False,
                      help=" ".join(
                        ["Debug flag. Will print out statistics and program",
                         "states, as well as plots of image at various",
                         "processing states. NOT IMPLEMENTED, CONCEPTUAL."]
                        )
                      )

  parser.add_argument("-o", "--out_path", metavar="O",
                      type=str, nargs="?", required=False,
                      help=" ".join(
                        ["Out path to a directory for processed images.",
                         "If the directory does not exist, it will be made.",
                         "If unspecified, default to writing the images to a",
                         "new folder in the program directory. Path will be",
                         "printed to stdout upon creation."]
                        )
                      )

  parser.add_argument("-i", "--in_path", metavar="I", 
                      type=str, nargs="?", required=False,
                      help=" ".join(
                        ["In path for an image, or a directory of images.",
                         "If directory does not exist, or the path is not",
                         "an image, an assertion error will be thrown.",
                         "If unspecified, default to reading from the webcam"]
                        )
                      )

  parser.add_argument("-s", "--stitch", 
                      action="store_true", required=False,
                      help=" ".join(
                        ["If specified, will stitch the images into a video",
                         "and save them in the same directory as the processed",
                         "images. May not work on every machine."]
                        )
                      )

  return parser

if __name__ == "__main__":
  parser = get_parser()
  args = parser.parse_args()

  params = Parameters.Params(args.virtual, 
                             args.color, 
                             args.blur, 
                             args.time,
                             args.debug, 
                             args.out_path, 
                             args.in_path, 
                             args.stitch)

  be = BackgroundEffect(params.virtual, params.color, params.blur)

  effector = ApplyEffect(params.in_path, params.out_path, params.stitch, be)

  effector.apply_effect()
