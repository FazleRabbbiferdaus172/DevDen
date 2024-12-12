document.querySelectorAll('.side-nav').forEach(item => {
    item.addEventListener('click', function() {
      document.querySelector('.selected').classList.toggle('selected');
      this.classList.toggle('selected');
    });
  });

document.querySelectorAll('.tool-bar-item').forEach(item => {
    item.addEventListener('click', function(ev) {
      try{
        document.querySelector('.selected').classList.toggle('selected');
        localStorage.setItem("selectedToolId", ev.target.id);
      }
      catch (e) {}
      this.classList.toggle('selected');
    });
  });