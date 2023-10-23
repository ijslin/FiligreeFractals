from PIL import Image


def split_image(image):
    width, height = image.size
    half_width = width // 2
    half_height = height // 2

    # Define the coordinates of the four quadrants
    quadrants = [
        (0, 0, half_width, half_height),  # Top-left
        (half_width, 0, width, half_height),  # Top-right
        (0, half_height, half_width, height),  # Bottom-left
        (half_width, half_height, width, height)  # Bottom-right
    ]

    # Create a list to store the quadrant images
    quadrant_images = []

    # Crop the image into quadrants
    for quadrant_coords in quadrants:
        quadrant = image.crop(quadrant_coords)
        quadrant_images.append(quadrant)

    return quadrant_images


def apply_image_processing(image):
    # Example image processing: Convert the image to grayscale
    return image.convert("L")


def recursive_image_processing(image, depth):
    if depth == 0:
        return image

    # Split the image into quadrants
    quadrants = split_image(image)

    # Apply image processing to each quadrant
    processed_quadrants = []
    for i, quadrant in enumerate(quadrants):
        print(f"Processing quadrant {i + 1} at depth {depth}")
        processed_quadrant = apply_image_processing(quadrant)
        processed_quadrants.append(recursive_image_processing(processed_quadrant, depth - 1))

    # Reassemble the processed quadrants into a new image
    result_image = Image.new("L", image.size)
    for i, processed_quadrant in enumerate(processed_quadrants):
        result_image.paste(processed_quadrant, (i % 2 * image.width // 2, i // 2 * image.height // 2))

    return result_image


if __name__ == "__main__":
    # Load your image
    input_image = Image.open("Filigree.png")

    # Set the depth of recursion (adjust as needed)
    recursion_depth = 3

    # Call the recursive image processing algorithm on the entire image
    output_image = recursive_image_processing(input_image, recursion_depth)

    # Save or display the resulting image
    output_image.save("FiligreeGray.png")
    output_image.show()
