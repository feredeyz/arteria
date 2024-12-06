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

            el.parentElement.replaceChildren(editButton, el);
        } else {
            alert("Failed to update post. Please try again.");
        }
    });
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

    el.parentElement.replaceChildren(submitEditButton, el);
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
}
