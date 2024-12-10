document.querySelectorAll('.side-nav').forEach(item => {
    item.addEventListener('click', function() {
      document.querySelector('.selected').classList.toggle('selected');
      this.classList.toggle('selected');  // Toggles the 'selected' class on click
    });
  });

document.querySelectorAll('.tool-bar-item').forEach(item => {
  debugger
    item.addEventListener('click', function() {
      try{document.querySelector('.selected').classList.toggle('selected');}
      catch (e) {}
      this.classList.toggle('selected');  // Toggles the 'selected' class on click
    });
  });