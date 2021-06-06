# ga-synth
Genetic Algorithm Synthesizer using Native Instruments Massive

# installing requirements:
* to install pyaudio, follow these requirements: http://people.csail.mit.edu/hubert/pyaudio/
    * when installing pyaudio using pip3 use the following command, updated from source: https://stackoverflow.com/questions/33513522/when-installing-pyaudio-pip-cannot-find-portaudio-h-in-usr-local-include
        * `pip3 install --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio`
    * Only installation succeeds using the above method. `pyaudio` fails when importing.
        * I think I need to re-install using an earlier version of python.
            * Based on this page: https://pypi.org/project/PyAudio/#modal-close I think only python 3.6 will work.
            * Additionally, pyaudio might need to be compiled from source since the versions listed on the link above are for windows 
            
    
