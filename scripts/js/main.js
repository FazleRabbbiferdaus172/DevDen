console.log("hiiiiiiiiiiiiiii")
document.querySelectorAll('.side-nav').forEach(item => {
    item.addEventListener('click', function() {
      document.querySelector('.selected').classList.toggle('selected');
      this.classList.toggle('selected');  // Toggles the 'selected' class on click
    });
  });