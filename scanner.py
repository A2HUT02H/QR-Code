import cv2, time
from datetime import datetime

# Camera to Room Mapping (only 1 camera for now)
camera_to_room_map = {0: "Room1", 1: "Room2"}

# Function to scan QR codes from a camera
def scan_qr_from_camera(camera_index):
    # Retrieve the room name based on camera index
    room = camera_to_room_map.get(camera_index, f"Room{camera_index}")
    
    # Initialize the video capture for the given camera index
    cap = cv2.VideoCapture(camera_index)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index}. Please check if the camera is connected.")
        return

    print(f"Scanning QR codes for {room}...")

    try:
        # Start an infinite loop to continuously scan for QR codes
        while True:
            ret, frame = cap.read()  # Capture a frame from the camera
            if not ret:
                print(f"Failed to grab frame from Camera {camera_index}.")
                break
            cv2.imshow("QR Scanner", frame)
            # Initialize the QR code detector
            detector = cv2.QRCodeDetector()
            # Try to detect and decode a QR code from the frame
            data, _, _ = detector.detectAndDecode(frame)

            # If QR code is detected
            if data:
                try:
                    # Split the decoded data into room and expiration time
                    detected_room, expiration_time_str = data.split('|')
                    print(f"Detected QR Code: Room = {detected_room}, Expiration = {expiration_time_str}")
                    
                    # Check if the detected room matches the current room and if the expiration time is valid
                    if detected_room == room and datetime.now() < datetime.strptime(expiration_time_str, "%d/%m/%Y %I:%M:%S %p"):
                        print(f"Valid QR code for {room}. Unlocking door...")
                    else:
                        print(f"Access Denied for {room}.")
                        time.sleep(0.5)
                except ValueError:
                    # Handle invalid QR code format
                    
                    print("Invalid QR code format.")
                    time.sleep(0.5)
            else:
                print("No QR code detected.")
                time.sleep(0.5)


            
            # Exit the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting QR scanner...")
                break
    finally:
        # Release the camera and close any OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

# Main entry point of the script
if __name__ == "__main__":
    # Start scanning for camera 0
    scan_qr_from_camera(0)