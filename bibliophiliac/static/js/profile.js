let avatarImg = document.querySelector('.form_input #avatar #avatar_img');
let addImg = document.querySelector('.form_input #add_img');
let avatarBtn = document.querySelector('.btn_container #avatar_btn');
let username = document.querySelector('.username #user_name');
let nameLabel = document.querySelector('.username #name_label');
let nameChange = document.querySelector('.username #change_name');
let profileBtn = document.querySelector('.form_input #profile_btn');
let submitBtn = document.querySelector('.change_and_save #submit_btn');
let reviewedBooks = document.querySelector('.reviews_profile .books_reviewed #reviewed_books');
let showBooks = document.querySelector('.reviews_profile .books_reviewed #books');

reviewedBooks.addEventListener('click', () => {
    showBooks.classList.toggle('all_books');
});


addImg.addEventListener('input', () => {
    previewProfileImage(document.querySelector('#add_img'));
});
profileBtn.addEventListener('click', () => {
    avatarImg.addEventListener('click', () => {
        addImg.click();
    });
    avatarBtn.addEventListener('click', () => {
        addImg.click();
    });
    avatarBtn.classList.toggle('hidden');
    username.classList.toggle('hidden');
    nameLabel.classList.toggle('hidden');
    nameChange.classList.toggle('hidden');
    profileBtn.classList.toggle('hidden');           
    submitBtn.classList.toggle('hidden');
});
    

function previewProfileImage(uploader) {      
    if (uploader.files && uploader.files[0]) {
        avatarImg.setAttribute('src', window.URL.createObjectURL(uploader.files[0]));
    }
}
