// Filtrar selector de Niveles según el Mundo seleccionado
  const nivelesData = JSON.parse(document.getElementById('partidajugada-data')?.textContent || '[]');

  function onFilterMundoChange(mundoId) {
    const nivelSelect = document.getElementById('filterNivel');
    if (!nivelSelect) return;
    
    nivelSelect.innerHTML = '<option value="">Todos los niveles</option>';
    
    const filtrados = mundoId 
      ? nivelesData.filter(n => String(n.mundo_id) === String(mundoId))
      : nivelesData;
      
    filtrados.forEach(n => {
      const opt = document.createElement('option');
      opt.value = n.id;
      opt.textContent = `Nivel ${n.numero_nivel} - ${n.titulo}`;
      nivelSelect.appendChild(opt);
    });
  }

  // Modal para detalle de partida
  function abrirDetallePartida(partidaId) {
    const modal = document.getElementById('partidaModal');
    const content = document.getElementById('modalPartidaContent');
    modal.style.display = 'flex';

    fetch(`/admin/core/partidajugada/${partidaId}/detail-json/`)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          const p = data.partida;
          const badgeClass = p.resultado === 'victoria' ? 'victoria' : (p.resultado === 'derrota' ? 'derrota' : 'abandonada');
          content.innerHTML = `
            <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 8px;">
              <img src="${p.avatar_url}" style="width: 48px; height: 48px; border-radius: 50%; border: 2px solid #8b5cf6;" />
              <div>
                <div style="font-size: 15px; font-weight: 800; color: #ffffff;">${p.nombre_completo}</div>
                <div style="font-size: 12px; color: #a855f7;">@${p.usuario} • ${p.area}</div>
              </div>
            </div>

            <div class="iq-detail-row">
              <span class="iq-detail-label">Fecha y Hora</span>
              <span class="iq-detail-val">${p.fecha_partida}</span>
            </div>
            <div class="iq-detail-row">
              <span class="iq-detail-label">Mundo ISO</span>
              <span class="iq-detail-val">${p.mundo} (${p.mundo_nombre})</span>
            </div>
            <div class="iq-detail-row">
              <span class="iq-detail-label">Nivel</span>
              <span class="iq-detail-val">Nivel ${p.numero_nivel} - ${p.nivel}</span>
            </div>
            <div class="iq-detail-row">
              <span class="iq-detail-label">Resultado</span>
              <span class="iq-result-pill ${badgeClass}">${p.resultado_display}</span>
            </div>
            <div class="iq-detail-row">
              <span class="iq-detail-label">Recompensa Obtenida</span>
              <span class="iq-detail-val">
                <span style="color: #f59e0b; margin-right: 12px;"><i class="bi bi-coin"></i> +${p.oro_obtenido} Oro</span>
                <span style="color: #38bdf8;"><i class="bi bi-gem"></i> +${p.gemas_obtenidas} Gemas</span>
              </span>
            </div>
          `;
        } else {
          content.innerHTML = `<div style="color: #ef4444; padding: 10px;">${data.error || 'Error al cargar telemetría.'}</div>`;
        }
      })
      .catch(err => {
        content.innerHTML = `<div style="color: #ef4444; padding: 10px;">Error de conexión con el servidor.</div>`;
      });
  }

  function cerrarDetallePartida(e) {
    if (e.target.id === 'partidaModal') {
      document.getElementById('partidaModal').style.display = 'none';
    }
  }

  function cerrarModalDirecto() {
    document.getElementById('partidaModal').style.display = 'none';
  }


// =============================================================
// REINICIO DE ANALÍTICAS Y TELEMETRÍA (MODO LANZAMIENTO)
// =============================================================
function getCsrfToken() {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  if (match) return match[1];
  return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}

function abrirModalReinicioLanzamiento() {
  const modal = document.getElementById('modalReinicioLanzamiento');
  const input = document.getElementById('inputConfirmarReinicio');
  const btn = document.getElementById('btnEjecutarReinicio');
  if (!modal) return;
  if (input) {
    input.value = '';
    input.disabled = false;
  }
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = '<i class="bi bi-rocket-takeoff-fill"></i><span>Sí, Reiniciar Todo a Cero</span>';
    btn.style.background = '';
  }
  modal.style.display = 'flex';
  if (input) setTimeout(() => input.focus(), 150);
}

function cerrarModalReinicio(e) {
  if (e.target.id === 'modalReinicioLanzamiento') {
    cerrarModalReinicioDirecto();
  }
}

function cerrarModalReinicioDirecto() {
  const modal = document.getElementById('modalReinicioLanzamiento');
  if (modal) modal.style.display = 'none';
}

function verificarTextoConfirmacion(val) {
  const btn = document.getElementById('btnEjecutarReinicio');
  if (!btn) return;
  btn.disabled = (val || '').trim().toUpperCase() !== 'REINICIAR';
}

function ejecutarReinicioLanzamiento() {
  const btn = document.getElementById('btnEjecutarReinicio');
  const input = document.getElementById('inputConfirmarReinicio');
  if (!btn || btn.disabled) return;

  btn.disabled = true;
  btn.innerHTML = '<i class="bi bi-arrow-repeat" style="animation: spin 1s linear infinite; display: inline-block;"></i><span>Reiniciando base de datos...</span>';
  if (input) input.disabled = true;

  fetch('/admin/core/partidajugada/reset-analytics-ajax/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken()
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      btn.innerHTML = '<i class="bi bi-check2-circle"></i><span>¡Completado! Recargando...</span>';
      btn.style.background = '#10b981';
      setTimeout(() => {
        window.location.reload();
      }, 900);
    } else {
      alert(data.error || 'Ocurrió un error al intentar reiniciar la telemetría.');
      btn.disabled = false;
      btn.innerHTML = '<i class="bi bi-rocket-takeoff-fill"></i><span>Sí, Reiniciar Todo a Cero</span>';
      if (input) input.disabled = false;
    }
  })
  .catch(err => {
    console.error(err);
    alert('Error de conexión al reiniciar la telemetría.');
    btn.disabled = false;
    btn.innerHTML = '<i class="bi bi-rocket-takeoff-fill"></i><span>Sí, Reiniciar Todo a Cero</span>';
    if (input) input.disabled = false;
  });
}
