# ga-synth
Genetic Algorithm Synthesizer using Native Instruments Massive

# installing requirements:
* to install pyaudio, follow these requirements: http://people.csail.mit.edu/hubert/pyaudio/
    * when installing pyaudio using pip3 use the following command, updated from source: https://stackoverflow.com/questions/33513522/when-installing-pyaudio-pip-cannot-find-portaudio-h-in-usr-local-include
        * `pip3 install --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio`