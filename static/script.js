// Enabling tool tips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

// pagination for moves
let current_page = 0;
let pages = document.querySelectorAll('.page');
let indicator = document.getElementById('page_indicator');
indicator.innerText = String(current_page + 1) + ' of ' + String(pages.length);

function swapImage(image) {
    const img = document.getElementById('pokemon-img');
    
    if (image === 'norm') {
        img.src = img.getAttribute('data-norm');
    } else {
        img.src = img.getAttribute('data-shiny');
    }
}

function randomFactGenerator() {
    let para = document.getElementById('placeholder');
    let random_facts = JSON.parse(para.dataset.flavours);
    let random_num = Math.floor(Math.random() * ((random_facts.length - 1) - 0 + 1)) + 0;
    
    para.innerText = random_facts[random_num];
}

function changePage(index) {
    let new_page = current_page + index;

    if (new_page >= 0 && new_page < pages.length) {
        pages[current_page].style.display = 'none';
        current_page = new_page;
        pages[current_page].style.display = 'block';
        indicator.innerText = String(current_page + 1) + ' of ' + String(pages.length);
    }
}