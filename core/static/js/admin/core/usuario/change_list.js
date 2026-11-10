let currentUserId = null;

function getCsrfToken() {
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
  return cookieValue || document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}

// 1. Abrir panel lateral y minimizar lista al seleccionar o pulsar un usuario
function seleccionarUsuario(userId, rowElement) {
  currentUserId = userId;
  alternarModoEdicion(false);
  alternarModoPassword(false);

  // Minimizar la lista de usuarios abriendo el panel lateral
  const splitView = document.getElementById('usersSplitView');
  splitView.classList.add('panel-open');

  // Resaltar fila seleccionada
  document.querySelectorAll('.iq-utbody-row').forEach(r => r.classList.remove('row-selected'));
  if (rowElement) {
    rowElement.classList.add('row-selected');
  } else {
    const targetRow = document.querySelector(`.iq-utbody-row[data-id="${userId}"]`);
    if (targetRow) targetRow.classList.add('row-selected');
  }

  // Cargar datos dinámicos vía AJAX
  fetch(`/admin/core/usuario/${userId}/detail-json/`)
    .then(res => res.json())
    .then(data => {
      if (!data.success) return;

      // Actualizar Panel Lateral de Perfil
      document.getElementById('profNombre').textContent = data.nombre_completo;
      document.getElementById('profAliasText').textContent = 'Alias: ' + data.alias;
      document.getElementById('profEmailText').textContent = data.correo;
      if (document.getElementById('profAvatarImg')) {
        document.getElementById('profAvatarImg').src = data.avatar_url || '/static/img/avatars/necromancer_1.png';
      }
      document.getElementById('profAreaBadge').textContent = data.area;
      document.getElementById('profRolBadge').textContent = data.rol_display;
      
      const badgeEstado = document.getElementById('profBadgeEstado');
      badgeEstado.textContent = data.estado_display;
      badgeEstado.className = `iq-badge-pill ${data.estado === 'activo' ? 'pill-activo' : 'pill-inactivo'}`;

      // Actualizar Tab Información
      const infoNombreAlias = document.getElementById('infoNombreAlias');
      if (infoNombreAlias) infoNombreAlias.textContent = `${data.nombre_completo} (${data.alias})`;
      const infoCorreo = document.getElementById('infoCorreo');
      if (infoCorreo) infoCorreo.textContent = data.correo;
      const infoAreaRol = document.getElementById('infoAreaRol');
      if (infoAreaRol) infoAreaRol.textContent = `${data.area} • ${data.rol_display}`;
      const pwdTargetUser = document.getElementById('pwdTargetUser');
      if (pwdTargetUser) pwdTargetUser.textContent = `${data.nombre_completo} (@${data.alias})`;

      // Actualizar Progreso
      if (data.progreso) {
        document.getElementById('profNivelText').textContent = 'Nivel ' + data.progreso.nivel;
        document.getElementById('profXpText').textContent = `${data.progreso.xp} / ${data.progreso.xp_max} XP`;
        document.getElementById('profXpBar').style.width = `${data.progreso.xp_pct}%`;
        document.getElementById('profOroVal').textContent = data.progreso.oro.toLocaleString();
        document.getElementById('profGemasVal').textContent = data.progreso.gemas.toLocaleString();
        document.getElementById('profVidasVal').textContent = `${data.progreso.vidas_actuales}/3`;
        document.getElementById('profReinicioVidas').textContent = data.progreso.ultimo_reinicio_vidas;
        document.getElementById('profReinicioProgreso').textContent = data.progreso.ultimo_reinicio_progreso;
      }

      // Actualizar Caja Inferior de Detalle
      document.getElementById('dtId').textContent = data.id;
      document.getElementById('dtName').textContent = data.nombre_completo;
      document.getElementById('dtAlias').textContent = data.alias;
      document.getElementById('dtEmail').textContent = data.correo;
      document.getElementById('dtArea').textContent = data.area;
      document.getElementById('dtRol').textContent = data.rol;
      const dtEstado = document.getElementById('dtEstado');
      dtEstado.textContent = data.estado_display;
      dtEstado.className = `iq-badge-pill ${data.estado === 'activo' ? 'pill-activo' : 'pill-inactivo'}`;
      document.getElementById('dtCreated').textContent = data.created_at;
      document.getElementById('dtUpdated').textContent = data.updated_at;

      // Prellenar campos del formulario de edición
      document.getElementById('editNombre').value = data.nombre_completo;
      document.getElementById('editAlias').value = data.alias;
      document.getElementById('editEmail').value = data.correo;
      document.getElementById('editArea').value = data.area;
      document.getElementById('editRol').value = data.rol;
      setEstadoForm(data.estado);
    })
    .catch(err => console.error("Error al cargar usuario:", err));
}

// 2. Cerrar panel lateral y re-expandir la tabla a ancho completo
function cerrarPanelPerfil() {
  const splitView = document.getElementById('usersSplitView');
  splitView.classList.remove('panel-open');
  document.querySelectorAll('.iq-utbody-row').forEach(r => r.classList.remove('row-selected'));
  alternarModoEdicion(false);
  alternarModoPassword(false);
}

// 3. Activar directamente edición (al oprimir ✏️ en la fila)
function activarEdicionUsuario(userId) {
  seleccionarUsuario(userId);
  setTimeout(() => {
    alternarModoEdicion(true);
  }, 100);
}

// 4. Alternar entre Modo Vista y Modo Edición en el panel lateral
function alternarModoEdicion(activar) {
  const tabContentProgreso = document.getElementById('tabContentProgreso');
  const tabContentInfo = document.getElementById('tabContentInfo');
  const editForm = document.getElementById('editUserForm');
  const pwdForm = document.getElementById('changePasswordForm');

  if (activar) {
    tabContentProgreso.style.display = 'none';
    if (tabContentInfo) tabContentInfo.style.display = 'none';
    if (pwdForm) pwdForm.classList.remove('active');
    editForm.classList.add('active');
  } else {
    editForm.classList.remove('active');
    if (!pwdForm || !pwdForm.classList.contains('active')) {
      const activeTab = document.querySelector('.iq-ptab.active');
      if (activeTab && activeTab.textContent.trim().toLowerCase().includes('información')) {
        if (tabContentInfo) tabContentInfo.style.display = 'flex';
      } else {
        tabContentProgreso.style.display = 'flex';
      }
    }
  }
}

// 5. Alternar Modo Cambio de Contraseña Independiente
function alternarModoPassword(activar) {
  const tabContentProgreso = document.getElementById('tabContentProgreso');
  const tabContentInfo = document.getElementById('tabContentInfo');
  const editForm = document.getElementById('editUserForm');
  const pwdForm = document.getElementById('changePasswordForm');

  if (activar) {
    tabContentProgreso.style.display = 'none';
    if (tabContentInfo) tabContentInfo.style.display = 'none';
    if (editForm) editForm.classList.remove('active');
    pwdForm.classList.add('active');
    document.getElementById('inputNuevaPassword').value = '';
    document.getElementById('inputConfirmarPassword').value = '';
    setTimeout(() => {
      document.getElementById('inputNuevaPassword').focus();
    }, 50);
  } else {
    pwdForm.classList.remove('active');
    const activeTab = document.querySelector('.iq-ptab.active');
    if (activeTab && activeTab.textContent.trim().toLowerCase().includes('información')) {
      if (tabContentInfo) tabContentInfo.style.display = 'flex';
    } else {
      tabContentProgreso.style.display = 'flex';
    }
  }
}

// 6. Ver / Ocultar Contraseña
function togglePasswordVisibility(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  if (input.type === 'password') {
    input.type = 'text';
    if (btn) btn.textContent = '🙈';
  } else {
    input.type = 'password';
    if (btn) btn.textContent = '👁️';
  }
}

// 7. Guardar Nueva Contraseña vía AJAX
function guardarCambioPassword(e) {
  e.preventDefault();
  const nueva = document.getElementById('inputNuevaPassword').value.trim();
  const confirmar = document.getElementById('inputConfirmarPassword').value.trim();
  const btnSave = document.getElementById('btnSavePassword');

  if (nueva.length < 6) {
    alert("La contraseña debe tener al menos 6 caracteres.");
    return;
  }

  if (nueva !== confirmar) {
    alert("Las contraseñas no coinciden. Por favor verifica.");
    return;
  }

  btnSave.disabled = true;
  btnSave.textContent = 'Actualizando...';

  fetch(`/admin/core/usuario/${currentUserId}/change-password-ajax/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken()
    },
    body: JSON.stringify({
      nueva_password: nueva,
      confirmar_password: confirmar
    })
  })
  .then(res => res.json())
  .then(data => {
    btnSave.disabled = false;
    btnSave.textContent = '🔑 Guardar Contraseña';
    if (data.success) {
      alert(`[OK] ${data.message}`);
      alternarModoPassword(false);
    } else {
      alert("Error: " + (data.error || "No se pudo actualizar la contraseña."));
    }
  })
  .catch(err => {
    btnSave.disabled = false;
    btnSave.textContent = '🔑 Guardar Contraseña';
    alert("Error de red al actualizar contraseña.");
  });
}

// 8. Selector de estado Activo/Inactivo
function setEstadoForm(estado) {
  document.getElementById('editEstado').value = estado;
  const optActivo = document.getElementById('optActivo');
  const optInactivo = document.getElementById('optInactivo');

  if (estado === 'activo') {
    optActivo.className = 'iq-status-opt selected-active';
    optInactivo.className = 'iq-status-opt';
  } else {
    optActivo.className = 'iq-status-opt';
    optInactivo.className = 'iq-status-opt selected-inactive';
  }
}

// 9. Guardar Cambios de Usuario vía AJAX
function guardarEdicionUsuario(e) {
  e.preventDefault();
  const btnSave = document.getElementById('btnSaveUserEdit');
  btnSave.textContent = 'Guardando...';
  btnSave.disabled = true;

  const payload = {
    nombre_completo: document.getElementById('editNombre').value,
    alias: document.getElementById('editAlias').value,
    correo: document.getElementById('editEmail').value,
    area: document.getElementById('editArea').value,
    rol: document.getElementById('editRol').value,
    estado: document.getElementById('editEstado').value,
  };

  fetch(`/admin/core/usuario/${currentUserId}/update-ajax/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken()
    },
    body: JSON.stringify(payload)
  })
  .then(res => res.json())
  .then(res => {
    btnSave.textContent = '💾 Guardar Cambios';
    btnSave.disabled = false;

    if (res.success) {
      // Actualizar la fila en la tabla
      const row = document.querySelector(`.iq-utbody-row[data-id="${currentUserId}"]`);
      if (row) {
        row.querySelector('.iq-tbl-name').textContent = res.usuario.nombre_completo;
        row.children[2].querySelector('.iq-cell-ellipsis').textContent = res.usuario.alias;
        row.children[3].querySelector('.iq-cell-ellipsis').textContent = res.usuario.correo;
        row.children[4].querySelector('.iq-cell-ellipsis').textContent = res.usuario.area;
        row.children[5].querySelector('.iq-cell-ellipsis').textContent = res.usuario.rol;
        
        const badge = document.getElementById(`badge-status-${currentUserId}`);
        if (badge) {
          badge.textContent = res.usuario.estado_display;
          badge.className = `iq-badge-pill ${res.usuario.estado === 'activo' ? 'pill-activo' : 'pill-inactivo'}`;
        }
      }

      // Recargar perfil y regresar al modo vista
      seleccionarUsuario(currentUserId);
      alternarModoEdicion(false);
      alert(`[OK] ${res.message}`);
    } else {
      alert("Error: " + (res.error || "No se pudo actualizar"));
    }
  })
  .catch(err => {
    btnSave.textContent = '💾 Guardar Cambios';
    btnSave.disabled = false;
    alert("Error de red al actualizar usuario.");
  });
}

// 10. Reiniciar Progreso del Usuario Actual
function reiniciarProgresoUsuarioActual() {
  if (!confirm("¿Confirmas que deseas reiniciar a 0 el nivel, XP, oro y gemas de este colaborador? Se generará asiento en la auditoría forense.")) {
    return;
  }

  fetch(`/admin/core/usuario/${currentUserId}/reset-progress-ajax/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCsrfToken()
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      document.getElementById('profNivelText').textContent = 'Nivel 1';
      document.getElementById('profXpText').textContent = '0 / 100 XP';
      document.getElementById('profXpBar').style.width = '0%';
      document.getElementById('profOroVal').textContent = '0';
      document.getElementById('profGemasVal').textContent = '0';
      document.getElementById('profVidasVal').textContent = '3/3';
      document.getElementById('profReinicioProgreso').textContent = data.progreso.ultimo_reinicio_progreso;
      alert(`[OK] ${data.message}`);
    } else {
      alert("Error: " + (data.error || "No se pudo reiniciar"));
    }
  });
}

// 11. Buscador y Filtros Client-side
document.addEventListener("DOMContentLoaded", function() {
  const searchInput = document.getElementById('userSearchInput');
  const roleSelect = document.getElementById('roleFilterSelect');
  const statusSelect = document.getElementById('statusFilterSelect');

  function aplicarFiltros() {
    const q = searchInput.value.toLowerCase().trim();
    const role = roleSelect.value;
    const status = statusSelect.value;

    document.querySelectorAll('.iq-utbody-row').forEach(row => {
      const name = (row.dataset.name || '').toLowerCase();
      const alias = (row.dataset.alias || '').toLowerCase();
      const email = (row.dataset.email || '').toLowerCase();
      const r = row.dataset.rol;
      const s = row.dataset.status;

      const matchesText = !q || name.includes(q) || alias.includes(q) || email.includes(q);
      const matchesRole = !role || r === role;
      const matchesStatus = !status || s === status;

      row.style.display = (matchesText && matchesRole && matchesStatus) ? '' : 'none';
    });
  }

  if (searchInput) searchInput.addEventListener('input', aplicarFiltros);
  if (roleSelect) roleSelect.addEventListener('change', aplicarFiltros);
  if (statusSelect) statusSelect.addEventListener('change', aplicarFiltros);
  const btnTrigger = document.getElementById('btnFilterTrigger');
  if (btnTrigger) btnTrigger.addEventListener('click', aplicarFiltros);

  // Auto-seleccionar primer usuario en carga para desplegar el panel lateral idéntico a la maqueta
  const firstRow = document.querySelector('.iq-utbody-row');
  if (firstRow) {
    const firstId = firstRow.dataset.id;
    if (firstId) {
      seleccionarUsuario(firstId, firstRow);
    }
  }
});

// 12. Pestañas del perfil
function cambiarTabPerfil(tabName) {
  document.querySelectorAll('.iq-ptab').forEach(t => t.classList.remove('active'));
  if (event && event.target) {
    event.target.classList.add('active');
  }

  alternarModoEdicion(false);
  alternarModoPassword(false);

  const tabProgreso = document.getElementById('tabContentProgreso');
  const tabInfo = document.getElementById('tabContentInfo');

  if (tabName === 'info') {
    tabProgreso.style.display = 'none';
    if (tabInfo) tabInfo.style.display = 'flex';
  } else {
    if (tabInfo) tabInfo.style.display = 'none';
    tabProgreso.style.display = 'flex';
  }
}
