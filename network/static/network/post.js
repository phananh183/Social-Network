document.addEventListener('DOMContentLoaded', function() {
    //By default, load all posts
    loadAllPost();
    document.querySelector('#compose-post').onsubmit = post;


    //Add event listener for 'following' button

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

export function loadAllPost() {
    fetch('/posts')
    .then(response => response.json())
    .then(posts => {
        console.log(posts);
        posts.forEach(post => createPost(post))
    })
}

//to create hmtl elements for a post
export function createPost(post) {
    postItem = document.createElement('a')
    postItem.href = "#"
    postItem.className = "list-group-item"

    div1 = document.createElement('div')
    div1.className = "d-flex w-100 justify-content-between"

    poster = document.createElement('a')
    poster.className = "mb-1"
    poster.href = `/user/${post.posterID}`
    poster.innerHTML = post.poster
    timestamp = document.createElement('small')
    timestamp.innerHTML = post.timestamp
    div1.append(poster, timestamp)

    content = document.createElement('p')
    content.className = "mb-1"
    content.innerHTML = post.content
    likes = document.createElement('small')
    likes.innerHTML = `${post.likes} likes`

    postItem.append(div1, content, likes)
    document.querySelector('#posts-view').append(postItem)
}

// export { createPost, loadAllPost }