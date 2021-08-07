import { createPost } from "./post.js"

document.addEventListener("DOMContentLoaded", function() {
    loadFollowing()
    document.querySelector('#compose-post').onsubmit = post;

})

function loadFollowing() {
    fetch('/following')
    .then(response => response.json())
    .then(posts => {
        console.log(posts);
        posts.forEach(post => createPost(post, '#following-view'))
    })
}
