document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('mundoSearchInput');
  const domainSelect = document.getElementById('mundoDomainSelect');
  const difficultySelect = document.getElementById('mundoDifficultySelect');
  const statusSelect = document.getElementById('mundoStatusSelect');
  const btnFilter = document.getElementById('btnMundosFilter');
  const tableRows = document.querySelectorAll('#mundosTableBody .mundo-row');
  const showingCount = document.getElementById('mundosShowingCount');
  const toast = document.getElementById('iqMundosToast');

  function showToast(msg, isError = false) {
    toast.textContent = msg;
    toast.style.background = isError ? '#ef4444' : '#10b981';
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 3200);
  }

  // Filtrado reactivo en tiempo real
  function applyFilters() {
    const query = (searchInput.value || '').trim().toLowerCase();
    const domainVal = (domainSelect.value || '').trim().toLowerCase();
    const diffVal = difficultySelect.value;
    const statusVal = statusSelect.value;

    let visibleCount = 0;

    tableRows.forEach(row => {
      const codigo = row.getAttribute('data-codigo') || '';
      const nombre = row.getAttribute('data-nombre') || '';
      const dominio = row.getAttribute('data-dominio') || '';
      const dificultad = row.getAttribute('data-dificultad') || '';
      const estado = row.getAttribute('data-estado') || '';

      const matchesSearch = !query || codigo.includes(query) || nombre.includes(query) || dominio.includes(query);
      const matchesDomain = !domainVal || dominio === domainVal;
      const matchesDiff = !diffVal || dificultad === diffVal;
      const matchesStatus = !statusVal || estado === statusVal;

      if (matchesSearch && matchesDomain && matchesDiff && matchesStatus) {
        row.style.display = '';
        visibleCount++;
      } else {
        row.style.display = 'none';
      }
    });

    if (showingCount) {
      showingCount.textContent = `Mostrando 1 - ${visibleCount} de ${visibleCount} mundos`;
    }
  }

  searchInput.addEventListener('input', applyFilters);
  domainSelect.addEventListener('change', applyFilters);
  difficultySelect.addEventListener('change', applyFilters);
  statusSelect.addEventListener('change', applyFilters);
  btnFilter.addEventListener('click', applyFilters);

  // -----------------------------------------------------------------
  // MODAL VER MUNDO
  // -----------------------------------------------------------------
  const viewModal = document.getElementById('viewMundoModal');
  const closeViewBtns = [document.getElementById('btnCloseViewMundo'), document.getElementById('btnCloseViewMundoBtn')];
  let currentViewingMundoId = null;

  closeViewBtns.forEach(btn => {
    if (btn) btn.addEventListener('click', () => viewModal.classList.remove('open'));
  });

  document.querySelectorAll('.btn-view-mundo').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      const mundoId = this.getAttribute('data-id');
      currentViewingMundoId = mundoId;

      fetch(`/admin/core/mundo/${mundoId}/detail-json/`)
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            const m = data.mundo;
            document.getElementById('viewMundoImg').src = m.imagen_url;
            document.getElementById('viewMundoCodigo').textContent = m.codigo_iso;
            document.getElementById('viewMundoNombre').textContent = m.nombre_tematico;
            document.getElementById('viewMundoOrden').textContent = m.orden;
            document.getElementById('viewMundoDominio').textContent = m.dominio;
            document.getElementById('viewMundoNiveles').textContent = `${m.total_niveles} niveles configurados`;

            const difEl = document.getElementById('viewMundoDificultad');
            difEl.innerHTML = `<span class="iq-dif-pill dif-${m.dificultad}">${m.dificultad_display}</span>`;

            const stEl = document.getElementById('viewMundoEstado');
            stEl.innerHTML = `<span class="iq-status-pill status-${m.estado}">${m.estado_display}</span>`;

            viewModal.classList.add('open');
          } else {
            showToast(data.error || 'Error al cargar mundo', true);
          }
        })
        .catch(() => showToast('Error de comunicación', true));
    });
  });

  // -----------------------------------------------------------------
  // MODAL EDITAR MUNDO
  // -----------------------------------------------------------------
  const editModal = document.getElementById('editMundoModal');
  const closeEditBtns = [document.getElementById('btnCloseEditMundo'), document.getElementById('btnCancelEditMundo')];
  const editForm = document.getElementById('editMundoForm');

  closeEditBtns.forEach(btn => {
    if (btn) btn.addEventListener('click', () => editModal.classList.remove('open'));
  });

  function openEditModal(mundoId) {
    document.getElementById('editMundoId').value = mundoId;

    fetch(`/admin/core/mundo/${mundoId}/detail-json/`)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          const m = data.mundo;
          document.getElementById('editInputOrden').value = m.orden;
          document.getElementById('editInputCodigo').value = m.codigo_iso;
          document.getElementById('editInputNombre').value = m.nombre_tematico;
          document.getElementById('editInputDominio').value = m.dominio;
          document.getElementById('editSelectDificultad').value = m.dificultad;
          document.getElementById('editSelectEstado').value = m.estado;

          editModal.classList.add('open');
        } else {
          showToast(data.error || 'Error al cargar datos', true);
        }
      })
      .catch(() => showToast('Error de conexión', true));
  }

  document.querySelectorAll('.btn-edit-mundo').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      openEditModal(this.getAttribute('data-id'));
    });
  });

  const btnEditFromView = document.getElementById('btnEditFromView');
  if (btnEditFromView) {
    btnEditFromView.addEventListener('click', () => {
      viewModal.classList.remove('open');
      if (currentViewingMundoId) openEditModal(currentViewingMundoId);
    });
  }

  // Guardar Cambios de Edición
  editForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const mundoId = document.getElementById('editMundoId').value;
    const payload = {
      orden: document.getElementById('editInputOrden').value,
      codigo_iso: document.getElementById('editInputCodigo').value,
      nombre_tematico: document.getElementById('editInputNombre').value,
      dominio: document.getElementById('editInputDominio').value,
      dificultad: document.getElementById('editSelectDificultad').value,
      estado: document.getElementById('editSelectEstado').value
    };

    fetch(`/admin/core/mundo/${mundoId}/update-ajax/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      },
      body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        showToast(data.message || 'Mundo actualizado');
        editModal.classList.remove('open');

        // Refrescar fila en la tabla
        const row = document.querySelector(`.mundo-row[data-id="${mundoId}"]`);
        if (row) {
          row.setAttribute('data-orden', payload.orden);
          row.setAttribute('data-codigo', payload.codigo_iso.toLowerCase());
          row.setAttribute('data-nombre', payload.nombre_tematico.toLowerCase());
          row.setAttribute('data-dominio', payload.dominio.toLowerCase());
          row.setAttribute('data-dificultad', payload.dificultad);
          row.setAttribute('data-estado', payload.estado);

          row.children[1].textContent = payload.orden;
          row.children[2].textContent = payload.codigo_iso;
          row.children[3].textContent = payload.nombre_tematico;
          row.children[4].textContent = payload.dominio;

          const diffMap = { facil: 'Fácil', normal: 'Normal', dificil: 'Difícil' };
          row.children[5].innerHTML = `<span class="iq-dif-pill dif-${payload.dificultad}">${diffMap[payload.dificultad]}</span>`;

          const stMap = { activo: 'Activo', inactivo: 'Inactivo' };
          row.children[6].innerHTML = `<span class="iq-status-pill status-${payload.estado}">${stMap[payload.estado]}</span>`;
        }
      } else {
        showToast(data.error || 'Error al actualizar', true);
      }
    })
    .catch(() => showToast('Error en la comunicación con el servidor', true));
  });

  // -----------------------------------------------------------------
  // MODAL CREAR MUNDO
  // -----------------------------------------------------------------
  const createModal = document.getElementById('createMundoModal');
  const btnOpenCreate = document.getElementById('btnOpenNewMundoModal');
  const closeCreateBtns = [document.getElementById('btnCloseCreateMundo'), document.getElementById('btnCancelCreateMundo')];
  const createForm = document.getElementById('createMundoForm');

  if (btnOpenCreate) {
    btnOpenCreate.addEventListener('click', () => createModal.classList.add('open'));
  }

  closeCreateBtns.forEach(btn => {
    if (btn) btn.addEventListener('click', () => createModal.classList.remove('open'));
  });

  createForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const payload = {
      orden: document.getElementById('createInputOrden').value,
      codigo_iso: document.getElementById('createInputCodigo').value,
      nombre_tematico: document.getElementById('createInputNombre').value,
      dominio: document.getElementById('createInputDominio').value,
      dificultad: document.getElementById('createSelectDificultad').value,
      estado: document.getElementById('createSelectEstado').value
    };

    fetch('/admin/core/mundo/create-ajax/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      },
      body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        showToast(data.message || 'Mundo creado exitosamente');
        createModal.classList.remove('open');
        setTimeout(() => window.location.reload(), 600);
      } else {
        showToast(data.error || 'Error al crear mundo', true);
      }
    })
    .catch(() => showToast('Error al conectar con el servidor', true));
  });

  // Cerrar modales al hacer clic fuera
  [viewModal, editModal, createModal].forEach(modal => {
    modal.addEventListener('click', function(e) {
      if (e.target === this) this.classList.remove('open');
    });
  });
});
