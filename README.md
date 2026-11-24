<<<<<<< HEAD

# Volume Hand Tracking 🎚️

A real-time hand gesture-based volume controller built using Python,
OpenCV, MediaPipe and Pycaw.

Control your Windows system volume using the distance between your
thumb and index finger.

## Features

- Real-time hand detection.
- 21-point hand landmark tracking.
- Thumb and index finger distance calculation.
- Gesture-based volume control.
- Real-time volume percentage display.
- Webcam-based interaction.

## Tech Stack

- Python
- OpenCV
- MediaPipe
- NumPy
- Pycaw
- COMTypes

## Project Structure

VOLUME-HAND-TRACKING/
│
├── handtrackingmodule.py
├── volumehandcontroller.py
├── requirements.txt
├── README.md
└── LICENSE

## Installation

Clone the repository:

```bash
git clone https://github.com/PranavChamoli06/VOLUME-HAND-TRACKING.git

cd VOLUME-HAND-TRACKING
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

Run the volume controller:

```bash
python volumehandcontroller.py
```

Move your thumb and index finger apart to increase volume.

Bring them closer to decrease volume.

Press `q` to exit.

## Platform Support

- Hand tracking: designed to work across platforms supported
  by OpenCV and MediaPipe.
- Volume control: Windows only, using Pycaw.

## License

This project is licensed under the MIT License.
=======
# Volume Hand Tracking

This project demonstrates hand tracking capabilities using OpenCV and MediaPipe in Python. It leverages MediaPipe's powerful machine learning models to detect and track hands in real-time video streams. This can be particularly useful for applications in gesture recognition, human-computer interaction, and augmented reality.

FEATURES:

- **Real-time Hand Detection**: Utilizes MediaPipe's hand tracking model to detect hands in video streams.
- **Hand Landmarks Visualization**: Displays 21 landmarks on each detected hand for detailed tracking.
- **Multiple Hands Support**: Capable of tracking multiple hands simultaneously.
- **Customizable**: Easy to modify and extend for applications like gesture recognition, sign language interpretation, or gaming.

REQUIREMENTS:

To run this project, you need:

- Python 3.6 or higher
- OpenCV
- MediaPipe

You can install the required packages using pip:

```bash
pip install opencv-python mediapipe
```

USUAGE:

1. Clone the repository or download the code files.
2. Run the script using Python.
3. Allow access to your camera when prompted.
4. The application will open a window showing the detected hands and their landmarks.

LICENSE

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
>>>>>>> origin/main
