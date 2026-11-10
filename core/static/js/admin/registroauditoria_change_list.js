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
