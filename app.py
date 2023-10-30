from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file:
            image = cv2.imdecode(
                np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR
            )

            # Defining image dimensions
            height, width, channels = image.shape

            # Scaling
            scale_x = 2
            scale_y = 2
            scaled_image = cv2.resize(
                image, (int(width * scale_x), int(height * scale_y))
            )

            # Rotation
            angle = 30
            rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
            rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

            # Translation
            tx = 50
            ty = 30
            translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
            translated_image = cv2.warpAffine(
                image, translation_matrix, (width, height)
            )

            # Shearing
            shear_matrix = np.float32([[1, 0.5, 0], [0.5, 1, 0]])
            sheared_image = cv2.warpAffine(image, shear_matrix, (width, height))

            # Display the original and transformed images
            plt.figure(figsize=(12, 4))
            plt.subplot(151), plt.imshow(
                cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            ), plt.title("Original")
            plt.subplot(152), plt.imshow(
                cv2.cvtColor(scaled_image, cv2.COLOR_BGR2RGB)
            ), plt.title("Scaled")
            plt.subplot(153), plt.imshow(
                cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB)
            ), plt.title("Rotated")
            plt.subplot(154), plt.imshow(
                cv2.cvtColor(translated_image, cv2.COLOR_BGR2RGB)
            ), plt.title("Translated")
            plt.subplot(155), plt.imshow(
                cv2.cvtColor(sheared_image, cv2.COLOR_BGR2RGB)
            ), plt.title("Sheared")
            plt.show()

            return render_template(
                "index.html", image_file="static/transformed_image.jpg"
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
