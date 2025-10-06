// Example interactivity for blog
document.addEventListener("DOMContentLoaded", function () {
    console.log("Django Blog JS Loaded");

    // Highlight posts on hover
    const posts = document.querySelectorAll(".post");
    posts.forEach(post => {
        post.addEventListener("mouseenter", () => {
            post.style.backgroundColor = "#eef";
        });
        post.addEventListener("mouseleave", () => {
            post.style.backgroundColor = "#fff";
        });
    });
});
