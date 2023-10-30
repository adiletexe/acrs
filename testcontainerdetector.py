import cv2
import numpy as np
import math
import schedule

# Green color range in HSV
lower_green = np.array([70, 100, 100])
upper_green = np.array([140, 255, 255])

# Minimum contour area to consider
min_contour_area = 1000  # Adjust this value as needed

elements_array = None

# Mouse callback function to capture mouse events
def get_mouse_coordinates(event, x, y, flags, param):
    global elements_array
    if event == cv2.EVENT_LBUTTONDOWN:
        print(elements_array)
        print(f"Mouse coordinates: x={x}, y={y}")

# Create a window to display the webcam feed
cv2.namedWindow("Green Detection")

# Set up the mouse callback function
cv2.setMouseCallback("Green Detection", get_mouse_coordinates)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    height, width, _ = frame.shape

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv_frame, lower_green, upper_green)

    # Apply morphological operations to close gaps between green objects
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    large_contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]

    if large_contours:
        # Find the rotated bounding box that covers all detected large contours
        merged_contour = np.concatenate(large_contours)
        rect = cv2.minAreaRect(merged_contour)

        # Get the box coordinates and convert them to integers
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # print("BOX:", box)
        # print("FRAME:", frame)

        array_np = sorted(box, key=lambda point: point[1])
        elements_array = np.vstack(array_np)
        # print(elements_array)
        highest1 = elements_array[0]
        highest2 = elements_array[1]
        highest3 = elements_array[2]
        highest4 = elements_array[3]

        # ADILET YOU SHOULD ADJUST HERE!
        # 1) colors
        # 2) real sizes
        # 3) counters, validate(ignore multiple objects)
        # 4) fix sizes, adjust (Turn 45 left, right, depending on the distance between highest points)


        #IMPORTANT
        # сортировка идет по высоте по нарастающей

        # if (left top is higher and distance between left top and right top is small to avoid false left turn)
        if (highest1[0] < highest2[0]) and (math.sqrt((highest2[0] - highest1[0])**2 + (highest2[1] - highest1[1])**2) < math.sqrt((highest1[0] - highest3[0])**2 + (highest3[1] - highest1[1])**2)):
            hypothenuse = math.sqrt((highest1[0] - highest3[0]) ** 2 + (highest1[1] - highest3[1]) ** 2)
            angle = round(math.degrees(math.asin(math.fabs(highest1[1] - highest3[1]) / hypothenuse)))
            print("right", angle)

        # if (right top is higher and distance between right top and left top is small to avoid false right turn)
        elif (highest1[0] > highest2[0]) and (math.sqrt((highest1[0] - highest2[0])**2 + (highest2[1] - highest1[1])**2) < math.sqrt((highest1[0] - highest3[0])**2 + (highest3[1] - highest1[1])**2)):
            hypothenuse = math.sqrt((highest1[0] - highest3[0]) ** 2 + (highest1[1] - highest3[1]) ** 2)
            angle = round(math.degrees(math.asin(math.fabs(highest1[1] - highest3[1]) / hypothenuse)))
            print("left", angle)

        # if (left top is higher and length is up)
        elif (highest1[0] < highest2[0]):
            hypothenuse = math.sqrt((highest1[0] - highest2[0]) ** 2 + (highest1[1] - highest2[1]) ** 2)
            angle = round(math.degrees(math.asin(math.fabs(highest1[1] - highest2[1]) / hypothenuse)))
            print("left", angle)

        # if (right top is higher and length is up)
        elif (highest1[0] > highest2[0]):
            hypothenuse = math.sqrt((highest1[0]-highest2[0])**2 + (highest1[1]-highest2[1])**2)
            angle = round(math.degrees(math.asin(math.fabs(highest1[1] - highest2[1]) / hypothenuse)))
            print("right", angle)

        # # just an example
        # if (highest2[1] - highest1[1] >= 100) and (highest1[0] < highest2[0]) and (math.sqrt((highest2[0] - highest1[0])**2 + (highest2[1] - highest1[1])**2) < math.sqrt((highest1[0] - highest3[0])**2 + (highest3[1] - highest1[1])**2)):
        #     hypothenuse = math.sqrt((highest1[0] - highest3[0]) ** 2 + (highest1[1] - highest3[1]) ** 2)
        #     angle = round(math.degrees(math.asin(math.fabs(highest1[1] - highest3[1]) / hypothenuse)))
        #     print("right", angle)

        # # if highest are same and width < length
        # elif (highest2[1] - highest1[1] <= 20) and (math.fabs(highest1[0] - highest2[0]) < math.fabs(highest2[1] - highest4[1])):
        #     print("Turn 90")

        # find center
        diagonal_center_highest = [((highest1[0] + highest2[0])/2), ((highest1[1] + highest2[1])/2)]
        diagonal_center_lowest = [((highest3[0] + highest4[0]) / 2), ((highest3[1] + highest4[1]) / 2)]
        center = [((diagonal_center_highest[0] + diagonal_center_lowest[0]) / 2),
                  ((diagonal_center_highest[1] + diagonal_center_lowest[1]) / 2)]
        # print(center)

        left_bottom_not_rotated_corner = [(center[0] - math.fabs(highest1[0] - highest2[0]) / 2),
                                          (center[1] + math.fabs(highest1[1] - highest3[1]) / 2)]
        left_top_not_rotated_corner = [(center[0] - math.fabs(highest1[0] - highest2[0]) / 2),
                                          (center[1] - math.fabs(highest1[1] - highest3[1]) / 2)]
        right_bottom_not_rotated_corner = [(center[0] + math.fabs(highest1[0] - highest2[0]) / 2),
                                          (center[1] + math.fabs(highest1[1] - highest3[1]) / 2)]
        right_top_not_rotated_corner = [(center[0] + math.fabs(highest1[0] - highest2[0]) / 2),
                                           (center[1] - math.fabs(highest1[1] - highest3[1]) / 2)]




        # NOT USED first algorithm to find an angle by left bottom

        # hypothenuse = math.sqrt((left_bottom_not_rotated_corner[0] - highest3[0])**2 + (left_bottom_not_rotated_corner[1] - highest3[1])**2)

        # if (-1) < (left_bottom_not_rotated_corner[0] / hypothenuse) < 1:
        #     angle = round(math.degrees(math.asin(left_bottom_not_rotated_corner[0]/hypothenuse)))
        #     # print(angle)



        # NEW USED ALGORITHM FOR GETTING ANGLE
        # hypothenuse = math.sqrt((highest1[0]-highest2[0])**2 + (highest1[1]-highest2[1])**2)
        # angle = round(math.degrees(math.asin(math.fabs(highest1[1] - highest2[1]) / hypothenuse)))
        # print(angle)


        # find center another way
        # diagonal_center_highest1_highest3 = [((highest1[0] + highest3[0]) / 2), ((highest1[1] + highest3[1]) / 2)]
        # diagonal_center_highest2_highest4 = [((highest2[0] + highest4[0]) / 2), ((highest2[1] + highest4[1]) / 2)]
        # center2 = [((diagonal_center_highest1_highest3[0] + diagonal_center_highest2_highest4[0]) / 2), ((diagonal_center_highest1_highest3[1] + diagonal_center_highest2_highest4[1]) / 2)]

        #find area
        # area = math.sqrt((highest1[0] - highest2[0])**2 + (highest1[1] - highest2[1])**2) * math.sqrt((highest1[0] - highest3[0])**2 + (highest1[1] - highest3[1])**2)

        # draw a point at center of container
        x, y = round(center[0]), round(center[1])
        radius = 5
        cv2.circle(frame, (x, y), radius, (0, 0, 255), -1)

        # vertical line
        center_x = width // 2
        cv2.line(frame, (center_x, 0), (center_x, height), (255, 0, 0), 1)

        move_horizontal = int(center_x - center[0])
        # print(move_horizontal)

        # draw not rotated rectangle
        x1, y1, width1, height1 = round(left_top_not_rotated_corner[0]), round(left_top_not_rotated_corner[1]), round(math.fabs(left_top_not_rotated_corner[0] - right_top_not_rotated_corner[0])), round(math.fabs(left_top_not_rotated_corner[1] - left_bottom_not_rotated_corner[1]))
        # print(x1, y1, width1, height1)
        cv2.rectangle(frame, (x1, y1), (x1 + width1, y1 + height1), (0, 0, 255), 2)

        center_x1, center_y1 = x1 + width1 // 2, y1 + height1 // 2

        cv2.line(frame, (center_x1, y1), (center_x1, height1 + y1), (0, 0, 255), 2)
        cv2.line(frame, (x1, center_y1), (x1 + width1, center_y1), (0, 0, 255), 2)



        # Draw the rotated rectangle
        cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Green Detection", frame)
    cv2.imshow("Green Mask", result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
