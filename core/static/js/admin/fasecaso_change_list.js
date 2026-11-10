function getCsrfToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    if (match) return match[1];
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    return input ? input.value : '';
  }

  function eliminarFase(faseId, titulo) {
    if (!confirm(`¿Estás seguro de que deseas eliminar la Fase "${titulo}"? Esta acción quedará registrada en auditoría.`)) {
      return;
    }

    const csrfToken = getCsrfToken();
    fetch(`/admin/core/fasecaso/${faseId}/delete-ajax/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/x-www-form-urlencoded',
      }
    })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        const card = document.getElementById(`card-fase-${faseId}`);
        if (card) {
          card.style.opacity = '0';
          card.style.transform = 'scale(0.9)';
          setTimeout(() => card.remove(), 250);
        }
      } else {
        alert(data.error || 'Error al eliminar la fase');
      }
    })
    .catch(err => {
      alert('Error en la comunicación con el servidor');
    });
  }
