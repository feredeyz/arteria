document.querySelectorAll('#addpost textarea').forEach(element => {
    element.style.height = 'auto';
    element.style.height = `${element.scrollHeight}px`;

    element.addEventListener('input', () => {
        element.style.height = 'auto';
        element.style.height = `${element.scrollHeight}px`; 
    });
});
