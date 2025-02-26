
const posts_elem = document.getElementById('posts');


async function show_test_p () {
    posts = await fetch('http://127.0.0.1:8000/blog/test/').then(response => response.json())
    console.log(posts)
    for (let i = 0; i < posts.length; i++) {
        posts_elem.innerHTML += `
        <div class="post">
            <h2>${posts[i].title}</h2>
            <p>${posts[i].content}</p>
        </div>
        `
    }
}

show_test_p();
