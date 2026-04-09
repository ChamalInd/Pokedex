function swapImage(image) {
    const img = document.getElementById('pokemon-img');
    
    if (image === 'norm') {
        img.src = img.getAttribute('data-norm');
    } else {
        img.src = img.getAttribute('data-shiny');
    }
}