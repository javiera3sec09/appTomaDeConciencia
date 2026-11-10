let hasUploadedImage = document.getElementById('previewLiveCard')?.dataset?.hasImage === 'true';

  function updateCharCounters() {
    const nombre = document.getElementById('id_nombre').value || '';
    const concepto = document.getElementById('id_concepto').value || '';
    const desc = document.getElementById('id_descripcion').value || '';

    document.getElementById('counterNombre').textContent = `${nombre.length}/100`;
    document.getElementById('counterConcepto').textContent = `${concepto.length}/150`;
    document.getElementById('counterDescripcion').textContent = `${desc.length}/250`;

    // Sincronizar en la tarjeta en vivo
    document.getElementById('previewTitle').textContent = nombre.trim() || 'Nombre de la Carta';
    document.getElementById('previewConcepto').textContent = concepto.trim() || 'Concepto ISO';
    document.getElementById('previewDesc').textContent = desc.trim() || 'Describe el efecto o utilidad de esta carta...';
  }

  function updateIsoBadge() {
    const val = document.getElementById('id_norma_iso').value || 'ISO 27001';
    document.getElementById('previewBadgeIso').textContent = val;
  }

  function updateStats() {
    const fuerza = document.getElementById('id_fuerza').value || '0';
    const defensa = document.getElementById('id_defensa').value || '0';
    document.getElementById('previewFuerza').textContent = fuerza;
    document.getElementById('previewDefensa').textContent = defensa;
  }

  function stepNumber(id, delta) {
    const input = document.getElementById(id);
    let val = parseInt(input.value || '0', 10);
    val = isNaN(val) ? 0 : val + delta;
    if (val < 0) val = 0;
    if (val > 100) val = 100;
    input.value = val;
    updateStats();
  }

  function toggleEstadoSwitch(isChecked) {
    const hidden = document.getElementById('id_estado');
    const label = document.getElementById('estadoToggleText');
    const pill = document.getElementById('previewPillEstado');

    if (isChecked) {
      hidden.value = 'activo';
      label.textContent = 'Activo';
      label.classList.remove('inactivo');
      pill.textContent = 'Activo';
      pill.className = 'iq-preview-pill-status activo';
    } else {
      hidden.value = 'inactivo';
      label.textContent = 'Inactivo';
      label.classList.add('inactivo');
      pill.textContent = 'Inactivo';
      pill.className = 'iq-preview-pill-status inactivo';
    }
  }

  function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
      processSelectedFile(file);
    }
  }

  function processSelectedFile(file) {
    if (!file.type.startsWith('image/')) {
      alert('Por favor selecciona un archivo de imagen válido (PNG, JPG, WEBP).');
      return;
    }

    if (file.size > 2 * 1024 * 1024) {
      alert('La imagen excede el límite de 2MB.');
      return;
    }

    // Mostrar pill de archivo seleccionado
    const pill = document.getElementById('fileChosenPill');
    const label = document.getElementById('fileNameLabel');
    label.textContent = file.name;
    pill.style.display = 'inline-flex';

    // Cargar previsualización en vivo
    const reader = new FileReader();
    reader.onload = function(evt) {
      document.getElementById('previewImgElem').src = evt.target.result;
      hasUploadedImage = true;
      forcePreviewMode('live');
    };
    reader.readAsDataURL(file);
  }

  function forcePreviewMode(mode) {
    const emptyState = document.getElementById('previewEmptyState');
    const liveCard = document.getElementById('previewLiveCard');
    const btnEmpty = document.getElementById('btnModeEmpty');
    const btnLive = document.getElementById('btnModeLive');

    if (mode === 'live') {
      emptyState.style.display = 'none';
      liveCard.classList.add('visible');
      btnEmpty.classList.remove('active');
      btnLive.classList.add('active');
    } else {
      emptyState.style.display = 'flex';
      liveCard.classList.remove('visible');
      btnEmpty.classList.add('active');
      btnLive.classList.remove('active');
    }
  }

  // Configuración de Drag & Drop
  document.addEventListener('DOMContentLoaded', () => {
    const dropzone = document.getElementById('dropzoneBox');
    const fileInput = document.getElementById('id_imagen');

    ['dragenter', 'dragover'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.add('dragover');
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.remove('dragover');
      }, false);
    });

    dropzone.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files.length > 0) {
        fileInput.files = files;
        processSelectedFile(files[0]);
      }
    }, false);

    // Event listeners para actualizar en vivo
    ['id_nombre', 'id_concepto', 'id_descripcion'].forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener('input', updateCharCounters);
      }
    });

    const normaEl = document.getElementById('id_norma_iso');
    if (normaEl) {
      normaEl.addEventListener('change', updateIsoBadge);
    }

    ['id_fuerza', 'id_defensa'].forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener('input', updateStats);
      }
    });

    // Inicializar contadores y badges
    updateCharCounters();
    updateIsoBadge();
    updateStats();

    // Si ya tiene imagen o es edición, mostrar la tarjeta en vivo de inmediato
    if (hasUploadedImage) {
      forcePreviewMode('live');
    } else {
      forcePreviewMode('empty');
    }
  });
