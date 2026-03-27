// main.js — students will add JavaScript here as features are built

// ------------------------------------------------------------------ //
// "See how it works" video modal                                       //
// ------------------------------------------------------------------ //

(function () {
    var YOUTUBE_URL = 'https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1';

    var modal   = document.getElementById('video-modal');
    var iframe  = document.getElementById('video-iframe');
    var openBtn = document.getElementById('how-it-works-btn');
    var closeBtn = document.getElementById('video-modal-close');
    var backdrop = modal && modal.querySelector('.video-modal-backdrop');

    if (!modal || !iframe || !openBtn) return;

    function openModal() {
        iframe.src = YOUTUBE_URL;
        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
        closeBtn.focus();
    }

    function closeModal() {
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
        // Clear src to stop video playback
        iframe.src = '';
    }

    openBtn.addEventListener('click', openModal);
    closeBtn.addEventListener('click', closeModal);
    backdrop.addEventListener('click', closeModal);

    // Close on Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('is-open')) {
            closeModal();
        }
    });
}());
