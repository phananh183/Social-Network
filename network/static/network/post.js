document.addEventListener('DOMContentLoaded', function() {
    //By default, load all posts
    loadAllPost();
    document.querySelector('#compose-post').onsubmit = post;
    })

function post() {
    const content = document.querySelector('#post-content').value
    fetch('/new-post', {
        method: "POST",
        body: JSON.stringify({
            content: content
        })
    })
    .then(response => response.json())
    .then(result => {console.log(result)})
    loadAllPost()
}

function loadAllPost() {
    fetch('/posts')
    .then(response => response.json())
    .then(posts => {
        console.log(posts);
        posts.forEach(post => createPost(post, '#posts-view'))
    })
}

//to create hmtl elements for a post
export function createPost(post, div_id) {
    var postItem = document.createElement('a')
    postItem.href = "#"
    postItem.className = "list-group-item"

    var div1 = document.createElement('div')
    div1.className = "d-flex w-100 justify-content-between"

    var poster = document.createElement('a')
    poster.className = "mb-1"
    poster.href = `/user/${post.posterID}`
    poster.innerHTML = post.poster
    var timestamp = document.createElement('small')
    timestamp.innerHTML = post.timestamp
    div1.append(poster, timestamp)

    var content = document.createElement('p')
    content.className = "mb-1"
    content.innerHTML = post.content
    var likes = document.createElement('small')
    likes.innerHTML = `${post.likes} likes`

    postItem.append(div1, content, likes)
    document.querySelector(div_id).append(postItem)
}