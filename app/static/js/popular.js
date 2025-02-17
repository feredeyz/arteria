function SubmitPostEdit(el) {
    const id = el.name;
    const text = document.querySelector(`textarea[name="${id}"]`);

    fetch('/edit-post', {
        method: "POST",
        body: JSON.stringify({
            id: id,
            content: text.value,
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(response => {
        if (response.ok) {
            text.readOnly = true;
            text.style = "background-color: rgba(0, 0, 0, 0);";

            const editButton = document.createElement('button');
            editButton.id = "edit-post-button";
            editButton.name = id;
            editButton.innerHTML = '<img src="/static/styles/images/edit.png">';
            editButton.onclick = () => editPost(editButton);
            editButton.style = `
                display: flex;
                justify-content: center;
                align-items: center;
                width: 2vw;
                height: 2vw;
                border-width: 0;
                border-radius: 10%;
                margin-right: 5px;`;
            editButton.children[0].style = `width: 1vw; height: 1vw;`;

            const deleteButton = document.querySelector('#delete-post-button');
            el.parentElement.replaceChildren(editButton, deleteButton);
        } else {
            alert("Failed to update post. Please try again.");
        }
    });
}

function addLike(el) {
    const userId = el.name;
    const postId = el.id;

    console.log("User ID:", userId, "Post ID:", postId);

    fetch('/add-like', {
        method: "POST",
        body: JSON.stringify({
            user: userId,
            post: postId
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(async (res) => {
        if (!res.ok) throw new Error(`Server error: ${res.status}`);
        return res.json();
    })
    .then((data) => {console.log("Response:", data); window.location.reload()})
    .catch((err) => console.error("Fetch error:", err));
}

function deleteLike(el) {
    const userId = el.getAttribute("name");
    const postId = el.getAttribute("id");

    console.log("User ID:", userId, "Post ID:", postId);

    fetch('/delete-like', {
        method: "POST",
        body: JSON.stringify({
            user: userId,
            post: postId
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => {
        if (!res.ok) throw new Error(`Server error: ${res.status}`);
        return res.json();
    })
    .then(data => {
        console.log("Response:", data);
        window.location.reload();
    })
    .catch(err => console.error("Fetch error:", err));
}



function editPost(el) {
    const id = el.name;
    const text = document.querySelector(`textarea[name="${id}"]`);
    text.readOnly = false;
    text.style = "background-color: rgba(0, 0, 0, 0.1);";
    text.focus();

    const submitEditButton = document.createElement('button');
    submitEditButton.id = "submit-edit-button";
    submitEditButton.name = id;
    submitEditButton.innerHTML = '<img src="/static/styles/images/check.png">';
    submitEditButton.onclick = () => SubmitPostEdit(submitEditButton);
    submitEditButton.style = `
        display: flex;
        justify-content: center;
        align-items: center;
        width: 2vw;
        height: 2vw;
        border-width: 0;
        border-radius: 10%;
        margin-right: 5px;`;
    submitEditButton.children[0].style = `width: 1vw; height: 1vw;`;

    const deleteButton = document.querySelector('#delete-post-button');
    el.parentElement.replaceChildren(submitEditButton, deleteButton);
}

function deletePost(el) {
    fetch('delete-post', {
        method: "DELETE",
        body: JSON.stringify({
            id: el.name,
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(() => {
        window.location.reload();
    })
};

document.querySelectorAll('#posts textarea').forEach( element => {
    if (element.scrollHeight < 500) {
        element.style.height = `${element.scrollHeight}px`;
    }
    else {
        element.style.height = '500px';
    }
  })