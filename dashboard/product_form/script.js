document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('productForm');
    
    form.addEventListener('submit', (e) => {
        if (!validateForm()) {
            e.preventDefault();
        }
    });
});

function validateForm() {
    const productName = document.getElementById('product-name').value;
    const category = document.getElementById('product-category').value;
    const condition = document.getElementById('condition').value;
    const description = document.getElementById('description').value;
    const reason = document.getElementById('selling-reason').value;
    const image = document.getElementById('product-image').files[0];

    // Basic validation
    if (!image) {
        alert('Please upload a product image');
        return false;
    }

    if (productName.trim() === '') {
        alert('Please enter a product name');
        return false;
    }

    if (category === '') {
        alert('Please select a product category');
        return false;
    }

    if (condition === '') {
        alert('Please select product condition');
        return false;
    }

    if (description.trim() === '') {
        alert('Please enter product description');
        return false;
    }

    if (reason.trim() === '') {
        alert('Please enter reason for selling');
        return false;
    }

    // If valid, form will submit
    alert('Product added successfully!');
    form.reset();
    return true;
}