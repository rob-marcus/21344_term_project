from tf_bodypix.api import download_model, load_model, BodyPixModelPaths


# Set of valid image extensions to process.
IMG_EXTS = {".jpg", 
            ".jpeg", 
            ".tif", 
            ".tiff",
            ".png"}

# TODO
# Add video support. 

# Tensorflow stuff. 
# TODO
# Use the API to save this to the program folder
print("Loading model.")
bodypix_model = load_model(download_model(
    BodyPixModelPaths.MOBILENET_FLOAT_50_STRIDE_16
	))
print("Model loaded.")

