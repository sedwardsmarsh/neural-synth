# ga-synth

Neural Network & Genetic Algorithm Synthesizer using Native Instruments Massive (or puredata via OSC?)

---

Goal of the project: Reproduce the input sound to the best of the network's ability, do not attempt to preprocess the input sound in any way.

---

* Neural Network for heavy lifting (getting the sound as close as possible to the target sound)
* GA for fine-tuning minizing the patch loss as close as possible

```mermaid
graph LR
    A-->B
    B-->C
```

## starlog/TODO

### 5/7/22

* need to verify dataset generation isn't creating duplicate files

### 5/6/22

* Submitted `midterm.pdf` and stuff for cmpm152 midterm
* I'm wondering about model performance on raw audio buffer versus model performance on extracted features via librosa.
  * Maybe the model would benefit from having two heads (one for the raw audio buffer), one for the extracted features via librosa.
  * Another model arch could be to convert the sound files to spectrogram images and setup a series of convolutional layers to parse the spectrogram image. Then, using the extracted latent meaning, run that information through a series of dense layers and recurrent layers in parallel?
    * like the image in notability

### 4/29/22

* What do the predictions the model is making look like?
  * I tried model.predict(train_data[0]) but got the error:
    * `ValueError: Input 0 of layer sequential_25 is incompatible with the layer: : expected min_ndim=3, found ndim=2. Full shape received: (None, 2205)`

### 4/25/22

* Ideas from Brian:
  * is there a way to export automation series values from Ableton? In order to measure patches which modulate params over time.
  * extract features using librosa and feed those to the network?
    * <https://towardsdatascience.com/how-to-apply-machine-learning-and-deep-learning-methods-to-audio-analysis-615e286fcbbc>

### 4/22/22

* Hypothesis from Dad: the model will miss subtleties in the sound if two rendered audio buffers are not compared.
  * How will a network trained on just the knobs compare to a network trained by comparing audio (SNR loss).

### 4/20/22

* solved issue where custom optimizer wasn't working. Thank god
* Model architecture needs improvement.
  * Basic (stacked GRUs) model: MSE loss starts at 5k -> 1.3k. train/test accuracy doesn't budge

  *

### 4/17/22

* ~~copy normalization function from cmpm 152 notebook~~

### 4/11/22

* Had a very enlightening conversation with Ryan (stilgar) on discord. He suggested training the model to learn the parameter positions for each patch, instead of trying to input the model's predicted parameters into Massive and then measure the resulting ESR/SNR. This should work fine because the model will have the audio buffer as input and will definitely be differentiable, since we're not trying to convert the model predictions into some non-differentiable form i.e. running it thru Massive.
* Maybe using a genetic algorithm to train the network weights?
* This problem seems so close to being solvable, ESR would be the perfect way to measure loss! Except that the model isn't producing an audio signal, unlike Jatin's guitar pedal.
* converting a tensor to a numpy array is difficult <https://github.com/tensorflow/tensorflow/issues/28840>
  * I'm going to try eager execution to allow conversion from tensor to numpy array
* After reading SO and getting help from the tensorflow discord, it seems like reinforcement learning is the way to go. Apparently, this is because the "function" I need to use to convert the model parameters into a waveform via Massive is not differentiable, i.e. there's no way to measure what model outputs lead to lower ESR after plugging them into Massive.
  * Still going to try converting model parameters to numpy arrays and see where that goes.

### 4/7/22

* I'm asking for help on the tensorflow discord
* I'm thinking that a custom loss function is downstream of where I can convert the output of the model into audio signals to measure Error-to-Signal Ratio.
  * I'm looking into making a custom `train_step(self, data)` and by extension `Model.fit()`
* need to update installation instructions

### 4/6/22

* ~~Trying one last time to install sounddevice into tensorflow environment~~
  * ~~considering: alternative to sounddevice library~~
  * **FINALLY** got it working. I exported the `environment.yaml`, but here's the manual installation process:
        1. `pip install python-rtmidi soundfile scipy`
        2. `conda install -c conda-forge libsndfile`
* **I need a custom loss function (Error-to-Signal/Signal-Noise Ratio)**
  * I sketched a custom train loop iteration in noteability in the note "Tensorflow autosynth"
  * might be useful: <https://towardsdatascience.com/custom-loss-function-in-tensorflow-eebcd7fed17a>
* I need to implement a custom training loop
  * evaluate parameters in Massive by recording audio and measuring loss between recorded audio and target signal
* Getting `ValueError: No gradients provided for any variable`.
  * from reading SO, seems like its and issue when using non-differentiable functions in your loss fn.
  * I think this is a problem because I haven't truly implemented the proper loss function yet.

### 3/24/22

* InputLayer to the model is confusing. Omitting the batch size seems to fix things.
  * Wondering if `feature` in GRU/LSTM input requiremnts is the number of input features or a feature stream
* Might need to add a Flatten layer between GRU and Dense layers

### 3/19/22

* Decided to use two separate virtual environments:
  * one environment for generating dataset
    * `$ source audio_midi_venv/bin/activate`
    * its a python virtual environment called *audio_midi_venv*
  * one environment for training/inference with tensorflow
    * `$ conda activate env_tensorflow`
    * its a conda environment called *env_tensorflow*
      * installation process, following this video: <https://www.youtube.com/watch?v=oZjau-aUk0U&t=373s>
                1. install conda miniforge
                2. `$ conda create --name <venv name> python=3.9`
                3. `$ conda activate <venv name>`
                4. `$ conda install -c apple tensorflow-deps`
                5. `$ pip install tensorflow-macos`, this might fail. let it crash.
                6. `$ pip install tensorflow-metal`
                7. if crash when importing tensorflow, run: `$ pip install tensorflow-macos --no-dependencies`
                8. if crash when importing tensorflow for flatbuffers, run: `$ pip install flatbuffers --no-dependencies`

### 3/18/22

* soundfile will not install in the special tensorflow alpha m1 venv
  * resulting error: `OSError: sndfile library not found`, although it is installed.
* What is the best way to train the network?
    1. send MIDI to Massive
    2. record output from Massive
    3. give the data to the model:
        1. convert the data to a spectrogram, so the network processes images
        2. process the raw audio data
    4. the model outputs the parameters for Massive to achieve the sound

### 8/12/21

* switched to using conda, because its the official method of getting tensorflow to work on M1.
  * source: <https://developer.apple.com/metal/tensorflow-plugin/>
* anaconda (source for conda packages) issues:
  * rtmidi isn't a package in anaconda, yet
  * conda environment causes issues for sounddevice underlying libraries
* installed a new virtual environment in this repo called "venv"
  * contains the higher-performance edition of tensorflow
  * however, doesn't work with sounddevice

### 7/28/21

* silence in the start of the sound need to be removed
  * <https://youtu.be/at2NppqIZok> contains a method for detecting the start of an audio sample and removing the silence from the start of the sample
  * for now, I'll manually trim the audio samples to ensure the GA will work

## ideas

### 8/12/21

* a possible model architecture to try, in keras:
  * <https://github.com/ruohoruotsi/LSTM-Music-Genre-Classification/blob/master/lstm_genre_classifier_keras.py>
  * <https://medium.com/in-pursuit-of-artificial-intelligence/deep-learning-using-raw-audio-files-66d5e7bf4cca>

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

## installing requirements WARNING NOT UP TO DATE

 6/14/21

* recording audio with `sounddevice`!!!!
* `pyaudio` now magically installs on the default `python3 -m venv ...` created virtual environment!!?
        * decided to switch to using `sounddevice` instead of `pyaudio`, for the simpler interface and better documentation
  * virtual env. information
    * `Python 3.8.2 (v3.8.2:7b3ab5921f, Feb 24 2020, 17:52:18) [Clang 6.0 (clang-600.0.57)] on darwin`

PRE 6/14/21

* re-write for pytorch Big Sur apple silicon installation
* to install pyaudio, follow these requirements: <http://people.csail.mit.edu/hubert/pyaudio/>
  * when installing pyaudio using pip3 use the following command, updated from source: <https://stackoverflow.com/questions/33513522/when-installing-pyaudio-pip-cannot-find-portaudio-h-in-usr-local-include>
    * `pip3 install --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio`

  * Only installation succeeds using the above method. `pyaudio` fails when importing.
    * I think I need to re-install using an earlier version of python.
      * Based on this page: <https://pypi.org/project/PyAudio/#modal-close> I think only python 3.6 will work.
      * Additionally, pyaudio might need to be compiled from source since the versions listed on the link above are for windows
      * try using pyenv to install a different version of python on the system??
        * pyenv might not work

  * started here. because I'm on m1, realized I needed to install <https://github.com/Homebrew/discussions/discussions/769>
    * pyaudio was apparently working on older(3.6) and newer(3.9) versions of python
      * need to install pyenv to install different versions of python
      * pyenv doesn't natively support apple silicon yet, needs rosetta2 translation (hopefully)
    1. if you're on m1, install x86_64 version of homebrew with: `arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
    2. install pyenv as x86_64 binary with: `arch -x86_64 /usr/local/bin/brew install pyenv`
        * the whole path to x86_64 brew must be included `/usr/local/bin/brew`
