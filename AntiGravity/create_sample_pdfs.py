"""
Creates 2 realistic engineering PDF notes using PyMuPDF (fitz)
for demonstration and testing in the AI Smart Notes application.
"""
import fitz

def create_sample_pdf(filename, title, subject, semester, content_sections):
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # Standard A4 size
    
    y = 50
    # Title
    page.insert_text((50, y), title, fontsize=18, fontname="helv", color=(0.1, 0.2, 0.6))
    y += 25
    # Metadata
    page.insert_text((50, y), f"Course: {subject} | Level: {semester}", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
    y += 15
    page.insert_text((50, y), "Zeal College of Engineering & Research, Pune", fontsize=10, fontname="helv", color=(0.5, 0.5, 0.5))
    y += 25
    page.draw_line((50, y), (545, y), color=(0.8, 0.8, 0.8), width=1)
    y += 30

    for heading, paragraphs in content_sections:
        page.insert_text((50, y), heading, fontsize=13, fontname="helv", color=(0.15, 0.15, 0.15))
        y += 18
        for p in paragraphs:
            # Wrap text roughly to avoid spilling
            rect = fitz.Rect(50, y, 545, y + 80)
            page.insert_textbox(rect, p, fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2), align=0)
            y += 65
        y += 15

    doc.save(filename)
    doc.close()
    print(f"Created: {filename}")

if __name__ == "__main__":
    # Sample 1: Sem 3 Prerequisite Topic
    create_sample_pdf(
        "Sem3_Linear_Algebra_and_Matrices.pdf",
        "Linear Algebra: Matrix Transformations and Eigenvalues",
        "Engineering Mathematics III",
        "Semester 3",
        [
            ("1. Introduction to Matrix Transformations", [
                "A matrix transformation T: R^n -> R^m represents a linear mapping between vector spaces. For any vector x, T(x) = Ax where A is an m x n matrix.",
                "Properties include linearity: T(u + v) = T(u) + T(v) and T(c*u) = c*T(u) for all vectors u, v and scalar c."
            ]),
            ("2. Eigenvalues, Eigenvectors, and Diagonalization", [
                "An eigenvector of a square matrix A is a non-zero vector v such that A*v = lambda*v, where lambda is the scalar eigenvalue.",
                "Finding eigenvalues requires solving the characteristic equation det(A - lambda*I) = 0. Diagonalization decouples coupled linear systems."
            ]),
            ("3. Gradient and Partial Derivatives in Multivariable Systems", [
                "The gradient vector nabla f represents the direction of steepest ascent of a multivariable scalar function f(x1, x2, ... xn).",
                "Gradient descent is an iterative first-order optimization algorithm that steps in the negative gradient direction to find local minima."
            ])
        ]
    )

    # Sample 2: Sem 5 Current Topic (Builds upon Linear Algebra)
    create_sample_pdf(
        "Sem5_Deep_Learning_and_Neural_Networks.pdf",
        "Deep Learning: Multilayer Perceptrons and Backpropagation",
        "Artificial Intelligence & Machine Learning",
        "Semester 5",
        [
            ("1. Neural Network Architecture", [
                "A multilayer perceptron (MLP) consists of input, hidden, and output layers. Information propagation computes y = sigma(W*x + b), where W is the weight matrix and b is bias.",
                "Affine transformations in each layer rely fundamentally on linear algebra matrix-vector products followed by non-linear activation functions."
            ]),
            ("2. Optimization via Gradient Descent and Backpropagation", [
                "Backpropagation calculates the gradient of the loss function with respect to each weight via the chain rule of calculus: dL/dw = (dL/dy) * (dy/dz) * (dz/dw).",
                "Weights are updated iteratively using stochastic gradient descent (SGD): W_new = W_old - alpha * grad(Loss), minimizing cross-entropy or mean squared error."
            ]),
            ("3. Dimensionality Reduction & Latent Embeddings", [
                "Autoencoders and principal component projections rely on singular value decomposition (SVD) and matrix factorizations to map inputs into dense lower-dimensional vector spaces.",
                "These latent embeddings preserve geometric distances and semantic properties across large feature representations."
            ])
        ]
    )
