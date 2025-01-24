// Register GSAP ScrollTrigger
gsap.registerPlugin(ScrollTrigger);

document.addEventListener('DOMContentLoaded', () => {
    // Initialize animations
    initializeAnimations();
    // Add event listeners
    setupEventListeners();
});

function initializeAnimations() {
    // Header animation
    gsap.from(".page-header", {
        duration: 1,
        y: -30,
        opacity: 0,
        ease: "power3.out"
    });

    // Card animation
    gsap.from(".update-user-section", {
        duration: 0.8,
        y: 30,
        opacity: 0,
        ease: "power2.out",
        scrollTrigger: {
            trigger: ".update-user-section",
            start: "top 80%"
        }
    });

    // Form fields animation
    gsap.from(".form-group", {
        duration: 0.5,
        y: 20,
        opacity: 0,
        stagger: 0.1,
        ease: "power2.out",
        delay: 0.5
    });
}

function setupEventListeners() {
    // Button hover animations
    document.querySelectorAll('.button').forEach(button => {
        button.addEventListener('mouseover', () => {
            gsap.to(button, {
                scale: 1.05,
                duration: 0.3,
                ease: "power2.out"
            });
        });

        button.addEventListener('mouseout', () => {
            gsap.to(button, {
                scale: 1,
                duration: 0.3,
                ease: "power2.out"
            });
        });
    });

    // Form validation feedback
    const form = document.querySelector('.update-user-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            if (!form.checkValidity()) {
                e.preventDefault();
                
                // Animate invalid fields
                const invalidFields = form.querySelectorAll(':invalid');
                invalidFields.forEach(field => {
                    gsap.to(field, {
                        x: [-10, 10, -10, 10, 0],
                        duration: 0.4,
                        ease: "power2.out"
                    });
                });
            }
        });
    }
}