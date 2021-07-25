import { createPost } from "./post.js"

document.addEventListener("DOMContentLoaded",() => loadPost(window.profileID))

function loadPost(profile_id) {
    fetch(`/posts/${profile_id}`)
    .then(request => request.json())
    .then(posts => {
        console.log(posts);
        posts.forEach(post => createPost(post, '#posts-view-by-profile'))
    })
}