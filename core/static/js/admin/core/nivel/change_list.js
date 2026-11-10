const _initNivel = JSON.parse(document.getElementById('nivel-data')?.textContent || '{}');
  const mundosData = _initNivel.mundosData || [];
  let currentMundoId = _initNivel.currentMundoId || 0;
  let currentPage = 1;
  const pageSize = 5;

  function showToast(msg) {
    const toast = document.getElementById('iqToast');
    document.getElementById('toastMessage').textContent = msg;
    toast.classList.add('show');
    setTimeout(() => { toast.classList.remove('show'); }, 3500);
  }

  function closeModal(id) {
    document.getElementById(id).style.display = 'none';
  }

  function openNewNivelModal() {
    const nextNum = getNextNivelNumber();
    document.getElementById('newNivelNumero').value = nextNum;
    document.getElementById('newNivelMundoId').value = currentMundoId;
    document.getElementById('newNivelTitulo').value = '';
    document.getElementById('modalNewNivel').style.display = 'flex';
  }

  function getNextNivelNumber() {
    const rows = document.querySelectorAll('#nivelesTableBody tr[data-numero]');
    let maxNum = 0;
    rows.forEach(r => {
      const n = parseInt(r.getAttribute('data-numero'), 10);
      if (!isNaN(n) && n > maxNum) maxNum = n;
    });
    return maxNum + 1;
  }

  // Conmutador interactivo de tabs de mundo
  function selectWorldTab(mundoId) {
    if (currentMundoId === mundoId) return;
    currentMundoId = mundoId;

    // Actualizar tabs visuales
    document.querySelectorAll('.iq-world-tab').forEach(tab => {
      if (parseInt(tab.getAttribute('data-mundo-id'), 10) === mundoId) {
        tab.classList.add('active');
      } else {
        tab.classList.remove('active');
      }
    });

    // Petición AJAX para obtener niveles y métricas del mundo seleccionado
    fetch(`/admin/core/nivel/mundo/${mundoId}/json/`)
      .then(res => res.json())
      .then(data => {
        if (!data.success) {
          showToast(data.error || 'Error al cargar mundo');
          return;
        }

        // 1. Actualizar Hero Banner
        const m = data.mundo;
        document.getElementById('heroAvatarImg').src = m.avatar_url;
        document.getElementById('heroTitle').textContent = `Mundo ${m.orden}: ${m.codigo_iso}`;
        document.getElementById('heroSubtitle').textContent = m.nombre_tematico;
        document.getElementById('heroDesc').textContent = m.descripcion;

        document.getElementById('statNiveles').textContent = m.total_niveles;
        document.getElementById('statXp').textContent = m.total_xp.toLocaleString();
        document.getElementById('statOro').textContent = m.total_oro.toLocaleString();
        document.getElementById('statGemas').textContent = m.total_gemas.toLocaleString();

        // 2. Renderizar tabla con los nuevos niveles
        renderTableRows(data.niveles);
        applyTableFilters();
      })
      .catch(err => {
        console.error('Error fetching niveles:', err);
      });
  }

  function renderTableRows(niveles) {
    const tbody = document.getElementById('nivelesTableBody');
    if (!niveles || niveles.length === 0) {
      tbody.innerHTML = `
        <tr id="emptyRow">
          <td colspan="7" style="text-align: center; padding: 40px; color: var(--text-muted);">
            No hay niveles registrados para este mundo. ¡Haz clic en "+ Nuevo Nivel" para comenzar!
          </td>
        </tr>
      `;
      return;
    }

    let html = '';
    niveles.forEach(n => {
      const tipoPill = n.tipo === 'jefe'
        ? '<span class="iq-pill-tipo-jefe">👑 Jefe</span>'
        : '<span class="iq-pill-tipo-normal">Normal</span>';

      let difPill = '<span class="iq-pill-dif-normal">Normal</span>';
      if (n.dificultad === 'facil') difPill = '<span class="iq-pill-dif-facil">Fácil</span>';
      else if (n.dificultad === 'dificil') difPill = '<span class="iq-pill-dif-dificil">Difícil</span>';

      const estPill = n.estado === 'activo'
        ? '<span class="iq-pill-estado-activo">Activo</span>'
        : '<span class="iq-pill-estado-inactivo">Inactivo</span>';

      html += `
        <tr data-id="${n.id}"
            data-numero="${n.numero_nivel}"
            data-titulo="${n.titulo.toLowerCase()}"
            data-tipo="${n.tipo}"
            data-dificultad="${n.dificultad}"
            data-estado="${n.estado}">
          <td style="font-weight: 700; color: #94a3b8;">${n.numero_nivel}</td>
          <td style="font-weight: 600; color: #ffffff;">${escapeHtml(n.titulo)}</td>
          <td>${tipoPill}</td>
          <td>${difPill}</td>
          <td>
            <div class="iq-rewards-box">
              <span class="iq-reward-item iq-reward-coin"><i class="bi bi-coin"></i> ${n.recompensa_oro}</span>
              <span class="iq-reward-item iq-reward-gem"><i class="bi bi-gem"></i> ${n.recompensa_gemas}</span>
              <span class="iq-reward-item iq-reward-xp"><i class="bi bi-star-fill"></i> ${n.recompensa_xp}</span>
            </div>
          </td>
          <td>${estPill}</td>
          <td style="text-align: center;">
            <div class="iq-actions-cell" style="justify-content: center;">
              <button type="button" class="btn-action-view" title="Ver Nivel" onclick="openViewNivelModal(${n.id})">
                <i class="bi bi-eye"></i>
              </button>
              <button type="button" class="btn-action-edit" title="Editar Nivel" onclick="openEditNivelModal(${n.id})">
                <i class="bi bi-pencil"></i>
              </button>
            </div>
          </td>
        </tr>
      `;
    });
    tbody.innerHTML = html;
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  // Filtrado y paginación en tiempo real
  function applyTableFilters() {
    const q = (document.getElementById('searchNivelInput').value || '').trim().toLowerCase();
    const tipo = document.getElementById('filterTipo').value;
    const dif = document.getElementById('filterDificultad').value;
    const est = document.getElementById('filterEstado').value;

    const rows = Array.from(document.querySelectorAll('#nivelesTableBody tr[data-id]'));
    let matched = [];

    rows.forEach(r => {
      const matchQ = !q || r.getAttribute('data-titulo').includes(q);
      const matchTipo = !tipo || r.getAttribute('data-tipo') === tipo;
      const matchDif = !dif || r.getAttribute('data-dificultad') === dif;
      const matchEst = !est || r.getAttribute('data-estado') === est;

      if (matchQ && matchTipo && matchDif && matchEst) {
        matched.push(r);
      } else {
        r.style.display = 'none';
      }
    });

    const total = matched.length;
    const totalPages = Math.ceil(total / pageSize) || 1;
    if (currentPage > totalPages) currentPage = 1;

    const startIdx = (currentPage - 1) * pageSize;
    const endIdx = startIdx + pageSize;

    matched.forEach((r, idx) => {
      if (idx >= startIdx && idx < endIdx) {
        r.style.display = '';
      } else {
        r.style.display = 'none';
      }
    });

    // Actualizar resumen
    document.getElementById('pagStart').textContent = total > 0 ? (startIdx + 1) : 0;
    document.getElementById('pagEnd').textContent = Math.min(endIdx, total);
    document.getElementById('pagTotal').textContent = total;

    // Renderizar botones de paginación
    const pageButtonsContainer = document.getElementById('pageButtons');
    let btns = '';
    for (let p = 1; p <= totalPages; p++) {
      btns += `<button type="button" class="iq-page-btn ${p === currentPage ? 'active' : ''}" onclick="goToPage(${p})">${p}</button>`;
    }
    pageButtonsContainer.innerHTML = btns;
  }

  function goToPage(p) {
    currentPage = p;
    applyTableFilters();
  }

  function prevPage() {
    if (currentPage > 1) {
      currentPage--;
      applyTableFilters();
    }
  }

  function nextPage() {
    const total = document.querySelectorAll('#nivelesTableBody tr[data-id]').length;
    const totalPages = Math.ceil(total / pageSize);
    if (currentPage < totalPages) {
      currentPage++;
      applyTableFilters();
    }
  }

  // Modales Ver y Editar
  function openViewNivelModal(nivelId) {
    fetch(`/admin/core/nivel/${nivelId}/detail-json/`)
      .then(res => res.json())
      .then(data => {
        if (!data.success) {
          showToast(data.error || 'Error');
          return;
        }
        const n = data.nivel;
        let fasesHtml = '';
        if (n.fases && n.fases.length > 0) {
          fasesHtml = `<div style="margin-top: 14px;"><h4 style="font-size: 13px; color: #cbd5e1; margin-bottom: 8px;">Fases de Caso (${n.fases.length}):</h4><ul style="padding-left: 20px; font-size: 12px; color: #94a3b8; margin: 0;">`;
          n.fases.forEach(f => {
            fasesHtml += `<li>Fase ${f.numero_fase}: <strong>${escapeHtml(f.titulo_incidente)}</strong> [${f.amenaza}]</li>`;
          });
          fasesHtml += `</ul></div>`;
        }

        document.getElementById('viewNivelBody').innerHTML = `
          <div style="display: flex; flex-direction: column; gap: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #231d4e; padding-bottom: 12px;">
              <div>
                <span style="font-size: 11px; text-transform: uppercase; color: #7dd3fc; font-weight: 700;">${n.mundo_codigo}</span>
                <h2 style="font-size: 18px; color: #ffffff; margin: 2px 0;">Nivel ${n.numero_nivel}: ${escapeHtml(n.titulo)}</h2>
              </div>
              <span class="${n.tipo === 'jefe' ? 'iq-pill-tipo-jefe' : 'iq-pill-tipo-normal'}">${n.tipo_display}</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 6px;">
              <div style="background: #0f0d23; padding: 10px; border-radius: 8px; border: 1px solid #231d4e;">
                <span style="font-size: 11px; color: #94a3b8;">Dificultad</span>
                <div style="font-size: 13px; font-weight: 700; color: #ffffff; margin-top: 2px;">${n.dificultad_display}</div>
              </div>
              <div style="background: #0f0d23; padding: 10px; border-radius: 8px; border: 1px solid #231d4e;">
                <span style="font-size: 11px; color: #94a3b8;">Estado</span>
                <div style="font-size: 13px; font-weight: 700; color: #ffffff; margin-top: 2px;">${n.estado_display}</div>
              </div>
              <div style="background: #0f0d23; padding: 10px; border-radius: 8px; border: 1px solid #231d4e;">
                <span style="font-size: 11px; color: #94a3b8;">Recompensas</span>
                <div style="font-size: 12px; font-weight: 700; color: #ffffff; margin-top: 2px;">🪙 ${n.recompensa_oro} | 💎 ${n.recompensa_gemas} | ⭐ ${n.recompensa_xp}</div>
              </div>
            </div>
            ${fasesHtml}
          </div>
        `;
        document.getElementById('btnViewToEdit').onclick = () => {
          closeModal('modalViewNivel');
          openEditNivelModal(n.id);
        };
        document.getElementById('modalViewNivel').style.display = 'flex';
      });
  }

  function openEditNivelModal(nivelId) {
    fetch(`/admin/core/nivel/${nivelId}/detail-json/`)
      .then(res => res.json())
      .then(data => {
        if (!data.success) {
          showToast(data.error || 'Error');
          return;
        }
        const n = data.nivel;
        document.getElementById('editNivelId').value = n.id;
        document.getElementById('editNivelNumero').value = n.numero_nivel;
        document.getElementById('editNivelTitulo').value = n.titulo;
        document.getElementById('editNivelTipo').value = n.tipo;
        document.getElementById('editNivelDificultad').value = n.dificultad;
        document.getElementById('editNivelEstado').value = n.estado;
        document.getElementById('editNivelOro').value = n.recompensa_oro;
        document.getElementById('editNivelGemas').value = n.recompensa_gemas;
        document.getElementById('editNivelXp').value = n.recompensa_xp;
        document.getElementById('modalEditNivel').style.display = 'flex';
      });
  }

  function submitNewNivel(e) {
    e.preventDefault();
    const payload = {
      mundo_id: document.getElementById('newNivelMundoId').value,
      numero_nivel: document.getElementById('newNivelNumero').value,
      titulo: document.getElementById('newNivelTitulo').value,
      tipo: document.getElementById('newNivelTipo').value,
      dificultad: document.getElementById('newNivelDificultad').value,
      estado: document.getElementById('newNivelEstado').value,
      recompensa_oro: document.getElementById('newNivelOro').value,
      recompensa_gemas: document.getElementById('newNivelGemas').value,
      recompensa_xp: document.getElementById('newNivelXp').value,
    };

    fetch('/admin/core/nivel/create-ajax/', {
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
          showToast(data.error || 'Error al crear nivel');
          return;
        }
        closeModal('modalNewNivel');
        showToast(data.message || 'Nivel creado');
        // Recargar niveles del mundo
        selectWorldTab(parseInt(payload.mundo_id, 10));
      })
      .catch(err => {
        showToast('Error de conexión');
      });
  }

  function submitEditNivel(e) {
    e.preventDefault();
    const nivelId = document.getElementById('editNivelId').value;
    const payload = {
      numero_nivel: document.getElementById('editNivelNumero').value,
      titulo: document.getElementById('editNivelTitulo').value,
      tipo: document.getElementById('editNivelTipo').value,
      dificultad: document.getElementById('editNivelDificultad').value,
      estado: document.getElementById('editNivelEstado').value,
      recompensa_oro: document.getElementById('editNivelOro').value,
      recompensa_gemas: document.getElementById('editNivelGemas').value,
      recompensa_xp: document.getElementById('editNivelXp').value,
    };

    fetch(`/admin/core/nivel/${nivelId}/update-ajax/`, {
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
        closeModal('modalEditNivel');
        showToast(data.message || 'Nivel actualizado');
        // Recargar vista del mundo
        selectWorldTab(currentMundoId);
      })
      .catch(err => {
        showToast('Error de conexión');
      });
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

  // Inicializar paginación al cargar
  document.addEventListener('DOMContentLoaded', () => {
    applyTableFilters();
  });
