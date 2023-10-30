import cv2

# Open a video capture object (0 corresponds to the default camera)
cap = cv2.VideoCapture(0)

# Define the coordinates and size of the original rectangle (x, y, width, height)
x, y, width, height = 100, 100, 200, 150

while True:
    # Read a frame from the video capture
    ret, frame = cap.read()

    # If the frame is not read properly, break the loop
    if not ret:
        break

    cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)

    center_x, center_y = x + width // 2, y + height // 2

    cv2.line(frame, (center_x, y), (center_x, height + y), (0, 255, 0), 2)
    cv2.line(frame, (x, center_y), (x + width, center_y), (0, 255, 0), 2)

    x, y = 300, 200  # Example coordinates
    radius = 5  # Radius of the circle representing the point

    # Draw a point on the frame
    cv2.circle(frame, (x, y), radius, (0, 0, 255), -1)

    # Display the frame with the rectangles and lines
    cv2.imshow('Video with Rectangles and Lines', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
