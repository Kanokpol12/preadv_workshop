import cv2
import numpy as np
import paho.mqtt.client as mqtt # type: ignore

# MQTT Setup
mqtt_broker = "_______________________"
mqtt_port = 1883
mqtt_topic = "________________________"

client = mqtt.Client()
client.connect(mqtt_broker, mqtt_port)

cap = cv2.VideoCapture(0)
alert_state = {"red": False, "blue": False, "green": False}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # สีแดง
    lower_red = np.array([155, 86, 159])
    upper_red = np.array([179, 255, 255])
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    red_area = cv2.countNonZero(mask_red)

    if red_area > 5000 and not alert_state["red"]:
        print("red")
        client.publish(mqtt_topic, "red")
        alert_state["red"] = True
    if red_area < 1000:
        alert_state["red"] = False

       # สีฟ้า
    lower_blue = np.array([100, 150, 100])
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    blue_area = cv2.countNonZero(mask_blue)

    if blue_area > 5000 and not alert_state["blue"]:
        print("blue")
        client.publish(mqtt_topic, "blue")
        alert_state["blue"] = True
    if blue_area < 1000:
        alert_state["blue"] = False

    # วาดขอบเขตสีแดง
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours_red:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "Red", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    # วาดขอบเขตสีฟ้า
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours_blue:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, "Blue", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # แสดงภาพจริง
    cv2.imshow("Color Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()