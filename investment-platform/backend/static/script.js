document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.category').forEach(category => {
    const header = category.querySelector('h2');
    header.addEventListener('click', () => {
      category.classList.toggle('open');
    });
  });
});

