let currentPage = 1;
const pageSize = 5; // 5 cartas por página como en la vista original
const blockSize = 20; // Bloques de hasta 20 números para que no se salgan de la pantalla

function showToast(msg) {
  const toast = document.getElementById('iqToast');
  if (!toast) return;
  document.getElementById('toastMessage').textContent = msg;
  toast.classList.add('show');
  setTimeout(() => { toast.classList.remove('show'); }, 3500);
}

function closeModal(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = 'none';
}

function openNewCartaModal() {
  const form = document.getElementById('formNewCarta');
  if (form) form.reset();
  const modal = document.getElementById('modalNewCarta');
  if (modal) modal.style.display = 'flex';
}

function applyCardsFilter() {
  const qInput = document.getElementById('searchCartaInput');
  const normaInput = document.getElementById('filterNorma');
  const estadoInput = document.getElementById('filterEstado');

  const q = (qInput ? qInput.value : '').trim().toLowerCase();
  const norma = normaInput ? normaInput.value : '';
  const est = estadoInput ? estadoInput.value : '';

  const cards = Array.from(document.querySelectorAll('.iq-carta-card'));
  let matched = [];

  cards.forEach(card => {
    const nom = card.getAttribute('data-nombre') || '';
    const nor = card.getAttribute('data-norma') || '';
    const con = card.getAttribute('data-concepto') || '';
    const e = card.getAttribute('data-estado') || '';

    const matchQ = !q || nom.includes(q) || nor.toLowerCase().includes(q) || con.includes(q);
    const matchNorma = !norma || nor === norma;
    const matchEstado = !est || e === est;

    if (matchQ && matchNorma && matchEstado) {
      matched.push(card);
    } else {
      card.style.display = 'none';
    }
  });

  const total = matched.length;
  const totalPages = Math.ceil(total / pageSize) || 1;
  if (currentPage > totalPages) currentPage = 1;

  const startIdx = (currentPage - 1) * pageSize;
  const endIdx = startIdx + pageSize;

  matched.forEach((card, idx) => {
    if (idx >= startIdx && idx < endIdx) {
      card.style.display = 'flex';
    } else {
      card.style.display = 'none';
    }
  });

  // Mostrar mensaje cuando 0 cartas coinciden con los filtros
  const noMatchEl = document.getElementById('noCardsMatch');
  if (noMatchEl) {
    noMatchEl.style.display = (total === 0 && cards.length > 0) ? 'block' : 'none';
  }

  // Actualizar resumen
  const elStart = document.getElementById('pagStart');
  const elEnd = document.getElementById('pagEnd');
  const elTotal = document.getElementById('pagTotal');

  if (elStart) elStart.textContent = total > 0 ? (startIdx + 1) : 0;
  if (elEnd) elEnd.textContent = Math.min(endIdx, total);
  if (elTotal) elTotal.textContent = total;

  // Renderizar botones de paginación en bloques de 20 (1..20, 20+, 40+, etc.)
  const pageButtonsContainer = document.getElementById('pageButtons');
  if (pageButtonsContainer) {
    let btns = '';

    const currentBlock = Math.floor((currentPage - 1) / blockSize);
    const startPage = currentBlock * blockSize + 1;
    const endPage = Math.min(totalPages, (currentBlock + 1) * blockSize);

    // Si estamos en un bloque posterior (pág 21+), botón para volver al bloque previo
    if (currentBlock > 0) {
      const prevBlockLast = startPage - 1;
      btns += `<button type="button" class="iq-page-btn iq-page-jump" title="Páginas anteriores (hasta pág. ${prevBlockLast})" onclick="goToPage(${prevBlockLast})">&laquo; ${prevBlockLast}</button>`;
    }

    // Páginas del bloque actual (ej: 1 al 20, 21 al 40)
    for (let p = startPage; p <= endPage; p++) {
      btns += `<button type="button" class="iq-page-btn ${p === currentPage ? 'active' : ''}" onclick="goToPage(${p})">${p}</button>`;
    }

    // Si hay más páginas después de este bloque, botón 20+, 40+, etc.
    if (endPage < totalPages) {
      btns += `<button type="button" class="iq-page-btn iq-page-jump" title="Más de ${endPage} páginas (ir a pág. ${endPage + 1})" onclick="goToPage(${endPage + 1})">${endPage}+</button>`;
    }

    pageButtonsContainer.innerHTML = btns;
  }
}

function goToPage(p) {
  currentPage = p;
  applyCardsFilter();
}

function prevPage() {
  if (currentPage > 1) {
    currentPage--;
    applyCardsFilter();
  }
}

function nextPage() {
  const cards = Array.from(document.querySelectorAll('.iq-carta-card'));
  const qInput = document.getElementById('searchCartaInput');
  const normaInput = document.getElementById('filterNorma');
  const estadoInput = document.getElementById('filterEstado');

  const q = (qInput ? qInput.value : '').trim().toLowerCase();
  const norma = normaInput ? normaInput.value : '';
  const est = estadoInput ? estadoInput.value : '';

  const matched = cards.filter(card => {
    const nom = card.getAttribute('data-nombre') || '';
    const nor = card.getAttribute('data-norma') || '';
    const con = card.getAttribute('data-concepto') || '';
    const e = card.getAttribute('data-estado') || '';
    return (!q || nom.includes(q) || nor.toLowerCase().includes(q) || con.includes(q)) &&
           (!norma || nor === norma) &&
           (!est || e === est);
  });

  const totalPages = Math.ceil(matched.length / pageSize) || 1;
  if (currentPage < totalPages) {
    currentPage++;
    applyCardsFilter();
  }
}

  // Modales Ver y Editar
  function openViewCartaModal(cartaId) {
    fetch(`/admin/core/carta/${cartaId}/detail-json/`)
      .then(res => res.json())
      .then(data => {
        if (!data.success) {
          showToast(data.error || 'Error');
          return;
        }
        const c = data.carta;
        document.getElementById('viewCartaBody').innerHTML = `
          <div style="display: flex; flex-direction: column; gap: 14px; align-items: center; text-align: center;">
            <div style="width: 100%; height: 160px; border-radius: 12px; overflow: hidden; position: relative; border: 1.5px solid #3b3378;">
              <img src="${c.imagen_url}" style="width: 100%; height: 100%; object-fit: cover;" alt="${c.nombre}" />
              <span class="iq-carta-iso-badge" style="font-size: 12px; padding: 4px 12px;">${c.norma_iso}</span>
            </div>
            <div>
              <h2 style="font-size: 18px; color: #ffffff; margin: 0;">${escapeHtml(c.nombre)}</h2>
              <div style="font-size: 12.5px; color: #c084fc; font-weight: 700; margin-top: 4px;">${escapeHtml(c.concepto)}</div>
              <p style="font-size: 12px; color: #94a3b8; margin: 8px 0 0 0; line-height: 1.4;">${escapeHtml(c.descripcion)}</p>
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; width: 100%;">
              <div style="background: #0f0d23; padding: 10px; border-radius: 8px; border: 1px solid #231d4e;">
                <span style="font-size: 11px; color: #94a3b8;">Fuerza</span>
                <div style="font-size: 15px; font-weight: 800; color: #c084fc; margin-top: 2px;">⚡ ${c.fuerza}</div>
              </div>
              <div style="background: #0f0d23; padding: 10px; border-radius: 8px; border: 1px solid #231d4e;">
                <span style="font-size: 11px; color: #94a3b8;">Defensa</span>
                <div style="font-size: 15px; font-weight: 800; color: #818cf8; margin-top: 2px;">🛡️ ${c.defensa}</div>
              </div>
              <div style="background: #0f0d23; padding: 10px; border-radius: 8px; border: 1px solid #231d4e;">
                <span style="font-size: 11px; color: #94a3b8;">Estado</span>
                <div style="font-size: 13px; font-weight: 700; color: #ffffff; margin-top: 4px;">${c.estado_display}</div>
              </div>
            </div>
          </div>
        `;
        document.getElementById('btnViewToEditCarta').onclick = () => {
          window.location.href = `/admin/core/carta/${c.id}/change/`;
        };
        document.getElementById('modalViewCarta').style.display = 'flex';
      });
  }

  function openEditCartaModal(cartaId) {
    fetch(`/admin/core/carta/${cartaId}/detail-json/`)
      .then(res => res.json())
      .then(data => {
        if (!data.success) {
          showToast(data.error || 'Error');
          return;
        }
        const c = data.carta;
        document.getElementById('editCartaId').value = c.id;
        document.getElementById('editCartaNombre').value = c.nombre;
        document.getElementById('editCartaNorma').value = c.norma_iso;
        document.getElementById('editCartaConcepto').value = c.concepto;
        document.getElementById('editCartaDescripcion').value = c.descripcion;
        document.getElementById('editCartaFuerza').value = c.fuerza;
        document.getElementById('editCartaDefensa').value = c.defensa;
        document.getElementById('editCartaEstado').value = c.estado;
        document.getElementById('modalEditCarta').style.display = 'flex';
      });
  }

  function submitNewCarta(e) {
    e.preventDefault();
    const payload = {
      nombre: document.getElementById('newCartaNombre').value,
      norma_iso: document.getElementById('newCartaNorma').value,
      concepto: document.getElementById('newCartaConcepto').value,
      descripcion: document.getElementById('newCartaDescripcion').value,
      fuerza: document.getElementById('newCartaFuerza').value,
      defensa: document.getElementById('newCartaDefensa').value,
      estado: document.getElementById('newCartaEstado').value,
    };

    fetch('/admin/core/carta/create-ajax/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify(payload)
    })
      .then(res => res.json())
      .then(data => {
        if (!data.success) {
          showToast(data.error || 'Error al crear');
          return;
        }
        closeModal('modalNewCarta');
        showToast(data.message || 'Carta creada exitosamente');
        setTimeout(() => window.location.reload(), 1200);
      })
      .catch(err => {
        showToast('Error de conexión');
      });
  }

  function submitEditCarta(e) {
    e.preventDefault();
    const cartaId = document.getElementById('editCartaId').value;
    const payload = {
      nombre: document.getElementById('editCartaNombre').value,
      norma_iso: document.getElementById('editCartaNorma').value,
      concepto: document.getElementById('editCartaConcepto').value,
      descripcion: document.getElementById('editCartaDescripcion').value,
      fuerza: document.getElementById('editCartaFuerza').value,
      defensa: document.getElementById('editCartaDefensa').value,
      estado: document.getElementById('editCartaEstado').value,
    };

    fetch(`/admin/core/carta/${cartaId}/update-ajax/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify(payload)
    })
      .then(res => res.json())
      .then(data => {
        if (!data.success) {
          showToast(data.error || 'Error al guardar');
          return;
        }
        closeModal('modalEditCarta');
        showToast(data.message || 'Carta actualizada');

        // Actualizar tarjeta en el DOM directamente
        const c = data.carta;
        const cardElem = document.querySelector(`.iq-carta-card[data-id="${c.id}"]`);
        if (cardElem) {
          cardElem.setAttribute('data-nombre', c.nombre.toLowerCase());
          cardElem.setAttribute('data-norma', c.norma_iso);
          cardElem.setAttribute('data-concepto', c.concepto.toLowerCase());
          cardElem.setAttribute('data-estado', c.estado);

          cardElem.querySelector('.iq-carta-title').textContent = c.nombre;
          cardElem.querySelector('.iq-carta-desc').textContent = c.descripcion;
          cardElem.querySelector('.iq-carta-iso-badge').textContent = c.norma_iso;
          cardElem.querySelector('.iq-stat-fuerza').innerHTML = `<i class="bi bi-lightning-fill"></i> ${c.fuerza}`;
          cardElem.querySelector('.iq-stat-defensa').innerHTML = `<i class="bi bi-shield-fill"></i> ${c.defensa}`;

          const pill = cardElem.querySelector('.iq-pill-estado-activo, .iq-pill-estado-inactivo');
          if (pill) {
            pill.className = c.estado === 'activo' ? 'iq-pill-estado-activo' : 'iq-pill-estado-inactivo';
            pill.textContent = c.estado_display;
          }
        }
      })
      .catch(err => {
        showToast('Error de conexión');
      });
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  document.addEventListener('DOMContentLoaded', () => {
    applyCardsFilter();
  });
