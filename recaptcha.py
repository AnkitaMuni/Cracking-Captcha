import cv2
import numpy as np
import tensorflow as tf
from PIL import Image, ImageTk
import tkinter as tk

if __name__=='__main__':
    labels = ['Bicycle', 'Bridge', 'Bus', 'Car', 'Traffic Light']

    # Load the .h5 model
    model_path = 'recaptcha.h5'
    model = tf.keras.models.load_model(model_path)

    # Create Tkinter window
    root = tk.Tk()
    root.title('Image Grid')

    # Load the input image
    input_image_path = 'download.png'
    input_image = cv2.imread(input_image_path)  # Convert BGR to RGB
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

    input_image = 255 - input_image

    # Convert the input image to PhotoImage format for Tkinter
    input_image_pil = Image.fromarray((input_image * 255).astype(np.uint8))
    input_image_pil = input_image_pil.resize((224, 224))  # Resize for display
    input_image_tk = ImageTk.PhotoImage(input_image_pil)


    # Display the input image in Tkinter window
    label_input = tk.Label(root, image=input_image_tk)
    label_input.image = input_image_tk
    label_input.pack(padx=10, pady=10)

    # Calculate the dimensions for the sub-images
    num_rows, num_cols = 3, 3
    sub_image_size = 224
    input_height, input_width, _ = input_image.shape

    # Calculate the step size for splitting the image
    step_size_rows = input_height // num_rows
    step_size_cols = input_width // num_cols

    # Create a 3x3 grid for images and labels
    for i in range(3):
        frame = tk.Frame(root)
        frame.pack()

        for j in range(3):
            # Extract sub-image
            start_row, end_row = i * step_size_rows, (i + 1) * step_size_rows
            start_col, end_col = j * step_size_cols, (j + 1) * step_size_cols
            sub_image = input_image[start_row:end_row, start_col:end_col]

            # Convert sub-image to PhotoImage format
            sub_image_pil = Image.fromarray((sub_image * 255).astype(np.uint8))
            sub_image_pil = sub_image_pil.resize((100, 100))  # Resize for display
            sub_image_tk = ImageTk.PhotoImage(sub_image_pil)

            input_sub_image = cv2.resize(sub_image, (224, 224)) / 255.0  # Resize and normalize

            # Make predictions using the trained model
            class_probabilities = model.predict(np.expand_dims(input_sub_image, axis=0))
            predicted_class_index = np.argmax(class_probabilities)
            predicted_class_label = labels[predicted_class_index]

            # Display the sub-image in the grid
            label_sub_image = tk.Label(frame, image=sub_image_tk, text=predicted_class_label, compound='top')
            label_sub_image.image = sub_image_tk
            label_sub_image.grid(row=i, column=j, padx=5, pady=5)

    # Start the Tkinter event loop
    root.mainloop()
