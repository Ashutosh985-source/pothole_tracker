import cv2


class PotholeDetector:

    def detect(self, image_path):
        img = cv2.imread(image_path)

        if img is None:
            return False, None

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)

        contours, _ = cv2.findContours(
            edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        detected = False

        for cnt in contours:
            area = cv2.contourArea(cnt)

            if area > 500:
                detected = True
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(
                    img, (x, y), (x + w, y + h), (0, 255, 0), 2
                )

        return detected, img
