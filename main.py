
import sys
from pathlib import Path

import volumehandcontroller


def main():

    print("=" * 45)
    print("       AI HAND GESTURE VOLUME CONTROLLER")
    print("=" * 45)

    print("\nStarting application...")
    print("Initializing hand tracking and volume control...\n")

    try:
        volumehandcontroller.main()

    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")

    except Exception as error:
        print(f"\nApplication error: {error}")
        raise

    finally:
        print("\nApplication closed successfully.")


if __name__ == "__main__":
    main()
