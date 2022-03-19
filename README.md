# ga-synth
Neural Network & Genetic Algorithm Synthesizer using Native Instruments Massive (or puredata via OSC?)
---

Goal of the project: Reproduct the input sound to the best of the network's ability, do not attempt to preprocess the input sound in any way. 

---

* Neural Network for heavy lifting (getting the sound as close as possible to the target sound)
* GA for fine-tuning minizing the patch loss as close as possible

## current challenges

### 3/18/21
* What is the best way to train the network?
    1. send MIDI to Massive
    2. record output from Massive
    3. give the data to the model:
        1. convert the data to a spectrogram, so the network processes images
        2. process the raw audio data
    4. the model outputs the parameters for Massive to achieve the sound

### 8/12/21
* switched to using conda, because its the official method of getting tensorflow to work on M1. 
    * source: https://developer.apple.com/metal/tensorflow-plugin/
* anaconda (source for conda packages) issues:
    * rtmidi isn't a package in anaconda, yet
    * conda environment causes issues for sounddevice underlying libraries
* installed a new virtual environment in this repo called "venv"
    * contains the higher-performance edition of tensorflow 
    * however, doesn't work with sounddevice

### 7/28/21
* silence in the start of the sound need to be removed
    * https://youtu.be/at2NppqIZok contains a method for detecting the start of an audio sample and removing the silence from the start of the sample
    * for now, I'll manually trim the audio samples to ensure the GA will work

## ideas

### 8/12/21
* a possible model architecture to try, in keras: 
    * https://github.com/ruohoruotsi/LSTM-Music-Genre-Classification/blob/master/lstm_genre_classifier_keras.py
    * https://medium.com/in-pursuit-of-artificial-intelligence/deep-learning-using-raw-audio-files-66d5e7bf4cca

### 7/28/21
* when comparing target audio file to the representative individual from the current population, can we compare individual directly to target audio? This would speed up the process of not having to re-write the current file to disk each time a new individual is generated.

### 6/17/21
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