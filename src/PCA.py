# from PIL import Image
# import imageio.v2 as imageio
# import cv2
# import numpy as np
# from sklearn.cluster import KMeans
# from sklearn.decomposition import PCA
# from collections import Counter
# import gc

# # Disable the safety check (use with caution!)
# Image.MAX_IMAGE_PIXELS = None

# # Or, set a higher limit
# Image.MAX_IMAGE_PIXELS = 1000000000  # Example: Allow up to 1 billion pixels

# def find_vector_set(diff_image, new_size):
#     vector_set = np.zeros((int(new_size[0] * new_size[1] / 25), 25))  # Preallocate the vector set
#     i = 0  # Index for filling the vector set

#     # Loop over the image in 5x5 blocks
#     for j in range(0, new_size[0] - 5 + 1, 5):  # Ensure j+5 does not exceed bounds
#         for k in range(0, new_size[1] - 5 + 1, 5):  # Ensure k+5 does not exceed bounds
#             block = diff_image[j:j+5, k:k+5]  # Extract 5x5 block
#             feature = block.ravel()  # Flatten the block into a 1D array
#             if feature.shape[0] == 25:  # Ensure the block is valid
#                 vector_set[i, :] = feature  # Add to the vector set
#                 i += 1  # Increment the index

#     # Trim unused rows in case the vector set is not fully populated
#     vector_set = vector_set[:i, :]  # Only keep valid rows
#     mean_vec = np.mean(vector_set, axis=0)  # Calculate the mean vector
#     vector_set = vector_set - mean_vec  # Normalize the vector set
#     gc.collect()
    
#     return vector_set, mean_vec

# def find_FVS(EVS, diff_image, mean_vec, new):
#     i = 2
#     feature_vector_set = []
 
#     while i < new[0] - 2:
#         j = 2
#         while j < new[1] - 2:
#             block = diff_image[i-2:i+3, j-2:j+3]
#             feature = block.flatten()
#             feature_vector_set.append(feature)
#             j = j+1
#         i = i+1
 
#     FVS = np.dot(feature_vector_set, EVS)
#     FVS = FVS - mean_vec
#     print(f"\nFeature vector space size: {FVS.shape}")
#     return FVS

# def clustering(FVS, components, new):
#     kmeans = KMeans(components, verbose=0)
#     kmeans.fit(FVS)
#     output = kmeans.predict(FVS)
#     count = Counter(output)

#     least_index = min(count, key=count.get)

#     # Ensure reshape dimensions match the output size
#     expected_size = (new[0] - 4) * (new[1] - 4)
#     print(f"Output size: {output.size}, Expected size: {expected_size}")
    
#     if output.size != expected_size:
#         raise ValueError(f"Cannot reshape: Output size {output.size} does not match the expected size {expected_size}")

#     # Reshape output correctly
#     change_map = np.reshape(output, (new[0] - 4, new[1] - 4))
#     return least_index, change_map

# def find_PCAKmeans(imagepath1, imagepath2):
#     # Load images
#     image1 = imageio.imread(imagepath1)
#     image2 = imageio.imread(imagepath2)

#     # Resize images
#     new_size = np.asarray(image1.shape) // 5  # Integer division for resizing
#     new_size = new_size * 5  # Ensure size is a multiple of 5
#     image1 = cv2.resize(image1, (new_size[1], new_size[0])).astype(np.int16)
#     image2 = cv2.resize(image2, (new_size[1], new_size[0])).astype(np.int16)

#     # Compute absolute difference
#     diff_image = abs(image1 - image2)

#     # Convert diff_image to 8-bit format and save it
#     diff_image_8bit = (diff_image / diff_image.max() * 255).astype(np.uint8)
#     diff_image_pil = Image.fromarray(diff_image_8bit)
#     diff_image_pil.save('diff.jpg')

#     # PCA and K-means clustering
#     vector_set, mean_vec = find_vector_set(diff_image, new_size)
#     pca = PCA()
#     pca.fit(vector_set)
#     EVS = pca.components_

#     FVS = find_FVS(EVS, diff_image, mean_vec, new_size)
#     components = 3
#     least_index, change_map = clustering(FVS, components, new_size)

#     # Post-process change map
#     change_map[change_map == least_index] = 255
#     change_map[change_map != 255] = 0

#     change_map = change_map.astype(np.uint8)
#     kernel = np.asarray(((0, 0, 1, 0, 0),
#                          (0, 1, 1, 1, 0),
#                          (1, 1, 1, 1, 1),
#                          (0, 1, 1, 1, 0),
#                          (0, 0, 1, 0, 0)), dtype=np.uint8)
#     cleanChangeMap = cv2.erode(change_map, kernel)

#     # Save maps as images
#     Image.fromarray(change_map).save("changemap.jpg")
#     Image.fromarray(cleanChangeMap).save("cleanchangemap.jpg")

# if __name__ == "__main__":
#     q = '/home/korotole/repos/vesuvius-challenge-study/src/ArcadiaLake1986.jpg'
#     p = '/home/korotole/repos/vesuvius-challenge-study/src/ArcadiaLake2011.jpg'
#     find_PCAKmeans(p,q)
from PIL import Image
import imageio.v2 as imageio
import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA
from collections import Counter
import gc

# Disable the safety check (use with caution!)
Image.MAX_IMAGE_PIXELS = None

# Or, set a higher limit
Image.MAX_IMAGE_PIXELS = 1000000000  # Example: Allow up to 1 billion pixels

def process_image_in_chunks(imagepath, chunk_size=(256, 256)):
    """Efficiently process large images by reading them in smaller chunks."""
    image = imageio.imread(imagepath)
    h, w, _ = image.shape
    for i in range(0, h, chunk_size[0]):
        for j in range(0, w, chunk_size[1]):
            chunk = image[i:i + chunk_size[0], j:j + chunk_size[1]]
            yield chunk

def find_vector_set(diff_image, new_size):
    vector_set = np.zeros((int(new_size[0] * new_size[1] / 25), 25))  # Preallocate the vector set
    i = 0  # Index for filling the vector set

    # Loop over the image in 5x5 blocks
    for j in range(0, new_size[0] - 5 + 1, 5):  # Ensure j+5 does not exceed bounds
        for k in range(0, new_size[1] - 5 + 1, 5):  # Ensure k+5 does not exceed bounds
            block = diff_image[j:j+5, k:k+5]  # Extract 5x5 block
            feature = block.ravel()  # Flatten the block into a 1D array
            if feature.shape[0] == 25:  # Ensure the block is valid
                vector_set[i, :] = feature  # Add to the vector set
                i += 1  # Increment the index

    # Trim unused rows in case the vector set is not fully populated
    vector_set = vector_set[:i, :]  # Only keep valid rows
    mean_vec = np.mean(vector_set, axis=0)  # Calculate the mean vector
    vector_set = vector_set - mean_vec  # Normalize the vector set
    gc.collect()
    
    return vector_set, mean_vec

def find_FVS(EVS, diff_image, mean_vec, new):
    i = 2
    feature_vector_set = []
 
    while i < new[0] - 2:
        j = 2
        while j < new[1] - 2:
            block = diff_image[i-2:i+3, j-2:j+3]
            feature = block.flatten()
            feature_vector_set.append(feature)
            j = j+1
        i = i+1
 
    FVS = np.dot(feature_vector_set, EVS)
    FVS = FVS - mean_vec
    print(f"\nFeature vector space size: {FVS.shape}")
    return FVS

def clustering(FVS, components, new):
    kmeans = MiniBatchKMeans(n_clusters=components, batch_size=1000, verbose=0)
    kmeans.fit(FVS)
    output = kmeans.predict(FVS)
    count = Counter(output)

    least_index = min(count, key=count.get)

    # Ensure reshape dimensions match the output size
    expected_size = (new[0] - 4) * (new[1] - 4)
    print(f"Output size: {output.size}, Expected size: {expected_size}")
    
    if output.size != expected_size:
        raise ValueError(f"Cannot reshape: Output size {output.size} does not match the expected size {expected_size}")

    # Reshape output correctly
    change_map = np.reshape(output, (new[0] - 4, new[1] - 4))
    return least_index, change_map

def find_PCAKmeans(imagepath1, imagepath2):
    # Process images in chunks to avoid memory overload
    for chunk1, chunk2 in zip(process_image_in_chunks(imagepath1), process_image_in_chunks(imagepath2)):
        # Resize chunk if necessary (resize per chunk, not the whole image at once)
        new_size = np.asarray(chunk1.shape) // 5  # Integer division for resizing
        new_size = new_size * 5  # Ensure size is a multiple of 5
        chunk1_resized = cv2.resize(chunk1, (new_size[1], new_size[0])).astype(np.int16)
        chunk2_resized = cv2.resize(chunk2, (new_size[1], new_size[0])).astype(np.int16)

        # Compute absolute difference
        diff_image = abs(chunk1_resized - chunk2_resized)

        # Convert diff_image to 8-bit format and save it
        diff_image_8bit = (diff_image / diff_image.max() * 255).astype(np.uint8)
        diff_image_pil = Image.fromarray(diff_image_8bit)
        diff_image_pil.save('diff_chunk.jpg')

        # PCA and K-means clustering
        vector_set, mean_vec = find_vector_set(diff_image, new_size)
        pca = PCA(n_components=50)  # Reduce dimensions to speed up PCA
        pca.fit(vector_set)
        EVS = pca.components_

        FVS = find_FVS(EVS, diff_image, mean_vec, new_size)
        components = 3
        least_index, change_map = clustering(FVS, components, new_size)

        # Post-process change map
        change_map[change_map == least_index] = 255
        change_map[change_map != 255] = 0

        change_map = change_map.astype(np.uint8)
        kernel = np.asarray(((0, 0, 1, 0, 0),
                             (0, 1, 1, 1, 0),
                             (1, 1, 1, 1, 1),
                             (0, 1, 1, 1, 0),
                             (0, 0, 1, 0, 0)), dtype=np.uint8)
        cleanChangeMap = cv2.erode(change_map, kernel)

        # Save maps as images
        Image.fromarray(change_map).save("changemap_chunk.jpg")
        Image.fromarray(cleanChangeMap).save("cleanchangemap_chunk.jpg")

if __name__ == "__main__":
    q = '/home/korotole/repos/vesuvius-challenge-study/src/ArcadiaLake1986.jpg'
    p = '/home/korotole/repos/vesuvius-challenge-study/src/ArcadiaLake2011.jpg'
    find_PCAKmeans(p,q)
