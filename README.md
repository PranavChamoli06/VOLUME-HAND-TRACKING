
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
