import { createPost } from "./post.js"

document.addEventListener("DOMContentLoaded", function() {
    loadPost(window.profileID);
    document.querySelector('#follow-button').onclick = () => {
        console.log('Button clicked')
        toggleFollow(window.profileID)
    }
})

function loadPost(profile_id) {
    fetch(`/posts/${profile_id}`)
    .then(request => request.json())
    .then(posts => {
        console.log(posts);
        posts.forEach(post => createPost(post, '#posts-view-by-profile'))
    })
}

function toggleFollow(profile_id) {
    fetch(`/user/${profile_id}/toggleFollow`, {
        method: "POST"
    })
    .then(location.reload())
}