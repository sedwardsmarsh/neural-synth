# ga-synth
Genetic Algorithm Synthesizer using Native Instruments Massive
<hr>

## ideas
6/17/21
* from dad: 
    * compare performance of "society of the mind", many discrete GAs solving atomic tasks like pitch and filter control versus performance of gigantic "end to end GA"
        * which converges faster?
        * which has more genetic variance?
            * does one method allow for easier control of genetic variance?
        * what else is there to analyze
    
    * for fitness function (comparing sound that GA produces for a generation vs. target sound):
        * what method yields best, most interesting, worst results?
        * taking difference of audio file
        * taking difference of spectrogram image
        * taking difference of series of FFTs (for sounds that modulate over time)
        * taking difference of series of spectrogram images (for sounds that modulate over time)

## installing requirements:
 6/14/21
* recording audio with `sounddevice`!!!!
* `pyaudio` now magically installs on the default `python3 -m venv ...` created virtual environment!!?
        * decided to switch to using `sounddevice` instead of `pyaudio`, for the simpler interface and better documentation
    * virtual env. information
        * `Python 3.8.2 (v3.8.2:7b3ab5921f, Feb 24 2020, 17:52:18) [Clang 6.0 (clang-600.0.57)] on darwin`

PRE 6/14/21
* re-write for pytorch Big Sur apple silicon installation
* to install pyaudio, follow these requirements: http://people.csail.mit.edu/hubert/pyaudio/
    * when installing pyaudio using pip3 use the following command, updated from source: https://stackoverflow.com/questions/33513522/when-installing-pyaudio-pip-cannot-find-portaudio-h-in-usr-local-include
        * `pip3 install --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio`
    
    * Only installation succeeds using the above method. `pyaudio` fails when importing.
        * I think I need to re-install using an earlier version of python.
            * Based on this page: https://pypi.org/project/PyAudio/#modal-close I think only python 3.6 will work.
            * Additionally, pyaudio might need to be compiled from source since the versions listed on the link above are for windows
            * try using pyenv to install a different version of python on the system??
                * pyenv might not work
    
    * started here. because I'm on m1, realized I needed to install https://github.com/Homebrew/discussions/discussions/769
        * pyaudio was apparently working on older(3.6) and newer(3.9) versions of python
            * need to install pyenv to install different versions of python
            * pyenv doesn't natively support apple silicon yet, needs rosetta2 translation (hopefully)
    1. if you're on m1, install x86_64 version of homebrew with: `arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
    2. install pyenv as x86_64 binary with: `arch -x86_64 /usr/local/bin/brew install pyenv`
        * the whole path to x86_64 brew must be included `/usr/local/bin/brew`