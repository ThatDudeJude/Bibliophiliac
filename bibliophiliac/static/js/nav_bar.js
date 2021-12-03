let burger = document.querySelector('.navbar .burger');
let nav_links = document.querySelector('.links')  
let drop_content = document.getElementsByClassName('dropdown-content')            
let btn_caret = document.getElementsByClassName('drop-btn')
burger.addEventListener('click', () => {                
    burger.classList.toggle('cross')
    nav_links.classList.toggle('show-links')                                
})

for (let i =0; i < btn_caret.length; i++) {
    btn_caret[i].addEventListener('click', () => {
        change_caret(drop_content[i], btn_caret[i])
        if (i == 0) {
            btn_caret[1].classList.toggle('not_clicked')
        }
    })    
}
                        
function change_caret(menu, btn ) {
    menu.classList.toggle('clicked')
    content = btn.innerHTML
    console.log('content', content)
    if (content.includes('down')) {
        content = content.replace('down', 'up')
    } else {
        content = content.replace('up', 'down')
    }
    btn.innerHTML = content
}