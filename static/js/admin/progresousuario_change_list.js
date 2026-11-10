document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('progSearchInput');
  const roleSelect = document.getElementById('progRoleSelect');
  const statusSelect = document.getElementById('progStatusSelect');
  const levelSelect = document.getElementById('progLevelSelect');
  const btnFilter = document.getElementById('btnProgFilter');
  const tableRows = document.querySelectorAll('#progTableBody .prog-row');
  const showingCount = document.getElementById('progShowingCount');
  const toast = document.getElementById('iqToast');

  // Función de Notificación Toast
  function showToast(msg, isError = false) {
    toast.textContent = msg;
    toast.style.background = isError ? '#ef4444' : '#10b981';
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 3200);
  }

  // Filtrado instantáneo en vivo
  function applyFilters() {
    const query = (searchInput.value || '').trim().toLowerCase();
    const roleVal = roleSelect.value;
    const statusVal = statusSelect.value;
    const levelVal = levelSelect.value;

    let visibleCount = 0;

    tableRows.forEach(row => {
      const name = row.getAttribute('data-name') || '';
      const alias = row.getAttribute('data-alias') || '';
      const email = row.getAttribute('data-email') || '';
      const role = row.getAttribute('data-role') || '';
      const status = row.getAttribute('data-status') || '';
      const level = parseInt(row.getAttribute('data-level') || '1', 10);

      // Coincidencia de texto
      const matchesSearch = !query || name.includes(query) || alias.includes(query) || email.includes(query);

      // Coincidencia de rol
      const matchesRole = !roleVal || role === roleVal;

      // Coincidencia de estado
      const matchesStatus = !statusVal || status === statusVal;

      // Coincidencia de rango de nivel
      let matchesLevel = true;
      if (levelVal === '1-5') matchesLevel = (level >= 1 && level <= 5);
      else if (levelVal === '6-10') matchesLevel = (level >= 6 && level <= 10);
      else if (levelVal === '11-15') matchesLevel = (level >= 11 && level <= 15);
      else if (levelVal === '16+') matchesLevel = (level >= 16);

      if (matchesSearch && matchesRole && matchesStatus && matchesLevel) {
        row.style.display = '';
        visibleCount++;
      } else {
        row.style.display = 'none';
      }
    });

    if (showingCount) {
      showingCount.textContent = `Mostrando 1 - ${Math.min(visibleCount, 10)} de ${visibleCount} jugadores`;
    }
  }

  searchInput.addEventListener('input', applyFilters);
  roleSelect.addEventListener('change', applyFilters);
  statusSelect.addEventListener('change', applyFilters);
  levelSelect.addEventListener('change', applyFilters);
  btnFilter.addEventListener('click', applyFilters);

  // Botón Actualizar con animación de giro
  const btnRefresh = document.getElementById('btnPageRefresh');
  if (btnRefresh) {
    btnRefresh.addEventListener('click', function() {
      btnRefresh.classList.add('spinning');
      setTimeout(() => {
        window.location.reload();
      }, 400);
    });
  }

  // -----------------------------------------------------------------
  // MODAL VER DETALLES
  // -----------------------------------------------------------------
  const viewModal = document.getElementById('viewModalBackdrop');
  const closeViewBtns = [document.getElementById('btnCloseViewModal'), document.getElementById('btnCloseViewModalBtn')];
  let currentViewingProgId = null;

  closeViewBtns.forEach(btn => {
    if (btn) btn.addEventListener('click', () => viewModal.classList.remove('open'));
  });

  document.querySelectorAll('.btn-view-prog').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      const progId = this.getAttribute('data-id');
      currentViewingProgId = progId;

      fetch(`/admin/core/progresousuario/${progId}/detail-json/`)
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            const p = data.progreso;
            const u = p.usuario;

            document.getElementById('viewPlayerName').textContent = u.nombre_completo;
            document.getElementById('viewPlayerAlias').textContent = '@' + u.alias;
            document.getElementById('viewPlayerEmail').textContent = u.correo + ' • ' + (u.area || 'General');
            if (document.getElementById('viewPlayerAvatarImg')) {
              document.getElementById('viewPlayerAvatarImg').src = u.avatar_url || '/static/img/avatars/necromancer_1.png';
            }
            document.getElementById('viewPlayerLevel').textContent = p.nivel;
            document.getElementById('viewPlayerXP').textContent = Number(p.xp).toLocaleString();
            document.getElementById('viewPlayerLives').textContent = `♥ ${p.vidas_actuales}`;
            document.getElementById('viewPlayerGold').textContent = Number(p.oro).toLocaleString();
            document.getElementById('viewPlayerGems').textContent = Number(p.gemas).toLocaleString();
            document.getElementById('viewPlayerLivesReset').textContent = p.ultimo_reinicio_vidas;
            document.getElementById('viewPlayerProgReset').textContent = p.ultimo_reinicio_progreso;

            const st = document.getElementById('viewPlayerStatus');
            st.textContent = u.estado_display;
            st.className = `iq-status-pill ${u.estado === 'activo' ? 'status-activo' : 'status-inactivo'}`;

            viewModal.classList.add('open');
          } else {
            showToast(data.error || 'Error al cargar detalles', true);
          }
        })
        .catch(() => showToast('Error de conexión', true));
    });
  });

  // -----------------------------------------------------------------
  // MODAL EDITAR PROGRESO
  // -----------------------------------------------------------------
  const editModal = document.getElementById('editModalBackdrop');
  const closeEditBtns = [document.getElementById('btnCloseEditModal'), document.getElementById('btnCancelEdit')];
  const editForm = document.getElementById('editProgForm');
  const editProgId = document.getElementById('editProgId');
  const editPlayerName = document.getElementById('editPlayerName');
  const editInputLevel = document.getElementById('editInputLevel');
  const editInputXP = document.getElementById('editInputXP');
  const editInputGold = document.getElementById('editInputGold');
  const editInputGems = document.getElementById('editInputGems');
  const editInputLives = document.getElementById('editInputLives');
  const btnResetProg = document.getElementById('btnResetIndividualProg');

  closeEditBtns.forEach(btn => {
    if (btn) btn.addEventListener('click', () => editModal.classList.remove('open'));
  });

  function openEditModal(progId) {
    editProgId.value = progId;

    fetch(`/admin/core/progresousuario/${progId}/detail-json/`)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          const p = data.progreso;
          const u = p.usuario;

          editPlayerName.textContent = `${u.nombre_completo} (@${u.alias})`;
          if (document.getElementById('editPlayerAvatarImg')) {
            document.getElementById('editPlayerAvatarImg').src = u.avatar_url || '/static/img/avatars/necromancer_1.png';
          }
          editInputLevel.value = p.nivel;
          editInputXP.value = p.xp;
          editInputGold.value = p.oro;
          editInputGems.value = p.gemas;
          editInputLives.value = p.vidas_actuales;

          editModal.classList.add('open');
        } else {
          showToast(data.error || 'Error al abrir edición', true);
        }
      })
      .catch(() => showToast('Error de conexión', true));
  }

  document.querySelectorAll('.btn-edit-prog').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      const progId = this.getAttribute('data-id');
      openEditModal(progId);
    });
  });

  const btnEditFromView = document.getElementById('btnEditFromView');
  if (btnEditFromView) {
    btnEditFromView.addEventListener('click', () => {
      viewModal.classList.remove('open');
      if (currentViewingProgId) openEditModal(currentViewingProgId);
    });
  }

  // Guardar Edición con AJAX
  editForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const progId = editProgId.value;

    const payload = {
      nivel: editInputLevel.value,
      xp: editInputXP.value,
      oro: editInputGold.value,
      gemas: editInputGems.value,
      vidas_actuales: editInputLives.value
    };

    fetch(`/admin/core/progresousuario/${progId}/update-ajax/`, {
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
        showToast(data.message || 'Progreso actualizado exitosamente');
        editModal.classList.remove('open');

        // Actualizar fila en la tabla
        const row = document.querySelector(`.prog-row[data-id="${progId}"]`);
        if (row) {
          row.setAttribute('data-level', payload.nivel);
          row.setAttribute('data-xp', payload.xp);
          row.setAttribute('data-oro', payload.oro);
          row.setAttribute('data-gemas', payload.gemas);
          row.setAttribute('data-vidas', payload.vidas_actuales);

          row.querySelector('.col-val-nivel').textContent = payload.nivel;
          row.querySelector('.col-val-xp').textContent = Number(payload.xp).toLocaleString();
          row.querySelector('.col-val-oro').textContent = Number(payload.oro).toLocaleString();
          row.querySelector('.col-val-gemas').textContent = Number(payload.gemas).toLocaleString();
          row.querySelector('.col-val-vidas span').textContent = payload.vidas_actuales;
        }
      } else {
        showToast(data.error || 'Error al actualizar', true);
      }
    })
    .catch(() => showToast('Error en la comunicación con el servidor', true));
  });

  // Reiniciar Progreso Individual
  if (btnResetProg) {
    btnResetProg.addEventListener('click', function() {
      if (!confirm('¿Estás seguro de reiniciar el progreso de este jugador a Nivel 1 y 0 XP? Esta acción quedará auditada.')) {
        return;
      }

      const progId = editProgId.value;
      fetch(`/admin/core/progresousuario/${progId}/reset-ajax/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          showToast(data.message || 'Progreso reiniciado');
          editModal.classList.remove('open');

          const row = document.querySelector(`.prog-row[data-id="${progId}"]`);
          if (row) {
            row.setAttribute('data-level', 1);
            row.setAttribute('data-xp', 0);
            row.setAttribute('data-oro', 0);
            row.setAttribute('data-gemas', 0);
            row.setAttribute('data-vidas', 3);

            row.querySelector('.col-val-nivel').textContent = '1';
            row.querySelector('.col-val-xp').textContent = '0';
            row.querySelector('.col-val-oro').textContent = '0';
            row.querySelector('.col-val-gemas').textContent = '0';
            row.querySelector('.col-val-vidas span').textContent = '3';
          }
        } else {
          showToast(data.error || 'Error al reiniciar', true);
        }
      })
      .catch(() => showToast('Error al conectar con el servidor', true));
    });
  }

  // Cerrar modales al hacer clic fuera
  [viewModal, editModal].forEach(modal => {
    modal.addEventListener('click', function(e) {
      if (e.target === this) this.classList.remove('open');
    });
  });
});
