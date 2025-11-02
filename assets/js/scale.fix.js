(function(document, window) {
    'use strict';
    
    // Viewport management for iOS devices
    var metas = document.getElementsByTagName('meta');
    var viewportMeta;
    
    // Find viewport meta tag
    for (var i = 0; i < metas.length; i++) {
        if (metas[i].name === "viewport") {
            viewportMeta = metas[i];
            break;
        }
    }
    
    var changeViewportContent = function(content) {
        if (viewportMeta) {
            viewportMeta.content = content;
        }
    };
    
    var initialize = function() {
        changeViewportContent("width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no");
    };
    
    var gestureStart = function() {
        changeViewportContent("width=device-width, minimum-scale=0.25, maximum-scale=1.6");
    };
    
    var gestureEnd = function() {
        initialize();
    };
    
    // iOS specific viewport handling
    if (navigator.userAgent.match(/iPhone/i) || navigator.userAgent.match(/iPad/i)) {
        initialize();
        document.addEventListener("touchstart", gestureStart, false);
        document.addEventListener("touchend", gestureEnd, false);
    }
    
    // Responsive navigation handling
    var handleResponsiveLayout = function() {
        var width = window.innerWidth || document.documentElement.clientWidth;
        var header = document.querySelector('header');
        var section = document.querySelector('section');
        
        // Add or remove mobile class based on viewport width
        if (width <= 960) {
            document.body.classList.add('mobile-view');
        } else {
            document.body.classList.remove('mobile-view');
        }
    };
    
    // Smooth scroll for anchor links
    var smoothScroll = function(target) {
        var targetElement = document.querySelector(target);
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    };
    
    // Handle navigation clicks
    var initSmoothScrolling = function() {
        var links = document.querySelectorAll('a[href^="#"]');
        for (var i = 0; i < links.length; i++) {
            links[i].addEventListener('click', function(e) {
                var href = this.getAttribute('href');
                if (href !== '#' && href.length > 1) {
                    e.preventDefault();
                    smoothScroll(href);
                }
            });
        }
    };
    
    // Image lazy loading for better performance
    var initLazyLoading = function() {
        var images = document.querySelectorAll('img[data-src]');
        
        if ('IntersectionObserver' in window) {
            var imageObserver = new IntersectionObserver(function(entries, observer) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        var img = entry.target;
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        imageObserver.unobserve(img);
                    }
                });
            });
            
            images.forEach(function(img) {
                imageObserver.observe(img);
            });
        } else {
            // Fallback for browsers without IntersectionObserver
            images.forEach(function(img) {
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
            });
        }
    };
    
    // Handle window resize with debouncing
    var resizeTimer;
    var handleResize = function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            handleResponsiveLayout();
        }, 250);
    };
    
    // Initialize on DOM ready
    var init = function() {
        handleResponsiveLayout();
        initSmoothScrolling();
        initLazyLoading();
        
        // Add event listeners
        window.addEventListener('resize', handleResize, false);
        window.addEventListener('orientationchange', handleResponsiveLayout, false);
        
        // Handle back/forward navigation
        window.addEventListener('pageshow', function(event) {
            if (event.persisted) {
                handleResponsiveLayout();
            }
        });
    };
    
    // Run initialization when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
})(document, window);