async function confirmEditting(el) {
    await fetch("/confirm-description-edit", {
        method: "POST",
        body: JSON.stringify({
          userId: el.name,
          content: document.getElementById('desc-text').value,
        }),
        headers: {
          "Content-Type": 'application/json'
        }
    });
}

async function changeAvatar(el) {
    const formData = new FormData();
    
    formData.append('image', el.files[0]); 
    formData.append('userId', el.id);

    await fetch('/change-avatar', {
      method: 'POST',
      body: formData,
    }).then(() => {
      window.location.reload();
    })
}

const description = document.getElementById('desc-text');
const descConfirm = document.getElementById('confirm-desc');

description.addEventListener('focus', function() {
  descConfirm.style.display = 'inline';
});

descConfirm.addEventListener('click', function() {
    descConfirm.style.display = 'none';
});

document.addEventListener('click', function() {
  if (!description.contains(event.target) && !descConfirm.contains(event.target)) {
    descConfirm.style.display = 'none';
  }
});

