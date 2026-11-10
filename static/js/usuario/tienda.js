function filtrarTienda(cat, btn) {
  document.querySelectorAll('.iq-shop-tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('#tiendaItemsGrid .iq-item-card').forEach(card => {
    if (cat === 'todos' || card.getAttribute('data-cat') === cat) {
      card.style.display = 'flex';
    } else {
      card.style.display = 'none';
    }
  });
}

function comprarItemTienda(itemKey) {
  const csrfMatch = document.cookie.match(/csrftoken=([^;]+)/);
  const csrfToken = csrfMatch ? csrfMatch[1] : '';

  const formData = new FormData();
  formData.append('item', itemKey);

  fetch('/api/tienda/canjear/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken,
    },
    body: formData,
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      if (data.vidas_actuales !== undefined && data.vidas_maximas !== undefined) {
        const el = document.getElementById('topbarEnergiaDisplay');
        if (el) el.textContent = `${data.vidas_actuales} / ${data.vidas_maximas}`;
      }
      if (data.oro !== undefined) {
        const el = document.getElementById('topbarOroDisplay');
        if (el) el.textContent = Number(data.oro).toLocaleString();
      }
      if (data.gemas !== undefined) {
        const el = document.getElementById('topbarGemasDisplay');
        if (el) el.textContent = Number(data.gemas).toLocaleString();
      }
      alert(data.message || '¡Operación realizada con éxito!');
    } else {
      alert(data.error || 'No se pudo completar la operación.');
    }
  })
  .catch(() => {
    alert('Error al comunicarse con el servidor.');
  });
}

window.comprarItemTienda = comprarItemTienda;
