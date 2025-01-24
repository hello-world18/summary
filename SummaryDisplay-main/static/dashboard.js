// Initialize GSAP ScrollTrigger
gsap.registerPlugin(ScrollTrigger);

// Hero Section Animation
gsap.from(".welcome-title", {
  duration: 1.2,
  opacity: 0,
  y: -50,
  ease: "power3.out"
});

// Staggered Card Animations
gsap.from(".card", {
  duration: 0.8,
  opacity: 0,
  y: 30,
  stagger: 0.2,
  ease: "power2.out",
  scrollTrigger: {
    trigger: ".card",
    start: "top 80%",
    toggleActions: "play none none reverse"
  }
});

// Table Row Animation
gsap.from("tbody tr", {
  duration: 0.6,
  opacity: 0,
  x: -30,
  stagger: 0.1,
  ease: "power2.out",
  scrollTrigger: {
    trigger: "table",
    start: "top 80%",
    toggleActions: "play none none reverse"
  }
});

// Button Hover Animation
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

  // Add ripple effect
  button.addEventListener('click', function(e) {
    let x = e.clientX - e.target.offsetLeft;
    let y = e.clientY - e.target.offsetTop;
    
    let ripple = document.createElement('span');
    ripple.style.left = `${x}px`;
    ripple.style.top = `${y}px`;
    
    this.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  });
});

// Smooth scroll animation for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      gsap.to(window, {
        duration: 1,
        scrollTo: target,
        ease: "power2.inOut"
      });
    }
  });
});

