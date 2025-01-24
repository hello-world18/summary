// GSAP Animations
window.onload = function() {
    gsap.from(".container", { 
        duration: 0.50, 
        opacity: 0, 
        y: -50 
    });
 
    gsap.from("h1", { 
        duration: 0.50, 
        opacity: 0, 
        y: -30, 
        delay: 0.1 
    });
 
    gsap.from("input", { 
        duration: 0.1, 
        opacity: 0, 
        y: -20, 
        stagger: 0.1,
        delay: 0.1
    });
 
    gsap.from("button", { 
        duration: 0.1, 
        opacity: 0, 
        y: -20, 
        delay: 0.1 
    });
 };
 