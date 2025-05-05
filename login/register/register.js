document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.registration-form');
    const formGroups = document.querySelectorAll('.form-group');
    const nextButtons = document.querySelectorAll('.next-button');
    const submitButton = document.querySelector('.submit-button');
    const progressBar = document.querySelector('.form-progress');
    const welcomeMessage = document.querySelector('.welcome-message');
    let currentStep = 0;

    // Initialize form
    formGroups[0].classList.add('active');
    updateProgress();

    // Next button functionality
    nextButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (validateCurrentStep()) {
                moveToNextStep();
            }
        });
    });

    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        if (validateCurrentStep()) {
            // In a real app, you would submit the form here
            showSuccessMessage();
        }
    });

    // Keyboard navigation
    form.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            if (currentStep < formGroups.length - 1) {
                if (validateCurrentStep()) {
                    moveToNextStep();
                }
            }
        }
    });

    function validateCurrentStep() {
        const currentInput = formGroups[currentStep].querySelector('.form-input');
        
        if (!currentInput.checkValidity()) {
            currentInput.reportValidity();
            return false;
        }
        return true;
    }

    function moveToNextStep() {
        formGroups[currentStep].classList.remove('active');
        currentStep++;
        
        if (currentStep < formGroups.length) {
            formGroups[currentStep].classList.add('active');
            updateProgress();
        }
    }

    function updateProgress() {
        const progressPercentage = (currentStep / (formGroups.length - 1)) * 100;
        progressBar.style.width = `${progressPercentage}%`;
    }

    function showSuccessMessage() {
        form.style.opacity = '0';
        form.style.transform = 'translateX(50%) scaleX(0)';
        form.style.transition = 'opacity 0.2s 0.1s, transform 0.3s';
        
        setTimeout(() => {
            form.style.display = 'none';
            welcomeMessage.style.opacity = '1';
            progressBar.style.width = '100%';
        }, 300);
    }

    // Input validation styling
    const inputs = document.querySelectorAll('.form-input');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value.trim() !== '') {
                this.setAttribute('data-filled', 'true');
            } else {
                this.removeAttribute('data-filled');
            }
        });
    });
});
