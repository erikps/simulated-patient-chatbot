
###
### Script to be copied into the build folder. 
###

import pathlib

FD = pathlib.Path(__file__).parent.absolute()

if __name__ == '__main__':
    install(FD.joinpath('frontend'))
    install(FD.joinpath('backend'))
