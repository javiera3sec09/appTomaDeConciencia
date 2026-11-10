document.addEventListener('DOMContentLoaded', function() {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const table = document.getElementById('parametrosTable');
  const tbody = document.getElementById('parametrosTbody');
  const allRows = Array.from(tbody.querySelectorAll('tr[data-id]'));
  
  const catFilterBtns = document.querySelectorAll('.iq-pg-cat-btn');
  const showingCountText = document.getElementById('showingCountText');
  const paginationContainer = document.getElementById('tablePagination');
  
  // Editor form elements
  const detailForm = document.getElementById('parametroDetailForm');
  const editParamId = document.getElementById('editParamId');
  const editCategoria = document.getElementById('editCategoria');
  const editClave = document.getElementById('editClave');
  const editValor = document.getElementById('editValor');
  const editDescripcion = document.getElementById('editDescripcion');
  const detailFormCard = document.getElementById('detailFormCard');

  // Modal elements
  const modalBackdrop = document.getElementById('paramViewModal');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  const modalEditBtn = document.getElementById('modalEditBtn');
  const modalCategoria = document.getElementById('modalCategoria');
  const modalClave = document.getElementById('modalClave');
  const modalValor = document.getElementById('modalValor');
  const modalDescripcion = document.getElementById('modalDescripcion');
  const modalUpdated = document.getElementById('modalUpdated');
  let currentModalParamId = null;

  // Toast
  const toast = document.getElementById('pgToast');
  const toastMsg = document.getElementById('toastMsg');
  function showToast(msg) {
    toastMsg.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 3500);
  }

  // State
  let currentCategory = 'ALL';
  let currentPage = 1;
  const pageSize = 5;

  // 1. Filtrado y Paginación
  function getFilteredRows() {
    if (currentCategory === 'ALL') {
      return allRows;
    }
    return allRows.filter(row => {
      const cat = row.getAttribute('data-categoria') || '';
      if (currentCategory === 'Jerarquía') {
        return cat.toLowerCase().includes('jerarqu');
      }
      if (currentCategory === 'Economía') {
        return cat.toLowerCase().includes('econom');
      }
      if (currentCategory === 'Otros') {
        const standard = ['vidas', 'jerarquia', 'jerarquía', 'economia', 'economía', 'seguridad', 'logros'];
        return !standard.includes(cat.toLowerCase());
      }
      return cat.toLowerCase() === currentCategory.toLowerCase();
    });
  }

  function renderTable() {
    const filtered = getFilteredRows();
    const totalItems = filtered.length;
    const totalPages = Math.ceil(totalItems / pageSize) || 1;

    if (currentPage > totalPages) {
      currentPage = totalPages;
    }

    const startIndex = (currentPage - 1) * pageSize;
    const endIndex = Math.min(startIndex + pageSize, totalItems);

    // Ocultar todas las filas
    allRows.forEach(row => row.style.display = 'none');

    // Mostrar sólo las de la página actual
    for (let i = startIndex; i < endIndex; i++) {
      if (filtered[i]) {
        filtered[i].style.display = '';
      }
    }

    // Texto de conteo
    if (totalItems === 0) {
      showingCountText.textContent = 'Mostrando 0 de 0 parámetros';
    } else {
      showingCountText.textContent = `Mostrando ${startIndex + 1} - ${endIndex} de ${totalItems} parámetros`;
    }

    // Renderizar botones de paginación
    renderPagination(totalPages);
  }

  function renderPagination(totalPages) {
    paginationContainer.innerHTML = '';
    if (totalPages <= 1) return;

    // Botón Anterior
    const prevBtn = document.createElement('button');
    prevBtn.type = 'button';
    prevBtn.className = 'iq-pg-page-btn';
    prevBtn.innerHTML = '&lt;';
    prevBtn.disabled = (currentPage === 1);
    prevBtn.addEventListener('click', () => {
      if (currentPage > 1) {
        currentPage--;
        renderTable();
      }
    });
    paginationContainer.appendChild(prevBtn);

    // Páginas
    for (let p = 1; p <= totalPages; p++) {
      const pageBtn = document.createElement('button');
      pageBtn.type = 'button';
      pageBtn.className = `iq-pg-page-btn ${p === currentPage ? 'active' : ''}`;
      pageBtn.textContent = p;
      pageBtn.addEventListener('click', () => {
        currentPage = p;
        renderTable();
      });
      paginationContainer.appendChild(pageBtn);
    }

    // Botón Siguiente
    const nextBtn = document.createElement('button');
    nextBtn.type = 'button';
    nextBtn.className = 'iq-pg-page-btn';
    nextBtn.innerHTML = '&gt;';
    nextBtn.disabled = (currentPage === totalPages);
    nextBtn.addEventListener('click', () => {
      if (currentPage < totalPages) {
        currentPage++;
        renderTable();
      }
    });
    paginationContainer.appendChild(nextBtn);
  }

  // 2. Eventos de Categoría
  catFilterBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      catFilterBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      currentCategory = this.getAttribute('data-cat');
      currentPage = 1;
      renderTable();
    });
  });

  // 3. Cargar en Editor
  function loadIntoEditor(row) {
    if (!row) return;
    const id = row.getAttribute('data-id');
    const cat = row.getAttribute('data-categoria');
    const clave = row.getAttribute('data-clave');
    const valor = row.getAttribute('data-valor');
    const desc = row.getAttribute('data-descripcion');

    editParamId.value = id;
    editClave.value = clave;
    editValor.value = valor;
    editDescripcion.value = desc;

    // Normalizar selección de categoría
    let matched = false;
    for (let i = 0; i < editCategoria.options.length; i++) {
      const optVal = editCategoria.options[i].value.toLowerCase();
      if (optVal.includes(cat.toLowerCase()) || cat.toLowerCase().includes(optVal)) {
        editCategoria.selectedIndex = i;
        matched = true;
        break;
      }
    }
    if (!matched) {
      editCategoria.value = 'Otros';
    }

    // Resaltar fila seleccionada
    allRows.forEach(r => r.classList.remove('selected-row'));
    row.classList.add('selected-row');

    // Scroll suave si está fuera de pantalla
    detailFormCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  // Delegación de clicks en la tabla
  tbody.addEventListener('click', function(e) {
    const editBtn = e.target.closest('.btn-edit-param');
    const viewBtn = e.target.closest('.btn-view-param');

    if (editBtn) {
      const row = editBtn.closest('tr');
      loadIntoEditor(row);
      return;
    }

    if (viewBtn) {
      const row = viewBtn.closest('tr');
      openViewModal(row);
      return;
    }
  });

  // 4. Modal Ver Detalles
  function openViewModal(row) {
    if (!row) return;
    currentModalParamId = row.getAttribute('data-id');
    modalCategoria.textContent = row.getAttribute('data-categoria');
    modalClave.textContent = row.getAttribute('data-clave');
    modalValor.textContent = row.getAttribute('data-valor');
    modalDescripcion.textContent = row.getAttribute('data-descripcion') || 'Sin descripción';
    modalUpdated.textContent = row.getAttribute('data-updated') || 'Reciente';

    modalBackdrop.style.display = 'flex';
  }

  modalCloseBtn.addEventListener('click', () => {
    modalBackdrop.style.display = 'none';
  });

  modalBackdrop.addEventListener('click', (e) => {
    if (e.target === modalBackdrop) {
      modalBackdrop.style.display = 'none';
    }
  });

  modalEditBtn.addEventListener('click', () => {
    modalBackdrop.style.display = 'none';
    if (currentModalParamId) {
      const row = tbody.querySelector(`tr[data-id="${currentModalParamId}"]`);
      if (row) loadIntoEditor(row);
    }
  });

  // 5. Enviar Formulario de Edición (AJAX)
  detailForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const id = editParamId.value;
    if (!id) {
      alert('Por favor selecciona un parámetro de la lista para editar.');
      return;
    }

    const formData = new FormData();
    formData.append('categoria', editCategoria.value);
    formData.append('clave', editClave.value);
    formData.append('valor', editValor.value);
    formData.append('descripcion', editDescripcion.value);

    const saveBtn = document.getElementById('btnGuardarCambios');
    const origText = saveBtn.innerHTML;
    saveBtn.disabled = true;
    saveBtn.innerHTML = 'Guardando...';

    fetch(`/admin/core/parametroglobal/${id}/update-ajax/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
      },
      body: formData,
    })
    .then(res => res.json())
    .then(data => {
      saveBtn.disabled = false;
      saveBtn.innerHTML = origText;

      if (data.success) {
        showToast(data.message || 'Parámetro actualizado exitosamente.');

        // Actualizar datos de la fila en tiempo real
        const row = tbody.querySelector(`tr[data-id="${id}"]`);
        if (row && data.parametro) {
          row.setAttribute('data-categoria', data.parametro.categoria);
          row.setAttribute('data-clave', data.parametro.clave);
          row.setAttribute('data-valor', data.parametro.valor);
          row.setAttribute('data-descripcion', data.parametro.descripcion);
          row.setAttribute('data-updated', data.parametro.updated_at);

          // Actualizar celdas visibles
          const cells = row.querySelectorAll('td');
          if (cells.length >= 5) {
            // Clave
            cells[1].querySelector('.iq-pg-key-code').textContent = data.parametro.clave;
            // Valor
            cells[2].querySelector('.iq-pg-val-pill').textContent = data.parametro.valor;
            // Descripción
            cells[3].querySelector('.iq-pg-desc-text').textContent = data.parametro.descripcion || '-';
            // Fecha
            cells[4].querySelector('.iq-pg-date-text').textContent = data.parametro.updated_at;
          }
        }
      } else {
        alert('Error al guardar: ' + (data.error || 'Ocurrió un problema inesperado.'));
      }
    })
    .catch(err => {
      saveBtn.disabled = false;
      saveBtn.innerHTML = origText;
      console.error(err);
      alert('Error de conexión al guardar el parámetro.');
    });
  });

  // 6. Botón Restablecer a Valores por Defecto
  const btnResetDefault = document.getElementById('btnResetDefault');
  btnResetDefault.addEventListener('click', function() {
    if (!confirm('¿Estás seguro de que deseas restablecer todos los parámetros globales a sus valores por defecto? Esta acción será auditada.')) {
      return;
    }

    const origBtnHtml = btnResetDefault.innerHTML;
    btnResetDefault.disabled = true;
    btnResetDefault.innerHTML = 'Restableciendo...';

    fetch('/admin/core/parametroglobal/reset-default-ajax/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
      }
    })
    .then(res => res.json())
    .then(data => {
      btnResetDefault.disabled = false;
      btnResetDefault.innerHTML = origBtnHtml;
      if (data.success) {
        showToast(data.message || 'Parámetros restablecidos por defecto.');
        setTimeout(() => {
          window.location.reload();
        }, 800);
      } else {
        alert('Error: ' + (data.error || 'No se pudieron restablecer los valores.'));
      }
    })
    .catch(err => {
      btnResetDefault.disabled = false;
      btnResetDefault.innerHTML = origBtnHtml;
      console.error(err);
      alert('Error de conexión al restablecer parámetros.');
    });
  });

  // 7. Inicialización: Cargar la primera fila en el editor por defecto
  if (allRows.length > 0) {
    loadIntoEditor(allRows[0]);
  }
  renderTable();
});
