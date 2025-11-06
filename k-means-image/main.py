import numpy as np
from PIL import Image

def read_image(filename):
    img = Image.open(filename)
    img = img.convert('RGB')
    data = np.array(img)
    print(f"Image loaded: {filename}, shape: {data.shape}")
    return img, data

def flatten_image(data):
    w, h, c = data.shape
    flat = data.reshape((w * h, c))
    return flat

def kmeans(X, k, max_iters=10):
    np.random.seed(42)
    idx = np.random.choice(len(X), k, replace=False)
    centers = X[idx]
    for it in range(max_iters):
        dists = np.linalg.norm(X[:, None] - centers[None, :], axis=2)
        labels = np.argmin(dists, axis=1)
        new_centers = np.array([X[labels == i].mean(axis=0) if np.any(labels == i) else centers[i] for i in range(k)])
        if np.allclose(centers, new_centers):
            print(f"Converged at iteration {it}")
            break
        centers = new_centers
    return labels, centers

def recreate_image(labels, centers, shape):
    seg_data = centers[labels].astype(np.uint8)
    seg_img = seg_data.reshape(shape)
    return seg_img

def main():
    img_file = input("Enter image filename: ")
    k = int(input("Enter number of clusters (k): "))
    img, data = read_image(img_file)
    flat = flatten_image(data)
    labels, centers = kmeans(flat, k)
    seg_img = recreate_image(labels, centers, data.shape)
    out_img = Image.fromarray(seg_img)
    out_img.save('output_kmeans.jpg')
    print("Segmented image saved as output_kmeans.jpg")

if __name__ == "__main__":
    main()
