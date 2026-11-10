(function() {
  const _initData = JSON.parse(document.getElementById('fasecarta-data')?.textContent || '{}');
  const JERARQUIA = _initData.jerarquia || {};
  const CARTAS_ACTIVAS = _initData.cartasActivas || [];

  let currentMundoId = _initData.currentMundoId;
  let currentNivelId = _initData.currentNivelId;
  let currentFaseId = _initData.currentFaseId;
  let currentFaseData = null;

  let currentDeck = _initData.currentDeck || [];
  let originalDeck = JSON.parse(JSON.stringify(currentDeck));

  // Elementos DOM
  const selectMundo = document.getElementById('selectMundo');
  const selectNivel = document.getElementById('selectNivel');
  const selectFase = document.getElementById('selectFase');
  const subtextMundo = document.getElementById('subtextMundo');
  const subtextNivel = document.getElementById('subtextNivel');
  const subtextFase = document.getElementById('subtextFase');

  const headerFaseNum = document.getElementById('headerFaseNum');
  const cartasCountBadge = document.getElementById('cartasCountBadge');
  const cartasContainer = document.getElementById('cartasContainer');
  const addMoreSlot = document.getElementById('addMoreSlot');
  const addMoreSubtext = document.getElementById('addMoreSubtext');
  const btnOpenAddModal = document.getElementById('btnOpenAddModal');

  const btnCancelChanges = document.getElementById('btnCancelChanges');
  const btnSaveDeck = document.getElementById('btnSaveDeck');

  const previewFaseNumBadge = document.getElementById('previewFaseNumBadge');
  const previewFaseTitle = document.getElementById('previewFaseTitle');
  const previewCountText = document.getElementById('previewCountText');
  const previewCardsList = document.getElementById('previewCardsList');
  const previewArtImg = document.getElementById('previewArtImg');

  const validationStatusBadge = document.getElementById('validationStatusBadge');
  const validationStatusText = document.getElementById('validationStatusText');

  // Modal
  const addCardModal = document.getElementById('addCardModal');
  const btnCloseModal = document.getElementById('btnCloseModal');
  const inputSearchModal = document.getElementById('inputSearchModal');
  const isoPillsContainer = document.getElementById('isoPillsContainer');
  const modalCatalogBody = document.getElementById('modalCatalogBody');

  // Toast
  const iqToast = document.getElementById('iqToast');
  const toastMessage = document.getElementById('toastMessage');

  function showToast(msg, isError = false) {
    toastMessage.textContent = msg;
    iqToast.classList.remove('error');
    if (isError) {
      iqToast.classList.add('error');
    }
    iqToast.classList.add('show');
    setTimeout(() => {
      iqToast.classList.remove('show');
    }, 3500);
  }

  // -------------------------------------------------------------
  // INICIALIZACIÓN DE FILTROS EN CASCADA
  // -------------------------------------------------------------
  function populateNiveles(mundoId, selectFirst = true) {
    const mundo = JERARQUIA.find(m => m.id === parseInt(mundoId));
    selectNivel.innerHTML = '';
    if (!mundo || !mundo.niveles || mundo.niveles.length === 0) {
      const opt = document.createElement('option');
      opt.value = '';
      opt.textContent = 'Sin niveles disponibles';
      selectNivel.appendChild(opt);
      subtextNivel.textContent = 'Sin niveles';
      populateFases(null);
      return;
    }

    mundo.niveles.forEach(n => {
      const opt = document.createElement('option');
      opt.value = n.id;
      opt.textContent = `${n.numero_nivel} - ${n.titulo}`;
      selectNivel.appendChild(opt);
    });

    if (selectFirst || !currentNivelId) {
      currentNivelId = mundo.niveles[0].id;
    }
    selectNivel.value = currentNivelId;
    const selNivelObj = mundo.niveles.find(n => n.id === parseInt(currentNivelId)) || mundo.niveles[0];
    subtextNivel.textContent = selNivelObj ? selNivelObj.titulo : '';

    populateFases(currentNivelId, selectFirst);
  }

  function populateFases(nivelId, selectFirst = true) {
    selectFase.innerHTML = '';
    if (!nivelId) {
      const opt = document.createElement('option');
      opt.value = '';
      opt.textContent = 'Sin fases';
      selectFase.appendChild(opt);
      subtextFase.textContent = 'Sin fase seleccionada';
      loadDeckForFase(null);
      return;
    }

    const mundo = JERARQUIA.find(m => m.id === parseInt(selectMundo.value));
    const nivel = mundo ? mundo.niveles.find(n => n.id === parseInt(nivelId)) : null;

    if (!nivel || !nivel.fases || nivel.fases.length === 0) {
      const opt = document.createElement('option');
      opt.value = '';
      opt.textContent = 'Sin fases creadas en este nivel';
      selectFase.appendChild(opt);
      subtextFase.textContent = 'Crea una fase en Fases de Caso';
      loadDeckForFase(null);
      return;
    }

    nivel.fases.forEach(f => {
      const opt = document.createElement('option');
      opt.value = f.id;
      opt.textContent = `${f.numero_fase} - ${f.titulo_incidente}`;
      selectFase.appendChild(opt);
    });

    if (selectFirst || !currentFaseId) {
      currentFaseId = nivel.fases[0].id;
    }
    selectFase.value = currentFaseId;
    const selFaseObj = nivel.fases.find(f => f.id === parseInt(currentFaseId)) || nivel.fases[0];
    subtextFase.textContent = selFaseObj ? selFaseObj.titulo_incidente : '';

    loadDeckForFase(currentFaseId);
  }

  // Cargar datos de la fase y baraja vía AJAX
  function loadDeckForFase(faseId) {
    if (!faseId) {
      currentDeck = [];
      originalDeck = [];
      headerFaseNum.textContent = '-';
      previewFaseNumBadge.textContent = '-';
      previewFaseTitle.textContent = 'Ninguna fase seleccionada';
      renderDeck();
      return;
    }

    fetch(`/admin/core/fasecartaopcion/fase/${faseId}/json/`)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          currentFaseData = data.fase;
          headerFaseNum.textContent = data.fase.numero_fase;
          previewFaseNumBadge.textContent = data.fase.numero_fase;
          previewFaseTitle.textContent = data.fase.titulo_incidente;
          subtextFase.textContent = data.fase.titulo_incidente;

          currentDeck = data.cartas_asignadas.map(c => ({
            carta_id: c.carta_id,
            nombre: c.nombre,
            norma_iso: c.norma_iso,
            concepto: c.concepto,
            descripcion: c.descripcion,
            imagen_url: c.imagen_url,
            fuerza: c.fuerza,
            defensa: c.defensa,
            es_solucion_correcta: Boolean(c.es_solucion_correcta)
          }));
          originalDeck = JSON.parse(JSON.stringify(currentDeck));
          renderDeck();
        } else {
          showToast(data.error || 'Error al cargar la fase', true);
        }
      })
      .catch(err => {
        console.error('Error cargando baraja:', err);
      });
  }

  // -------------------------------------------------------------
  // RENDERIZADO REACTIVO DE CARTAS Y VISTA PREVIA
  // -------------------------------------------------------------
  function renderDeck() {
    const total = currentDeck.length;
    cartasCountBadge.textContent = `${total}/5`;
    previewCountText.textContent = `${total}/5`;

    // Renderizar slots dashed
    if (total >= 5) {
      addMoreSlot.classList.add('disabled');
      addMoreSubtext.textContent = 'Has alcanzado el límite máximo de 5 cartas por fase';
      btnOpenAddModal.disabled = true;
    } else {
      addMoreSlot.classList.remove('disabled');
      const faltan = 5 - total;
      addMoreSubtext.textContent = `Puedes añadir hasta ${faltan} carta${faltan > 1 ? 's' : ''} más (máximo 5)`;
      btnOpenAddModal.disabled = false;
    }

    // Renderizar lista principal
    cartasContainer.innerHTML = '';
    if (total === 0) {
      cartasContainer.innerHTML = `
        <div style="text-align: center; padding: 30px; color: #8b95b5; font-size: 13.5px;">
          <i class="bi bi-inbox" style="font-size: 32px; display: block; margin-bottom: 8px; color: #616b8d;"></i>
          No hay cartas asignadas a esta fase.<br>
          Haz clic en <strong>"+ Agregar Carta"</strong> para seleccionar del catálogo de cartas activas.
        </div>
      `;
    } else {
      currentDeck.forEach((item, index) => {
        const row = document.createElement('div');
        row.className = 'iq-deck-item';
        row.innerHTML = `
          <div class="iq-deck-item-handle">
            <i class="bi bi-grip-vertical"></i>
            <span>${index + 1}</span>
          </div>
          <img src="${item.imagen_url}" alt="${item.nombre}" class="iq-deck-thumb" onerror="this.src='/static/img/cartas/carta_ciberseguridad.png'">
          <div class="iq-deck-item-body">
            <div class="iq-deck-card-name">${escapeHtml(item.nombre)}</div>
            <div class="iq-deck-card-meta">
              <span>${escapeHtml(item.norma_iso)}</span> &bull; <span>${escapeHtml(item.concepto)}</span>
              <span style="display: inline-flex; align-items: center; gap: 4px; margin-left: 8px; font-size: 11px; color: #06b6d4; font-weight: 700;">
                <i class="bi bi-lightning-charge-fill"></i> ${item.fuerza || 85}
              </span>
              <span style="display: inline-flex; align-items: center; gap: 4px; margin-left: 6px; font-size: 11px; color: #c084fc; font-weight: 700;">
                <i class="bi bi-shield-fill"></i> ${item.defensa || 85}
              </span>
            </div>
            <div class="iq-deck-card-desc">${escapeHtml(item.descripcion)}</div>
          </div>
          <div class="iq-switch-group">
            <span class="iq-switch-label">Es solución correcta</span>
            <div class="iq-switch-container" data-idx="${index}">
              <div class="iq-switch-track ${item.es_solucion_correcta ? 'active' : ''}">
                <div class="iq-switch-thumb"></div>
              </div>
              <span class="iq-switch-state">${item.es_solucion_correcta ? 'Sí' : 'No'}</span>
            </div>
          </div>
          <button type="button" class="btn-remove-deck-card" data-idx="${index}" title="Quitar carta de esta fase">
            <i class="bi bi-trash3-fill"></i>
          </button>
        `;
        cartasContainer.appendChild(row);
      });
    }

    // Renderizar Vista Previa Lateral
    previewCardsList.innerHTML = '';
    if (total === 0) {
      previewCardsList.innerHTML = `<span style="font-size: 12px; color: #616b8d; text-align: center; padding: 8px 0;">Sin cartas asignadas</span>`;
    } else {
      currentDeck.forEach(item => {
        const pItem = document.createElement('div');
        pItem.className = 'iq-preview-item';
        pItem.innerHTML = `
          <div class="iq-preview-item-left">
            <img src="${item.imagen_url}" alt="${item.nombre}" class="iq-preview-item-thumb" onerror="this.src='/static/img/cartas/carta_ciberseguridad.png'">
            <span class="iq-preview-item-name">${escapeHtml(item.nombre)}</span>
          </div>
          ${item.es_solucion_correcta ?
            `<span class="iq-preview-badge-correct"><i class="bi bi-check-lg"></i> Correcta</span>` :
            `<span class="iq-preview-badge-incorrect"><i class="bi bi-x-lg"></i> Incorrecta</span>`
          }
        `;
        previewCardsList.appendChild(pItem);
      });
    }

    // Validaciones de Negocio
    validateDeck();
  }

  function validateDeck() {
    const total = currentDeck.length;
    const correctas = currentDeck.filter(c => c.es_solucion_correcta).length;

    let isValid = true;
    let message = 'Cumple con todas las reglas';

    if (total === 0) {
      isValid = false;
      message = 'Debe contener al menos 1 carta';
    } else if (total > 5) {
      isValid = false;
      message = 'Máximo 5 cartas por fase';
    } else if (correctas === 0) {
      isValid = false;
      message = 'Debe existir al menos 1 carta correcta';
    }

    validationStatusBadge.className = `iq-validation-status ${isValid ? 'valid' : 'invalid'}`;
    validationStatusBadge.innerHTML = `
      <i class="bi ${isValid ? 'bi-check-circle-fill' : 'bi-exclamation-triangle-fill'}"></i>
      <span>${message}</span>
    `;

    btnSaveDeck.disabled = !isValid;
  }

  function escapeHtml(text) {
    if (!text) return '';
    return String(text)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // -------------------------------------------------------------
  // EVENT LISTENERS DEL PANEL Y LISTA
  // -------------------------------------------------------------
  // Cambiar switch de solución correcta
  cartasContainer.addEventListener('click', function(e) {
    const switchEl = e.target.closest('.iq-switch-container');
    if (switchEl) {
      const idx = parseInt(switchEl.getAttribute('data-idx'));
      if (!isNaN(idx) && currentDeck[idx]) {
        currentDeck[idx].es_solucion_correcta = !currentDeck[idx].es_solucion_correcta;
        renderDeck();
      }
      return;
    }

    // Eliminar carta
    const removeBtn = e.target.closest('.btn-remove-deck-card');
    if (removeBtn) {
      const idx = parseInt(removeBtn.getAttribute('data-idx'));
      if (!isNaN(idx) && currentDeck[idx]) {
        const removed = currentDeck.splice(idx, 1);
        showToast(`"${removed[0].nombre}" removida de la fase.`);
        renderDeck();
      }
    }
  });

  // Eventos de selección de Mundo -> Nivel -> Fase
  selectMundo.addEventListener('change', function() {
    currentMundoId = this.value;
    const mundo = JERARQUIA.find(m => m.id === parseInt(currentMundoId));
    subtextMundo.textContent = mundo ? mundo.nombre_tematico : '';
    populateNiveles(currentMundoId, true);
  });

  selectNivel.addEventListener('change', function() {
    currentNivelId = this.value;
    const mundo = JERARQUIA.find(m => m.id === parseInt(selectMundo.value));
    const nivel = mundo ? mundo.niveles.find(n => n.id === parseInt(currentNivelId)) : null;
    subtextNivel.textContent = nivel ? nivel.titulo : '';
    populateFases(currentNivelId, true);
  });

  selectFase.addEventListener('change', function() {
    currentFaseId = this.value;
    loadDeckForFase(currentFaseId);
  });

  // Botón Cancelar
  btnCancelChanges.addEventListener('click', function() {
    currentDeck = JSON.parse(JSON.stringify(originalDeck));
    renderDeck();
    showToast('Cambios descartados.');
  });

  // Botón Guardar Configuración
  btnSaveDeck.addEventListener('click', function() {
    if (!currentFaseId) {
      showToast('Selecciona una fase válida primero.', true);
      return;
    }

    const payload = {
      cartas: currentDeck.map(c => ({
        carta_id: c.carta_id,
        es_solucion_correcta: c.es_solucion_correcta
      }))
    };

    btnSaveDeck.disabled = true;
    btnSaveDeck.innerHTML = `<span class="spinner-border spinner-border-sm" role="status"></span> Guardando...`;

    fetch(`/admin/core/fasecartaopcion/fase/${currentFaseId}/guardar-ajax/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify(payload)
    })
      .then(res => res.json())
      .then(data => {
        btnSaveDeck.disabled = false;
        btnSaveDeck.innerHTML = `<i class="bi bi-floppy2-fill"></i> Guardar Configuración`;
        if (data.success) {
          originalDeck = JSON.parse(JSON.stringify(currentDeck));
          showToast(data.message || 'Configuración guardada exitosamente.');
        } else {
          showToast(data.error || 'Error al guardar configuración.', true);
        }
      })
      .catch(err => {
        btnSaveDeck.disabled = false;
        btnSaveDeck.innerHTML = `<i class="bi bi-floppy2-fill"></i> Guardar Configuración`;
        showToast('Error de red al guardar configuración.', true);
        console.error(err);
      });
  });

  // -------------------------------------------------------------
  // MODAL DE CATÁLOGO DE CARTAS ACTIVAS
  // -------------------------------------------------------------
  let selectedNormaFilter = 'ALL';
  let selectedUsageFilter = 'ALL'; // 'ALL', 'AVAILABLE', 'USED'
  const usagePillsContainer = document.getElementById('usagePillsContainer');

  function buildModalCatalog() {
    // Extraer normas únicas
    const normas = Array.from(new Set(CARTAS_ACTIVAS.map(c => c.norma_iso))).sort();
    isoPillsContainer.innerHTML = `<button type="button" class="iq-iso-pill ${selectedNormaFilter === 'ALL' ? 'active' : ''}" data-iso="ALL">Todas las Normas</button>`;
    normas.forEach(iso => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = `iq-iso-pill ${selectedNormaFilter === iso ? 'active' : ''}`;
      btn.setAttribute('data-iso', iso);
      btn.textContent = iso;
      isoPillsContainer.appendChild(btn);
    });

    renderCatalogGrid();
  }

  function renderCatalogGrid() {
    const search = (inputSearchModal.value || '').toLowerCase().trim();
    const assignedIds = new Set(currentDeck.map(c => c.carta_id));

    const filtered = CARTAS_ACTIVAS.filter(c => {
      const matchNorma = selectedNormaFilter === 'ALL' || c.norma_iso === selectedNormaFilter;
      const matchSearch = !search ||
        c.nombre.toLowerCase().includes(search) ||
        c.norma_iso.toLowerCase().includes(search) ||
        c.concepto.toLowerCase().includes(search);

      const isAssignedCurrent = assignedIds.has(c.id);
      const isUsedAnywhere = (c.usos && c.usos.length > 0) || isAssignedCurrent;

      let matchUsage = true;
      if (selectedUsageFilter === 'AVAILABLE') {
        matchUsage = !isUsedAnywhere;
      } else if (selectedUsageFilter === 'USED') {
        matchUsage = isUsedAnywhere;
      }

      return matchNorma && matchSearch && matchUsage;
    });

    modalCatalogBody.innerHTML = '';
    if (filtered.length === 0) {
      modalCatalogBody.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: #8b95b5;">
          <i class="bi bi-search" style="font-size: 28px; display: block; margin-bottom: 8px;"></i>
          No se encontraron cartas activas con ese criterio.
        </div>
      `;
      return;
    }

    filtered.forEach(carta => {
      const isAssigned = assignedIds.has(carta.id);
      const isFull = currentDeck.length >= 5;
      const isUsedElsewhere = carta.usos && carta.usos.length > 0;

      let usageBadgeHtml = '';
      if (isAssigned) {
        usageBadgeHtml = `<span class="iq-card-usage-tag assigned-here"><i class="bi bi-check-circle-fill"></i> Ya agregada a esta fase</span>`;
      } else if (isUsedElsewhere) {
        const ubicaciones = carta.usos.map(u => `${u.mundo_codigo} N${u.nivel_numero}-F${u.fase_numero}`).join(', ');
        usageBadgeHtml = `<span class="iq-card-usage-tag used-elsewhere" title="En uso en: ${escapeHtml(ubicaciones)}"><i class="bi bi-layers-fill"></i> En uso (${carta.usos.length} fase${carta.usos.length > 1 ? 's' : ''}): ${escapeHtml(ubicaciones)}</span>`;
      } else {
        usageBadgeHtml = `<span class="iq-card-usage-tag available"><i class="bi bi-stars"></i> Disponible (Sin usar)</span>`;
      }

      const card = document.createElement('div');
      card.className = `iq-catalog-card ${isAssigned ? 'is-assigned' : ''}`;
      card.innerHTML = `
        <div class="iq-catalog-card-head">
          <img src="${carta.imagen_url}" alt="${carta.nombre}" class="iq-catalog-thumb" onerror="this.src='/static/img/cartas/carta_ciberseguridad.png'">
          <div class="iq-catalog-meta">
            <div class="iq-catalog-name" title="${escapeHtml(carta.nombre)}">${escapeHtml(carta.nombre)}</div>
            <div class="iq-catalog-iso">${escapeHtml(carta.norma_iso)}</div>
          </div>
        </div>
        ${usageBadgeHtml}
        <div class="iq-catalog-desc">${escapeHtml(carta.concepto)}: ${escapeHtml(carta.descripcion)}</div>
        <div class="iq-catalog-stats">
          <span><i class="bi bi-lightning-charge-fill" style="color: #06b6d4;"></i> ${carta.fuerza}</span>
          <span><i class="bi bi-shield-fill" style="color: #a855f7;"></i> ${carta.defensa}</span>
        </div>
        <button type="button" class="btn-select-catalog-card ${isAssigned ? 'btn-already-assigned' : ''}" data-id="${carta.id}" ${isAssigned || isFull ? 'disabled' : ''}>
          ${isAssigned ?
            `<i class="bi bi-check2"></i> Ya agregada a esta fase` :
            (isFull ? `Límite alcanzado (5/5)` : `<i class="bi bi-plus-lg"></i> Añadir a Fase`)
          }
        </button>
      `;
      modalCatalogBody.appendChild(card);
    });
  }

  // Abrir Modal
  function openModal() {
    if (currentDeck.length >= 5) {
      showToast('Ya has alcanzado el límite máximo de 5 cartas por fase.', true);
      return;
    }
    inputSearchModal.value = '';
    selectedNormaFilter = 'ALL';
    selectedUsageFilter = 'ALL';
    if (usagePillsContainer) {
      usagePillsContainer.querySelectorAll('.iq-usage-filter-btn').forEach(b => b.classList.remove('active'));
      const allBtn = usagePillsContainer.querySelector('[data-usage="ALL"]');
      if (allBtn) allBtn.classList.add('active');
    }
    buildModalCatalog();
    addCardModal.classList.add('show');
  }

  btnOpenAddModal.addEventListener('click', openModal);
  addMoreSlot.addEventListener('click', function() {
    if (currentDeck.length < 5) {
      openModal();
    }
  });

  btnCloseModal.addEventListener('click', function() {
    addCardModal.classList.remove('show');
  });

  addCardModal.addEventListener('click', function(e) {
    if (e.target === addCardModal) {
      addCardModal.classList.remove('show');
    }
  });

  inputSearchModal.addEventListener('input', renderCatalogGrid);

  if (usagePillsContainer) {
    usagePillsContainer.addEventListener('click', function(e) {
      const btn = e.target.closest('.iq-usage-filter-btn');
      if (btn) {
        usagePillsContainer.querySelectorAll('.iq-usage-filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selectedUsageFilter = btn.getAttribute('data-usage') || 'ALL';
        renderCatalogGrid();
      }
    });
  }

  isoPillsContainer.addEventListener('click', function(e) {
    const pill = e.target.closest('.iq-iso-pill');
    if (pill) {
      isoPillsContainer.querySelectorAll('.iq-iso-pill').forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      selectedNormaFilter = pill.getAttribute('data-iso');
      renderCatalogGrid();
    }
  });

  // Seleccionar carta desde el modal
  modalCatalogBody.addEventListener('click', function(e) {
    const btn = e.target.closest('.btn-select-catalog-card');
    if (btn && !btn.disabled) {
      const cartaId = parseInt(btn.getAttribute('data-id'));
      const carta = CARTAS_ACTIVAS.find(c => c.id === cartaId);
      if (carta) {
        if (currentDeck.length >= 5) {
          showToast('Máximo 5 cartas por fase.', true);
          return;
        }
        currentDeck.push({
          carta_id: carta.id,
          nombre: carta.nombre,
          norma_iso: carta.norma_iso,
          concepto: carta.concepto,
          descripcion: carta.descripcion,
          imagen_url: carta.imagen_url,
          fuerza: carta.fuerza,
          defensa: carta.defensa,
          es_solucion_correcta: currentDeck.length === 0 // si es la primera, marcarla por defecto como correcta
        });
        showToast(`"${carta.nombre}" agregada a la fase.`);
        renderDeck();
        renderCatalogGrid(); // refrescar estado de botones en el modal
        if (currentDeck.length >= 5) {
          addCardModal.classList.remove('show');
        }
      }
    }
  });

  // CSRF Helper
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

  // Inicialización inmediata al cargar
  renderDeck();

})();
