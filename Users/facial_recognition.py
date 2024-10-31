# import face_recognition
# import os

# # Specify the path to the model files
# MODEL_DIR = os.path.join("C:/Users/Zeineb Ben Mami/Documents/Django/backold/Cleverio_Backend/media/models")

# face_detector_model = os.path.join(MODEL_DIR, "shape_predictor_68_face_landmarks.dat")
# face_recognition_model = os.path.join(MODEL_DIR, "dlib_face_recognition_resnet_model_v1.dat")

# # Load models (modify this depending on how you intend to use face_recognition)
# def load_face_models():
#     try:
#         # Initialize face detection and encoding models
#         face_detector = face_recognition.face_landmarks_model(face_detector_model)
#         face_encoder = face_recognition.face_recognition_model(face_recognition_model)
#         print("Models loaded successfully.")
#     except Exception as e:
#         print("Error loading models:", str(e))

# # Example usage of the model
# def recognize_face(image_path):
#     load_face_models()
#     # Your face recognition logic goes here
#     image = face_recognition.load_image_file(image_path)
#     encodings = face_recognition.face_encodings(image)
#     if encodings:
#         print("Face encoding generated successfully.")
#     else:
#         print("No face found.")

# # Testing with a sample image
# if __name__ == "__main__":
#     test_image_path = "C:/path/to/your/test/image.jpg"  # Replace with the actual path to a test image
#     recognize_face(test_image_path)
