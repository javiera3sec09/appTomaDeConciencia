// Registros serializados de la página actual para selección reactiva inmediata
  const REGISTROS = JSON.parse(document.getElementById('registroauditoria-data')?.textContent || '[]');

  function selectAuditRecord(recordId) {
    // Actualizar estilo de fila activa
    document.querySelectorAll('.iq-audit-row').forEach(row => {
      row.classList.remove('active');
      if (parseInt(row.getAttribute('data-id')) === recordId) {
        row.classList.add('active');
      }
    });

    const reg = REGISTROS.find(r => r.id === recordId);
    if (!reg) return;

    // Actualizar campos del panel de detalles
    document.getElementById('detFechaHora').textContent = reg.created_at_full;
    document.getElementById('detUsuario').textContent = reg.admin_alias;
    document.getElementById('detModulo').textContent = reg.modulo_display;
    document.getElementById('detRegistroId').textContent = reg.registro_codigo;
    document.getElementById('detDireccionIp').textContent = reg.direccion_ip;

    // Badge de Acción
    let badgeHtml = '';
    const acc = reg.accion;
    if (acc === 'EDITAR') {
      badgeHtml = `<span class="iq-action-badge editar"><i class="bi bi-pencil-fill"></i> EDITAR</span>`;
    } else if (acc === 'ELIMINAR') {
      badgeHtml = `<span class="iq-action-badge eliminar"><i class="bi bi-trash3-fill"></i> ELIMINAR</span>`;
    } else if (acc === 'CAMBIAR_CONFIG') {
      badgeHtml = `<span class="iq-action-badge cambiar_config"><i class="bi bi-gear-fill"></i> CAMBIAR_CONFIG</span>`;
    } else if (acc === 'REINICIAR_PROGRESO') {
      badgeHtml = `<span class="iq-action-badge reiniciar_progreso"><i class="bi bi-arrow-repeat"></i> REINICIAR_PROGRESO</span>`;
    } else {
      badgeHtml = `<span class="iq-action-badge crear"><i class="bi bi-plus-circle-fill"></i> ${reg.accion_display}</span>`;
    }
    document.getElementById('detAccion').innerHTML = badgeHtml;

    // Snapshots JSON formateados
    const antBox = document.getElementById('detDatosAnteriores');
    const nueBox = document.getElementById('detDatosNuevos');

    try {
      antBox.textContent = JSON.stringify(reg.datos_anteriores, null, 2);
    } catch(e) {
      antBox.textContent = String(reg.datos_anteriores || '{}');
    }

    try {
      nueBox.textContent = JSON.stringify(reg.datos_nuevos, null, 2);
    } catch(e) {
      nueBox.textContent = String(reg.datos_nuevos || '{}');
    }
  }

  // Formatear JSON inicial si existe
  window.addEventListener('DOMContentLoaded', () => {
    if (REGISTROS.length > 0) {
      selectAuditRecord(REGISTROS[0].id);
    }
  });


// =============================================================
// GESTIÓN DE MODAL Y DEPURACIÓN DE REGISTROS DE AUDITORÍA
// =============================================================
function getCsrfToken() {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  if (match) return match[1];
  return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}

function abrirModalDepurarAuditoria() {
  const modal = document.getElementById('modalDepurarAuditoria');
  if (!modal) return;
  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';

  const check = document.getElementById('checkConfirmarPurge');
  if (check) check.checked = false;
  verificarConfirmacionPurge(false);

  actualizarPreviewPurge();
}

function cerrarModalDepurarAuditoria(e) {
  if (e.target && e.target.id === 'modalDepurarAuditoria') {
    cerrarModalDepurarAuditoriaDirecto();
  }
}

function cerrarModalDepurarAuditoriaDirecto() {
  const modal = document.getElementById('modalDepurarAuditoria');
  if (modal) modal.style.display = 'none';
  document.body.style.overflow = '';
}

function actualizarPreviewPurge() {
  const tiempo = document.getElementById('purgeTiempoSelect')?.value || '1';
  const adminId = document.getElementById('purgeAdminSelect')?.value || 'todos';
  const accion = document.getElementById('purgeAccionSelect')?.value || 'todas';
  const countEl = document.getElementById('purgeCountPreview');

  if (countEl) {
    countEl.textContent = 'Calculando registros...';
    countEl.style.color = '#94a3b8';
  }

  fetch('/admin/core/registroauditoria/purge-ajax/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken()
    },
    body: JSON.stringify({
      tiempo: tiempo,
      admin_id: adminId,
      accion: accion,
      preview: true
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success && countEl) {
      const c = data.count;
      countEl.textContent = `${c} registro${c === 1 ? '' : 's'} encontrado${c === 1 ? '' : 's'}`;
      countEl.style.color = c > 0 ? '#38bdf8' : '#a855f7';
    } else if (countEl) {
      countEl.textContent = 'No se pudo calcular';
    }
  })
  .catch(err => {
    console.error(err);
    if (countEl) countEl.textContent = 'Error al consultar registros';
  });
}

function verificarConfirmacionPurge(isChecked) {
  const btn = document.getElementById('btnEjecutarPurge');
  if (btn) {
    btn.disabled = !isChecked;
  }
}

function ejecutarPurgeAuditoria() {
  const btn = document.getElementById('btnEjecutarPurge');
  const tiempo = document.getElementById('purgeTiempoSelect')?.value || '1';
  const adminId = document.getElementById('purgeAdminSelect')?.value || 'todos';
  const accion = document.getElementById('purgeAccionSelect')?.value || 'todas';
  const check = document.getElementById('checkConfirmarPurge');

  if (!btn || btn.disabled) return;

  btn.disabled = true;
  btn.innerHTML = '<i class="bi bi-arrow-repeat" style="animation: spin 1s linear infinite; display: inline-block;"></i><span>Eliminando registros...</span>';
  if (check) check.disabled = true;

  fetch('/admin/core/registroauditoria/purge-ajax/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken()
    },
    body: JSON.stringify({
      tiempo: tiempo,
      admin_id: adminId,
      accion: accion,
      preview: false
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      btn.innerHTML = `<i class="bi bi-check2-circle"></i><span>¡${data.deleted_count} eliminados! Recargando...</span>`;
      btn.style.background = '#10b981';
      setTimeout(() => {
        window.location.reload();
      }, 900);
    } else {
      alert(data.error || 'Ocurrió un error al eliminar los registros de auditoría.');
      btn.disabled = false;
      btn.innerHTML = '<i class="bi bi-trash3-fill"></i><span>Eliminar Registros</span>';
      if (check) check.disabled = false;
    }
  })
  .catch(err => {
    console.error(err);
    alert('Error de conexión al depurar los registros de auditoría.');
    btn.disabled = false;
    btn.innerHTML = '<i class="bi bi-trash3-fill"></i><span>Eliminar Registros</span>';
    if (check) check.disabled = false;
  });
}
