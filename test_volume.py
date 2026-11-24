
from pycaw.pycaw import AudioUtilities

# Get default speakers.
device = AudioUtilities.GetSpeakers()

# Get endpoint volume.
volume = device.EndpointVolume

# Read current volume.
current_volume = volume.GetMasterVolumeLevelScalar()

# Read volume range.
min_vol, max_vol, step = volume.GetVolumeRange()

print("Audio Device:", device.FriendlyName)
print("Current Volume:", round(current_volume * 100, 2), "%")
print("Minimum Volume:", min_vol, "dB")
print("Maximum Volume:", max_vol, "dB")

# Set volume to 50%.
volume.SetMasterVolumeLevelScalar(0.5, None)

print("Volume successfully changed to 50%.")
