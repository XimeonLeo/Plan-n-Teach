async function deleteNote(note_id) {
  // Confirm deletion with the user
  if (confirm('Are you sure you want to delete this note?')) {
    try {
      // Send a POST request to delete the note
      const response = await fetch('/delete-note', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ note_id: note_id }),
      });

      if (!response.ok) {
        throw new Error('Failed to delete note. Server responded with status ' + response.status);
      }

      // Redirect to dashboard after successful deletion
      window.location.href = '/dashboard';
    } catch (error) {
      console.error('Error deleting note:', error.message);
      alert('An error occurred while deleting the note. Please try again later.');
    }
  }
}



// Select element function
const selectElement = function (element) {
	return document.querySelector(element);
};

let menuToggler = selectElement('.menu-toggle');
let body = selectElement('body');

menuToggler.addEventListener('click', function () {
	body.classList.toggle('open');
});

// Scroll reveal
window.sr = ScrollReveal();

sr.reveal('.animate-left', {
	origin: 'left',
	duration: 1000,
	distance: '25rem',
	Delay: 300
});

sr.reveal('.animate-right', {
	origin: 'right',
	duration: 1000,
	distance: '25rem',
	delay: 600
});

sr.reveal('.animate-top', {
	origin: 'top',
	duration: 1000,
	distance: '25rem',
	delay: 600
});

sr.reveal('.animate-bottom', {
	origin: 'bottom',
	duration: 1000,
	distance: '25rem',
	Delay: 600
});
