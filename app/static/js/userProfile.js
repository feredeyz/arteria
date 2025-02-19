async function confirmEditting(el) {
    await fetch("/confirm-edit", {
        method: "POST",
        body: JSON.stringify({
          userId: el.name,
          content: [document.getElementById('desc-text').value, document.getElementById('username').value]
        }),
        headers: {
          "Content-Type": 'application/json'
        }
    }).then((res) => res.json()).then((msg) => {
      console.log(msg);
      
      if (msg.msg === "Username already taken.") {
        alert("Username already taken.");
      } else if (msg.msg === "ok") {
        alert('Success!');
        window.location.reload();
      }
    }).catch((err) => console.log(err))
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
const confirm = document.getElementById('confirm-button');
const username = document.getElementById('username');
const date = document.getElementById('date');

description.addEventListener('focus', function() {
  confirm.style.display = 'inline';
});

username.addEventListener('focus', function() {
  confirm.style.display = 'inline';
});

date.addEventListener('focus', function() {
  confirm.style.display = 'inline';
});

document.addEventListener('click', function() {
  if (!username.contains(event.target) && !date.contains(event.target) && !description.contains(event.target) && !confirm.contains(event.target)) {
    confirm.style.display = 'none';
  }
});

