function deleteAllPosts() {
    fetch('/delete-all-posts', {
        method: "GET",
    })
}

function deleteAllUsers() {
    fetch('/delete-all-users', {
        method: "GET",
    })
}