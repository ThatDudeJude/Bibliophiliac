let avatarImage = document.querySelector('#avatar-img');
let addImage = document.querySelector('#add-img');
let changeAvatarButton = document.querySelector('#avatar-btn');
let username = document.querySelector('.profile-name');
let nameLabel = document.querySelector('.name-label');
let nameChange = document.querySelector('.change-name');
let changeProfileButton = document.querySelector('#profile-btn');
let submitButton = document.querySelector('#submit-btn');


addImage.addEventListener('input', () => {
    previewProfileImage(document.querySelector('#add-img'))            
});                       
changeProfileButton.addEventListener('click', () => {
    avatarImage.addEventListener('click', () => {
        addImage.click()                                                
    });                
    changeAvatarButton.addEventListener('click', () => {
        addImage.click()                                                            
    });       
    
    changeAvatarButton.classList.toggle('hidden')
    username.classList.toggle('hidden')
    nameLabel.classList.toggle('hidden')
    nameChange.classList.toggle('hidden')
    changeProfileButton.classList.toggle('hidden')            
    submitButton.classList.toggle('hidden')
});
// add image preview 

function previewProfileImage(uploader) {
    // ensure file was selected
    if (uploader.files && uploader.files[0]) {
        avatarImage.setAttribute('src', window.URL.createObjectURL(uploader.files[0]));
    }
}