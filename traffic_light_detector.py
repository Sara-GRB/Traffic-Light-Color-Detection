import cv2
import numpy as np

def detect_traffic_light_color(hsv_roi):
    # محدوده‌های رنگی برای قرمز، زرد و سبز
    red1 = cv2.inRange(hsv_roi, (0, 70, 50), (10, 255, 255))
    red2 = cv2.inRange(hsv_roi, (160, 70, 50), (180, 255, 255))
    red_mask = red1 | red2

    yellow_mask = cv2.inRange(hsv_roi, (15, 70, 50), (35, 255, 255))
    green_mask = cv2.inRange(hsv_roi, (40, 70, 50), (90, 255, 255))

    red_pixels = cv2.countNonZero(red_mask)
    yellow_pixels = cv2.countNonZero(yellow_mask)
    green_pixels = cv2.countNonZero(green_mask)

    if red_pixels > 150:
        return "RED"
    elif yellow_pixels > 150:
        return "YELLOW"
    elif green_pixels > 150:
        return "GREEN"
    else:
        return "UNKNOWN"

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    output = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # پیدا کردن دایره‌ها با Hough Transform
    circles = cv2.HoughCircles(
        blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
        param1=50, param2=30, minRadius=5, maxRadius=50
    )

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            # استخراج ناحیه دور دایره
            roi = frame[y - r:y + r, x - r:x + r]
            if roi.shape[0] == 0 or roi.shape[1] == 0:
                continue

            hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            color = detect_traffic_light_color(hsv_roi)

            # رسم دایره و رنگ تشخیص‌داده‌شده
            cv2.circle(output, (x, y), r, (0, 255, 0), 2)
            cv2.putText(output, color, (x - 10, y - r - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Traffic Light Detection", output)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
