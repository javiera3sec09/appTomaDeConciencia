const _initFaseCaso = JSON.parse(document.getElementById('fasecaso-data')?.textContent || '{}');
  const mundosData = _initFaseCaso.mundosData || [];
  const nivelesData = _initFaseCaso.nivelesData || [];

  function onDiffChange(selectElem) {
    const val = selectElem.value;
    const text = selectElem.options[selectElem.selectedIndex].text;
    const pill = document.getElementById('diffPillDisplay');
    if (pill) {
      pill.textContent = text;
      pill.className = 'iq-diff-pill-btn ' + val;
    }
    syncPreview();
  }

  // Sincronización en vivo de campos del formulario con la Vista Previa
  function syncPreview() {
    // Número de Fase
    const numFase = document.getElementById('id_numero_fase').value || '1';
    document.getElementById('previewFaseBadge').textContent = 'Fase ' + numFase;

    // Título del Incidente
    const titulo = document.getElementById('id_titulo_incidente').value.trim() || 'Acceso No Autorizado';
    document.getElementById('previewTitulo').textContent = titulo;

    // Amenaza
    const amenazaSelect = document.getElementById('id_amenaza');
    const amenazaText = amenazaSelect.value || 'Phishing';
    document.getElementById('previewAmenaza').textContent = 'Amenaza: ' + amenazaText;

    // Dificultad
    const difSelect = document.getElementById('id_dificultad');
    const difText = difSelect.options[difSelect.selectedIndex] ? difSelect.options[difSelect.selectedIndex].text : 'Normal';
    document.getElementById('previewDificultad').textContent = 'Dificultad: ' + difText;

    // Contexto del caso & Contador de caracteres
    const contextoInput = document.getElementById('id_caso_contexto');
    const contextoVal = contextoInput.value;
    document.getElementById('casoCounter').textContent = contextoVal.length + '/500';
    document.getElementById('previewContexto').textContent = contextoVal || 'Describe el escenario o situación del incidente...';

    // Oro y XP
    const oro = document.getElementById('id_recompensa_oro').value || '0';
    document.getElementById('previewOro').textContent = oro;

    const xp = document.getElementById('id_recompensa_xp').value || '0';
    document.getElementById('previewXP').textContent = xp;
  }

  // Control numérico con botones de incremento/decremento
  function stepNumber(fieldId, delta) {
    const input = document.getElementById(fieldId);
    if (!input) return;
    let val = parseInt(input.value, 10);
    if (isNaN(val)) val = 0;
    val += delta;
    const min = parseInt(input.min, 10);
    if (!isNaN(min) && val < min) val = min;
    input.value = val;
    syncPreview();
  }

  // Toggle switch de estado Activo/Inactivo
  function toggleEstado(checked) {
    const hiddenInput = document.getElementById('id_estado');
    const label = document.getElementById('estadoText');
    if (checked) {
      hiddenInput.value = 'activo';
      label.textContent = 'Activo';
      label.classList.remove('inactivo');
    } else {
      hiddenInput.value = 'inactivo';
      label.textContent = 'Inactivo';
      label.classList.add('inactivo');
    }
  }

  // Carga y filtra los niveles correspondientes al Mundo seleccionado
  function loadNivelesForMundo(mundoId, preselectNivelId) {
    const quickNivelSelect = document.getElementById('nivelQuickSelector');
    if (!quickNivelSelect) return;

    quickNivelSelect.innerHTML = '';
    const nivelesMundo = nivelesData.filter(n => String(n.mundo_id) === String(mundoId));

    if (nivelesMundo.length === 0) {
      const opt = document.createElement('option');
      opt.value = '';
      opt.textContent = 'Sin niveles disponibles en esta norma';
      quickNivelSelect.appendChild(opt);
      return;
    }

    let selectedId = null;
    nivelesMundo.forEach((n, idx) => {
      const opt = document.createElement('option');
      opt.value = n.id;
      opt.textContent = n.numero_nivel + ' – ' + n.titulo;
      opt.dataset.numero = n.numero_nivel;
      opt.dataset.titulo = n.titulo;
      if (preselectNivelId && String(n.id) === String(preselectNivelId)) {
        opt.selected = true;
        selectedId = n.id;
      } else if (!preselectNivelId && idx === 0) {
        opt.selected = true;
        selectedId = n.id;
      }
      quickNivelSelect.appendChild(opt);
    });

    if (!selectedId && nivelesMundo.length > 0) {
      selectedId = nivelesMundo[0].id;
      quickNivelSelect.value = selectedId;
    }

    onNivelSelectChange(selectedId);
  }

  // Cambio de Mundo superior
  function onMundoSelectChange(mundoId) {
    const mundo = mundosData.find(m => String(m.id) === String(mundoId));
    if (!mundo) return;

    // Actualizar visual de la tarjeta de mundo
    const topImg = document.getElementById('topMundoImg');
    if (topImg) topImg.src = mundo.imagen_url;

    const topDesc = document.getElementById('topMundoDesc');
    if (topDesc) topDesc.textContent = mundo.descripcion_tematica;

    const chipMundo = document.getElementById('assignedMundoChip');
    if (chipMundo) chipMundo.textContent = mundo.codigo_iso;

    // Recargar niveles del mundo seleccionado
    loadNivelesForMundo(mundoId, null);
  }

  // Cambio de Nivel superior
  function onNivelSelectChange(nivelId) {
    if (!nivelId) return;
    const nivel = nivelesData.find(n => String(n.id) === String(nivelId));
    if (!nivel) return;

    // Actualizar descripción de la tarjeta de nivel
    const topDesc = document.getElementById('topNivelDesc');
    if (topDesc) {
      topDesc.textContent = 'Aprende a proteger el acceso a la información (Dificultad: ' + nivel.dificultad + ').';
    }

    // Sincronizar el campo hidden del formulario para envío a Django
    const hiddenNivel = document.getElementById('id_nivel');
    if (hiddenNivel) {
      hiddenNivel.value = nivel.id;
    }

    // Actualizar chip en el banner de destino
    const chipNivel = document.getElementById('assignedNivelChip');
    if (chipNivel) {
      chipNivel.textContent = nivel.numero_nivel + ' – ' + nivel.titulo;
    }
  }

  // Inicializar al cargar la página
  document.addEventListener('DOMContentLoaded', function() {
    syncPreview();
    const mundoSelect = document.getElementById('mundoSelector');
    const currentMundoId = mundoSelect ? mundoSelect.value : '1';
    const initialNivelId = document.getElementById('id_nivel').value;
    loadNivelesForMundo(currentMundoId, initialNivelId);
  });
