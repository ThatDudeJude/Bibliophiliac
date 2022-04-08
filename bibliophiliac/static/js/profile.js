let avatarImage = document.querySelector('#avatar-img');
let addImage = document.querySelector('#add-img');
let changeAvatarButton = document.querySelector('#avatar-btn');
let username = document.querySelector('.profile-name');
let nameLabel = document.querySelector('.name-label');
let nameChange = document.querySelector('.change-name');
let changeProfileButton = document.querySelector('#profile-btn');
let submitButton = document.querySelector('#submit-btn');
let cancelButton = document.querySelector('#cancel-btn');

let navAvatar = document.querySelector('#nav-avatar')

avatarImage.src = avatarImage.src + "?" +new Date().getTime()
navAvatar.src = avatarImage.src


addImage.addEventListener('input', () => {    
    
    previewProfileImage(document.querySelector('#add-img')) ;
});                       
changeProfileButton.addEventListener('click', () => {
    avatarImage.addEventListener('click', () => {
        addImage.click();                                               
    });                
    changeAvatarButton.addEventListener('click', () => {
        addImage.click();
    });       
    
    changeAvatarButton.classList.toggle('hidden')
    username.classList.toggle('hidden')
    nameLabel.classList.toggle('hidden')
    nameChange.classList.toggle('hidden')
    changeProfileButton.classList.toggle('hidden')            
    submitButton.classList.toggle('hidden')
    cancelButton.classList.toggle('hidden')
});
cancelButton.addEventListener('click', () => {
    avatarImage.removeEventListener('click', () => {
        addImage.click()                                                
    });                
    changeAvatarButton.removeEventListener('click', () => {
        addImage.click()                
    });       
    
    changeAvatarButton.classList.toggle('hidden');
    username.classList.toggle('hidden');
    nameLabel.classList.toggle('hidden');
    nameChange.classList.toggle('hidden');
    changeProfileButton.classList.toggle('hidden');
    submitButton.classList.toggle('hidden');
    cancelButton.classList.toggle('hidden');
})
// add image preview 



    
function previewProfileImage(uploader, currentImage) {
    // ensure file was selected
    if (uploader.files && uploader.files[0]) {
        avatarImage.setAttribute('src', window.URL.createObjectURL(uploader.files[0]));
    } 
}